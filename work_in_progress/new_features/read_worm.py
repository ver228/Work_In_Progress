# -*- coding: utf-8 -*-
"""
This module defines the NormalizedWorm class

"""

import numpy as np
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter
import warnings


import numba

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
                curve[:, nn], window, pol_degree)

    return smoothed_curve

#%% properties
def _h_bend_angles(skels, segment_size):
    '''this is a vectorize version to calculate the angles between segments
    segment_size points from each side of a center point.
    '''
    s_center = skels[:, segment_size:-segment_size, :] #center points
    s_left = skels[:, :-2*segment_size, :] #left side points
    s_right = skels[:, 2*segment_size:, :] #right side points
    
    d_left = s_left - s_center 
    d_right = s_center - s_right
    
    ang_l = np.arctan2(d_left[...,0], d_left[...,1])
    ang_r = np.arctan2(d_right[...,0], d_right[...,1])
    
    ang = ang_l-ang_r
    ang[ang > np.pi] -= 2 * np.pi
    ang[ang < -np.pi] += 2 * np.pi
    
    return ang

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
class DataPartition():
    def __init__(self, n_segments=49):
        partitions_limits = {'head': (0, 8),
                            'neck': (8, 16),
                            'midbody': (16, 33),
                            'hips': (33, 41),
                            'tail': (41, 49),
                            'head_tip': (0, 3),
                            'head_base': (5, 8),
                            'tail_base': (41, 44),
                            'tail_tip': (46, 49),
                            'all': (0, 49),
                            'body': (8, 41)
                            }
        
        if n_segments != 49:
            r_fun = lambda x : int(round(x/49*n_segments))
            for key in partitions_limits:
                partitions_limits[key] = tuple(map(r_fun, partitions_limits[key]))
        
        self.n_segments = n_segments
        self.partitions_limits =  partitions_limits

    def apply(self, data, partition = 'all', func=np.mean, axis=1):
        assert self.n_segments == data.shape[1]
        assert partition in self.partitions_limits
        
        ini, fin = self.partitions_limits[partition]
        
        d_transform = func(data[:, ini:fin, :], axis=1)
        return d_transform
    
    def apply_partitions(self, data, partitions=None, func=np.mean):
        if partitions is None:
            partitions = self.partitions_limits.keys()
        
        data_transforms = \
        {pp : self.apply(data, partition=pp, func=func) for pp in partitions}
        
        return data_transforms
                                
    
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
        self.ventral_contour = dorsal_contour
        self.skeleton = skeleton
        
        self.n_segments = n_segments
        self.n_frames = n_frames
        
        if widths is not None:
            #I might be able to calculate the widths if the dorsal and ventral contour are given
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
        self.dorsal_contour = _smooth(self.ventral_contour)
        
        
#    @property
#    def signed_areas(self):
#        try:
#            return self._signed_area
#        except:
#            if self.ventral_contour is not None:
#                self._signed_area = _h_signed_areas(self.ventral_contour, self.dorsal_contour)
#                return self._signed_area
#            else:
#                warnings.warn('No contours were given therefore the area cannot be calculated.')
#                return None
#    
#    @property
#    def areas(self):
#        try:
#            return self._area
#        except:
#            self._area = np.abs(self._signed_area)
#            return self._area
#    
#    @property
#    def bend_angles(self):
#        try:
#            return self._bend_angles
#        except:
#            self._bend_angles = _h_bend_angles(self.skeleton, self.bend_segment_size)
#            return self._bend_angles


