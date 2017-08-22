# -*- coding: utf-8 -*-
"""
This module defines the NormalizedWorm class

"""

import numpy as np
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter
import numba
import tables
import warnings

@numba.jit
def fillfnan(arr):
    '''
    fill foward nan values (iterate using the last valid nan)
    I define this function so I do not have to call pandas DataFrame
    '''
    out = arr.copy()
    for idx in range(out.shape[0]):
        if np.isnan(out[idx]):
            out[idx] = out[idx - 1]
    return out

def nanunwrap(x):
    '''correct for phase change for a vector with nan values 
    '''
    bad = np.isnan(x)
    x = fillfnan(x)
    x = np.unwrap(x)
    x[bad] = np.nan
    return x

#%% properties
def _h_tangent_angles(skels, points_window):
    '''this is a vectorize version to calculate the angles between segments
    segment_size points from each side of a center point.
    '''
    s_center = skels[:, points_window:-points_window, :] #center points
    s_left = skels[:, :-2*points_window, :] #left side points
    s_right = skels[:, 2*points_window:, :] #right side points
    
    d_left = s_left - s_center 
    d_right = s_center - s_right
    
    #arctan2 expects the y,x angle
    ang_l = np.arctan2(d_left[...,1], d_left[...,0])
    ang_r = np.arctan2(d_right[...,1], d_right[...,0])
    
    with warnings.catch_warnings():
        #I am unwraping in one dimension first
        warnings.simplefilter("ignore")
        ang = np.unwrap(ang_r-ang_l, axis=1);
    
    for ii in range(ang.shape[1]):
        ang[:, ii] = nanunwrap(ang[:, ii])
    return ang

def _h_curvature(skeletons, points_window, lengths=None):
    if lengths is None:
        #caculate the length if it is not given
        lengths = _h_lengths(skeletons)
    
    #Number of segments is the number of vertices minus 1
    n_segments = skeletons.shape[1] -1 
    
    #This is the fraction of the length the angle is calculated on
    length_frac = 2*(points_window-1)/(n_segments-1)
    segment_length = length_frac*lengths
    segment_angles = _h_tangent_angles(skeletons, points_window)
    
    curvature = segment_angles/segment_length[:, None]
    
    return curvature
    


def _h_curvature_test(skeletons):
    '''
    Calculate the curvature using univariate splines. This method is slower and can fail
    badly if the fit does not work, so I am only using it as testing
    '''
    from scipy.interpolate import UnivariateSpline
    
    def _get_curvature(skel):
        if np.any(np.isnan(skel)):
            return np.full(skel.shape[0], np.nan)
        
        x = skel[:, 0]
        y = skel[:, 1]
        n = np.arange(x.size)
    
        fx = UnivariateSpline(n, x, k=5)
        fy = UnivariateSpline(n, y, k=5)
    
        x_d = fx.derivative(1)(n)
        x_dd = fx.derivative(2)(n)
        y_d = fy.derivative(1)(n)
        y_dd = fy.derivative(2)(n)
        curvature = (x_d*y_dd - y_d*x_dd) / np.power(x_d** 2 + y_d** 2, 3 / 2)
        return  curvature
    
    
    curvatures_fit = np.array([_get_curvature(skel) for skel in skeletons])
    return curvatures_fit


#%%
def _h_angles(skeletons):
    dd = np.diff(skeletons,axis=1);
    angles = np.arctan2(dd[...,0], dd[...,1])
    
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        angles = np.unwrap(angles, axis=1);
    
    mean_angles = np.mean(angles, axis=1)
    angles -= mean_angles[:, None]
    
    return angles, mean_angles


EIGEN_PROJECTION_FILE = 'master_eigen_worms_N2.mat'
def _h_eigen_projections(skeletons):
    with tables.File(EIGEN_PROJECTION_FILE) as fid:
        eigen_worms = fid.get_node('/eigenWorms')[:]
        eigen_worms = eigen_worms.T
    
    angles, _ = _h_angles(skeletons)   
    eigen_projections = np.dot(eigen_worms, angles.T)
    eigen_projections = np.rollaxis(eigen_projections, -1, 0)
    return eigen_projections

#%%   

