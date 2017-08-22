# -*- coding: utf-8 -*-
"""
This module defines the NormalizedWorm class

"""

import numpy as np
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter

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

class SmoothedWorm():
    """
    Encapsulates the notion of a worm's elementary measurements, scaled
    (i.e. "normalized") to 49 points along the length of the worm.
    """

    def __init__(self, 
                 skeleton, 
                 widths = None, 
                 ventral_contour = None, 
                 dorsal_contour = None,
                 skel_smooth_window = None,
                 coords_smooth_window = None
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
        
        
        def _fix_smooth(smooth_window):
            if smooth_window is not None and smooth_window % 2 == 0:
                smooth_window += 1
            assert smooth_window is None or smooth_window > self.pol_degree
            return smooth_window
        
        self.pol_degree = 3
        
        skel_smooth_window = _fix_smooth(skel_smooth_window)
        coords_smooth_window = _fix_smooth(coords_smooth_window)
        
        self._smooth_coords(s_win = coords_smooth_window)
        self._smooth_skeletons(s_win = skel_smooth_window)
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
    
    def _smooth_skeletons(self, s_win):
        if s_win is None:
            return
        
        def _smooth(curves, pol_degree=3):
            if curves is not None:
                for ii in range(curves.shape[0]):
                    if not np.any(np.isnan(curves[ii])):
                        curves[ii] = _h_smooth_curve(
                            curves[ii], 
                            window = s_win, 
                            pol_degree = self.pol_degree
                            )
            return curves
        
        self.skeleton = _smooth(self.skeleton)
        self.widths = _smooth(self.widths)
        self.ventral_contour = _smooth(self.ventral_contour)
        self.dorsal_contour = _smooth(self.dorsal_contour)

    def _smooth_coords(self, s_win):
        if s_win is None:
            return
        
        good_index, = np.where(~np.isnan(self.skeleton[:, 0, 0]))
        
        def _smooth(dat):
            dat_S = np.full_like(dat, np.nan)
            for ii in range(dat.shape[1]):
                fx = interp1d(good_index, dat[good_index, ii, 0])
                fy = interp1d(good_index, dat[good_index, ii, 1])
                
                ind = np.arange(good_index[0], good_index[-1]+1)
                
                xx = fx(ind)
                yy = fy(ind)
                xs = savgol_filter(xx, s_win, self.pol_degree)
                ys = savgol_filter(yy, s_win, self.pol_degree)
                
                good_index_s = good_index-good_index[0]
                
                dat_S[good_index, ii, 0] = xs[good_index_s]
                dat_S[good_index, ii, 1] = ys[good_index_s]
                
            return dat_S
        
        self.skeleton = _smooth(self.skeleton)
        self.ventral_contour = _smooth(self.ventral_contour)
        self.dorsal_contour = _smooth(self.dorsal_contour)



if __name__ == '__main__':
    from tierpsy.analysis.feat_create.obtainFeaturesHelper import WormFromTableSimple
    from tierpsy.analysis.feat_create.obtainFeatures import getGoodTrajIndexes
    from tierpsy.helper.misc import RESERVED_EXT
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
    #mask_dir = '/Users/ajaver/OneDrive - Imperial College London/tests/join/'
    
    #save_dir = '/Users/ajaver/OneDrive - Imperial College London/smooth_examples'
    save_dir = './'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    fnames = glob.glob(os.path.join(mask_dir, '*.hdf5'))
    fnames = [x for x in fnames if any(fnmatch.fnmatch(x, ext) for ext in exts)]
    fnames = [x for x in fnames if not any(x.endswith(ext) for ext in RESERVED_EXT)]
    
    #x.n_valid_skel/x.n_frames >= feat_filt_param['bad_seg_thresh']]
    for mask_video in fnames[1:]:
        skeletons_file = mask_video.replace('MaskedVideos','Results').replace('.hdf5', '_skeletons.hdf5')
        good_traj_index, worm_index_type = getGoodTrajIndexes(skeletons_file)
        for iw, worm_index in enumerate(good_traj_index):
            worm = WormFromTableSimple(skeletons_file,
                                worm_index,
                                worm_index_type=worm_index_type
                                )
            
            wormN = SmoothedWorm(
                     worm.skeleton, 
                     worm.widths, 
                     worm.ventral_contour, 
                     worm.dorsal_contour,
                     skel_smooth_window = 5,
                     coords_smooth_window = 11
                    )
            
            save_file = os.path.join(save_dir, 'worm_example_W{}.npz'.format(worm_index))
            np.savez(save_file, 
                     skeleton=wormN.skeleton, 
                     ventral_contour=wormN.ventral_contour, 
                     dorsal_contour=wormN.dorsal_contour
                     )
            
            
            #%%
            break
            
        break
        
#%%