if __name__ == '__main__':
    from tierpsy.analysis.feat_create.obtainFeaturesHelper import WormFromTableSimple
    from tierpsy.analysis.feat_create.obtainFeatures import getGoodTrajIndexes

    
    import matplotlib.pylab as plt
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
            #%%
            #dd = np.linalg.norm(np.diff(coord_avgs, axis=0), axis=-1)
            
            def _h_orientation_vector(x, axis=None):
                return x[:, -1, :] - x[:, 0, :]
            p_obj = DataPartition()
            coord_avgs = p_obj.apply_partitions(worm.skeleton)
            coord_orientations = p_obj.apply_partitions(worm.skeleton, func=_h_orientation_vector)
            
            
            delta_size = 12
            
            for part in ['head', 'neck', 'midbody', 'hips', 'tail']:
            
                orientation_v = coord_orientations[part].copy()
                coords = coord_avgs[part].copy()
                
                
                vv = coords[delta_size:] - coords[:-delta_size]
                speed_c = np.linalg.norm(vv, axis=1)
                
                if part != 'midbody':
                    coords -= coord_avgs['midbody']
                    
                
                velocity = coords[delta_size:] - coords[:-delta_size]
                speed = np.linalg.norm(velocity, axis=1)
                
                #I do not need to normalize the vectors because it will only add a constant factor, 
                #and I am only interested in the sign
                s_sign = np.sign(np.sum(velocity*orientation_v[delta_size:], axis=1))
                signed_speed = speed *s_sign
            
                
                orientation = np.arctan2(orientation_v[:, 0], orientation_v[:, 1])
                orientation = nanunwrap(orientation)
                angular_velocity = orientation[delta_size:] - orientation[:-delta_size]
                
                
                xlim = (0, 500)
                plt.figure()
                plt.subplot(2,1,1)
                #plt.plot(np.abs(np.diff(signed_speed)))
                plt.plot(angular_velocity)
                plt.xlim(xlim)
                plt.subplot(2,1,2)
                plt.plot(speed_c)
                plt.plot(speed)
                
                plt.xlim(xlim)
                
                plt.title(part)
            
            
            #%%
            
            
            
            
            #%%
            
            #% normalise orientation
            #speed = sqrt(sum(velocity.^2));
            #signedSpeed = sign(sum(velocity.*orientation)).*speed;

            #plt.plot(coord_avgs['head'][:, 0])
            #plt.plot(coord_avgs['midbody'][:, 0])
            #plt.plot(coord_avgs['head'][:, 0]-coord_avgs['midbody'][:, 0])
            
            #%%
            #plt.figure()
            #plt.plot(xx,yy, '-')
            #plt.axis('equal')
            #vv = np.linalg.norm(np.diff(worm.skeleton, axis=0), axis=2)
            
            
            
            #%%
            break
        #%%
            plt.figure()
            #plt.plot(worm.skeleton[0,:,0], worm.skeleton[0,:,1], '.-')
            #plt.plot(worm.ventral_contour[0,:,0], worm.ventral_contour[0,:,1], '.-')
            #plt.plot(worm.dorsal_contour[0,:,0], worm.dorsal_contour[0,:,1], '.-')
            
            plt.plot(wormN.skeleton[0,:,0], wormN.skeleton[0,:,1], '.-')
            plt.plot(wormN.ventral_contour[0,:,0], wormN.ventral_contour[0,:,1], '.-')
            plt.plot(wormN.dorsal_contour[0,:,0], wormN.dorsal_contour[0,:,1], '.-')
            plt.axis('equal')
        #%%
            
            #%%
            skels = wormN.skeleton
            angles = [(segment_size, _h_bend_angles(skels, segment_size)) for segment_size in  range(4,8)]
            
            tot = len(angles)
            n_cols = tot
            n_rows = 2#int(np.ceil(tot/n_cols))
            
            import matplotlib.cm as cm
            segment_size, ang = angles[2]
            
            n_range = 301
            start_p = 7000
            delta_f = 30
            for ii in range(start_p, start_p+n_range, delta_f):
                plt.figure(figsize=(3*n_cols,3*n_rows))
                
                for iseg, (segment_size, ang) in enumerate(angles):
                    plt.subplot(2, n_cols, iseg+1)
                    x = wormN.skeleton[ii,:,0]
                    y = wormN.skeleton[ii,:,1]
                    c = (ang[ii]+np.pi)/(2*np.pi)
                    c = np.pad(c, (segment_size,segment_size), 'edge')
                    c = cm.plasma(c)
                    plt.scatter(x, y, c=c)
                    plt.axis('equal')
                    
                    
                    plt.subplot(2,n_cols, iseg+1+n_cols)
                    dd = np.arange(ang[ii].size) + segment_size
                    plt.plot(dd, ang[ii], '.-')
                    
                    plt.xlim(0, x.size)
                    
            
             #%%
            
            
#            plt.figure(figsize = (15, 5))
#            plt.subplot(1,2,1)
#                
#            plt.plot(, '.-')
#            plt.plot(wormN.ventral_contour[ii,:,0], wormN.ventral_contour[ii,:,1], '.-')
#            plt.plot(wormN.dorsal_contour[ii,:,0], wormN.dorsal_contour[ii,:,1], '.-')
#            plt.axis('equal')
#            
#            for segment_size, ang in angles:
#                #plt.subplot(2,1,2)
#                #plt.plot(ang[:, 0])
#                
#                plt.subplot(1,2,2)
#                dd = np.arange(ang[ii].size) + segment_size
#                plt.plot(dd, ang[ii], '.-')
          #%%     
        break
#%%