def _h_signed_areas(cnt_side1, cnt_side2):
    '''calculate the contour area using the shoelace method, the sign indicate the contour orientation.'''
    assert cnt_side1.shape == cnt_side2.shape
    if cnt_side1.ndim == 2:
        # if it is only two dimenssion (as if in a single skeleton).
        # Add an extra dimension to be compatible with the rest of the code
        cnt_side1 = cnt_side1[None, ...]
        cnt_side2 = cnt_side2[None, ...]

    contour = np.hstack((cnt_side1, cnt_side2[:, ::-1, :]))
    signed_area = np.sum(
        contour[:,:-1,0] * contour[:,1:,1] -
        contour[:,1:,0] * contour[:,:-1,1],
        axis=1)/ 2
    
    assert signed_area.size == contour.shape[0]
    return signed_area


def _h_lengths(skeletons):
    '''
    Calculate length using the skeletons
    '''
    delta_coords = np.diff(skeletons, axis=1)
    segment_sizes = np.linalg.norm(delta_coords, axis=2)
    w_lenght = np.sum(segment_sizes, axis=1)
    return w_lenght

#%%
def _h_resample_curve(curve, resampling_N=49, widths=None):
    '''Resample curve to have resampling_N equidistant segments
    I give width as an optional parameter since I want to use the 
    same interpolation as with the skeletons
    
    I calculate the length here indirectly
    '''

    # calculate the cumulative length for each segment in the curve
    dx = np.diff(curve[:, 0])
    dy = np.diff(curve[:, 1])
    dr = np.sqrt(dx * dx + dy * dy)

    lengths = np.cumsum(dr)
    lengths = np.hstack((0, lengths))  # add the first point
    tot_length = lengths[-1]

    # Verify array lengths
    if len(lengths) < 2 or len(curve) < 2:
        return None, None, None

    fx = interp1d(lengths, curve[:, 0])
    fy = interp1d(lengths, curve[:, 1])

    subLengths = np.linspace(0 + np.finfo(float).eps, tot_length, resampling_N)

    # I add the epsilon because otherwise the interpolation will produce nan
    # for zero
    try:
        resampled_curve = np.zeros((resampling_N, 2))
        resampled_curve[:, 0] = fx(subLengths)
        resampled_curve[:, 1] = fy(subLengths)
        if widths is not None:
            fw = interp1d(lengths, widths)
            widths = fw(subLengths)
    except ValueError:
        resampled_curve = np.full((resampling_N, 2), np.nan)
        widths = np.full(resampling_N, np.nan)

    return resampled_curve, tot_length, widths


def _h_smooth_curve(curve, window=5, pol_degree=3):
    '''smooth curves using the savgol_filter'''

    if curve.shape[0] < window:
        # nothing to do here return an empty array
        return np.full_like(curve, np.nan)

    # consider the case of one (widths) or two dimensions (skeletons, contours)
    if curve.ndim == 1:
        smoothed_curve = savgol_filter(curve, window, pol_degree)
    else:
        smoothed_curve = np.zeros_like(curve)
        for nn in range(curve.ndim):
            smoothed_curve[:, nn] = savgol_filter(
                curve[:, nn], window, pol_degree, mode='mirror')

    return smoothed_curve

                                
    
#%%

class NormalizedWormN():
    """
    Encapsulates the notion of a worm's elementary measurements, scaled
    (i.e. "normalized") to 49 points along the length of the worm.
    """

    def __init__(self, 
                 skeleton, 
                 widths = None, 
                 ventral_contour = None, 
                 dorsal_contour = None,
                 smooth_window = None
                 ):
        """
        I assume data is evenly distributed in time, and missing frames are nan.
        """
        
        #validate dimenssions
        n_frames, n_segments, n_dims = skeleton.shape
        assert n_dims == 2
        if ventral_contour is not None:
            assert dorsal_contour is not None
            assert ventral_contour.shape == (n_frames, n_segments, n_dims)
            assert ventral_contour.shape == dorsal_contour.shape


        self.ventral_contour = ventral_contour
        self.dorsal_contour = dorsal_contour
        self.skeleton = skeleton
        
        self.n_segments = n_segments
        self.n_frames = n_frames
        
        if widths is not None:
            #TODO I might be able to calculate the widths if the dorsal and ventral contour are given
            self.widths = widths
            assert widths.shape == (n_frames, n_segments)
        
        
        self._smooth_coords(smooth_window)
        self._resample_coords()
        
    def _resample_coords(self):
        
        def _resample(A, W = None):
            #I am adding the W as width, in the case of skeletons, 
            #I want to interpolate the widths using the same spacing
            new_A = np.full_like(A, np.nan)
            
            if W is not None:
                new_W = np.full(self.n_frames, np.nan)
                L = np.full(self.n_frames, np.nan)
                for ii in range(A.shape[0]):
                    new_A[ii], L[ii], W[ii] = \
                        _h_resample_curve(A[ii], self.n_segments, W[ii])
                return new_A, L, new_W
            else:
                for ii in range(A.shape[0]):
                    new_A[ii], _, _ = _h_resample_curve(A[ii], self.n_segments)
                return new_A
        
        
        self.skeleton, self.length, self.widths = _resample(self.skeleton, W = self.widths)
        if self.dorsal_contour is not None:
            self.ventral_contour = _resample(self.ventral_contour)
            self.dorsal_contour = _resample(self.dorsal_contour)
    
    def _smooth_coords(self, smooth_window = None):
        if smooth_window is None:
            return
        
        POL_DEGREE_DFLT = 3
        if smooth_window % 2 == 0:
            smooth_window += 1
        
        assert smooth_window>POL_DEGREE_DFLT

        def _smooth(curves, pol_degree=3):
            if curves is not None:
                for ii in range(curves.shape[0]):
                    if not np.any(np.isnan(curves[ii])):
                        curves[ii] = _h_smooth_curve(
                            curves[ii], window = smooth_window, pol_degree=pol_degree)
            return curves
        
        self.skeleton = _smooth(self.skeleton)
        self.widths = _smooth(self.widths)
        self.ventral_contour = _smooth(self.ventral_contour)
        self.dorsal_contour = _smooth(self.dorsal_contour)


if __name__ == '__main__':
    from tierpsy.analysis.feat_create.obtainFeaturesHelper import WormFromTableSimple
    from tierpsy.analysis.feat_create.obtainFeatures import getGoodTrajIndexes
    import glob
    import os
    import fnmatch
    
    exts = ['']

    exts = ['*'+ext+'.hdf5' for ext in exts]
    
    #mask_dir = '/Volumes/behavgenom_archive$/Avelino/screening/CeNDR/MaskedVideos/CeNDR_Set1_310517/'
    #mask_dir = '/Volumes/behavgenom_archive$/Avelino/screening/CeNDR/MaskedVideos/CeNDR_Set1_160517/'
    #mask_dir = '/Volumes/behavgenom_archive$/Avelino/screening/CeNDR/MaskedVideos/CeNDR_Set1_020617/'
    #mask_dir = '/Volumes/behavgenom_archive$/Avelino/Worm_Rig_Tests/Test_Food/MaskedVideos/FoodDilution_041116'
    #mask_dir = '/Volumes/behavgenom_archive$/Avelino/screening/Development/MaskedVideos/Development_C1_170617/'
    #mask_dir = '/Volumes/behavgenom_archive$/Avelino/screening/Development/MaskedVideos/**/'
    #mask_dir = '/Users/ajaver/OneDrive - Imperial College London/optogenetics/ATR_210417'
    mask_dir = '/Users/ajaver/OneDrive - Imperial College London/optogenetics/Arantza/MaskedVideos/**/'
    
    fnames = glob.glob(os.path.join(mask_dir, '*.hdf5'))
    fnames = [x for x in fnames if any(fnmatch.fnmatch(x, ext) for ext in exts)]
    
    #x.n_valid_skel/x.n_frames >= feat_filt_param['bad_seg_thresh']]
    for mask_video in fnames[1:]:
        skeletons_file = mask_video.replace('MaskedVideos','Results').replace('.hdf5', '_skeletons.hdf5')
        good_traj_index, worm_index_type = getGoodTrajIndexes(skeletons_file)
        for iw, worm_index in enumerate(good_traj_index):
            worm = WormFromTableSimple(skeletons_file,
                                worm_index,
                                worm_index_type=worm_index_type
                                )
            
            wormN = NormalizedWormN(
                     worm.skeleton, 
                     worm.widths, 
                     worm.ventral_contour, 
                     worm.dorsal_contour,
                     smooth_window=5
                    )
            
            
            np.savez('worm_example_W{}.npz'.format(worm_index), 
                     skeleton=wormN.skeleton, 
                     ventral_contour=wormN.ventral_contour, 
                     dorsal_contour=wormN.dorsal_contour
                     )
            break
            
        break
        
