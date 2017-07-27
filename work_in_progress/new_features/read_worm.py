# -*- coding: utf-8 -*-
"""
This module defines the NormalizedWorm class

"""

import numpy as np
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter
import warnings

def _h_signed_area(cnt_side1, cnt_side2):
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



def _h_resample_curve(curve, resampling_N=49, widths=None):
    '''Resample curve to have resampling_N equidistant segments
    I give width as an optional parameter since I want to use the 
    same interpolation as with the skeletons
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


class NormalizedWormN():
    """
    Encapsulates the notion of a worm's elementary measurements, scaled
    (i.e. "normalized") to 49 points along the length of the worm.

    The data consists of 7 Numpy arrays (where n is the number of frames):
   - Of shape (n_frames, n_segments,2):
        ventral_contour
        dorsal_contour
        skeleton
    - Of shape (n_frames, 49):
        angles
        widths
    - Of shape (n_frames):
        length
        area
    """

    def __init__(self, 
                 skeleton, 
                 widths = None, 
                 ventral_contour = None, 
                 dorsal_contour = None,
                 smooth_window = None):
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
            #I might be able to calculate the widths if the dorsal and ventral contour are given
            self.widths = widths
            assert widths.shape == (n_frames, n_segments)
        
        
        self._smooth_coords(smooth_window)
        self._resample_coords()
        
    def _resample_coords(self):
        
        def _resample(A, W = None):
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
        
        
    @property
    def signed_area(self):
        try:
            return self._signed_area
        except:
            if self.ventral_contour is not None:
                self._signed_area = _h_signed_area(self.ventral_contour, self.dorsal_contour)
                return self._signed_area
            else:
                warnings.warn('No contours were given therefore the area cannot be calculated.')
                return None
    
    @property
    def area(self):
        try:
            return self._area
        except:
            self._area = np.abs(self._signed_area)
            return self._area

#    @property
#    def angles(self):
#        try:
#            return self._angles 
#        except:
#            #I could use the unnormalized skeleton (more points), but it shouldn't make much a huge difference.
#            self._angles = WormParsing.compute_angles(self.skeleton)
#
#            if self.video_info.ventral_mode == 2:
#                #switch in the angle sign in case of the contour orientation is anticlockwise
#                self._angles = -self._angles
#            
#            return self._angles

            #A second option would be to use the contour orientation to find the correct side
            # if self.signed_area is not None:
            #     #I want to use the signed area to determine the contour orientation.
            #     #first assert all the contours have the same orientation. This might be a problem 
            #     #if the worm does change ventral/dorsal orientation, but for the moment let's make it a requirement.
            #     valid = self.signed_area[~np.isnan(self.signed_area)]
            #     assert np.all(valid>=0) if valid[0]>=0 else np.all(valid<=0) 

            #     #if the orientation is anticlockwise (negative signed area) change the sign of the angles
            #     if valid[0] < 0:
            #         self._angles *= -1
#
#    def angle(self):
#        """
#        Frame-by-frame mean of the skeleton points
#
#        Returns
#        ---------------------------------------
#        A numpy array of length n, giving for each frame
#        the angle formed by the first and last skeleton point.
#
#        """
#        try:
#            return self._angle
#        except AttributeError:
#            s = self.skeleton
#            # obtain vector between first and last skeleton point
#            v = s[-1, :, :] - s[0, :, :]
#            # find the angle of this vector
#            self._angle = np.arctan2(v[1, :], v[0, :]) * (180 / np.pi)
#
#            return self._angle


    @property
    def centred_skeleton(self):
        """
        Return a skeleton numpy array with each frame moved so the
        centroid of the worm is 0,0

        Returns
        ---------------------------------------
        A numpy array with the above properties.

        """
        try:
            return self._centred_skeleton
        except AttributeError:
            s = self.skeleton

            if s.size != 0:
                s_mean = np.ones(s.shape) * self.centre
                self._centred_skeleton = s - s_mean
            else:
                self._centred_skeleton = s

            return self._centred_skeleton

    @property
    def orientation_free_skeleton(self):
        """
        Perform both a rotation and a translation of the skeleton

        Returns
        ---------------------------------------
        A numpy array, which is the centred and rotated normalized
        worm skeleton.

        Notes
        ---------------------------------------
        To perform this matrix multiplication we are multiplying:
          rot_matrix * s
        This is shape 2 x 2 x n, times 2 x 49 x n.
        Basically we want the first matrix treated as two-dimensional,
        and the second matrix treated as one-dimensional,
        with the results applied elementwise in the other dimensions.

        To make this work I believe we need to pre-broadcast rot_matrix
        into the skeleton points dimension (the one with 49 points) so
        that we have
          2 x 2 x 49 x n, times 2 x 49 x n
        #s1 = np.rollaxis(self.skeleton, 1)

        #rot_matrix = np.ones(s1.shape) * rot_matrix

        #self.skeleton_rotated = rot_matrix.dot(self.skeleton)

        """
        try:
            return self._orientation_free_skeleton
        except AttributeError:
            orientation = self.angle

            # Flip and convert to radians
            a = -orientation * (np.pi / 180)

            rot_matrix = np.array([[np.cos(a), -np.sin(a)],
                                   [np.sin(a), np.cos(a)]])

            # We need the x,y listed in the first dimension
            s1 = np.rollaxis(self.centred_skeleton, 1)

            # For example, here is the first point of the first frame rotated:
            # rot_matrix[:,:,0].dot(s1[:,0,0])

            # ATTEMPTING TO CHANGE rot_matrix from 2x2x49xn to 2x49xn
            # rot_matrix2 = np.ones((2, 2, s1.shape[1],
            #                        s1.shape[2])) * rot_matrix

            s1_rotated = []

            # Rotate the worm frame-by-frame and add these skeletons to a list
            for frame_index in range(self.num_frames):
                s1_rotated.append(rot_matrix[:, :, frame_index].dot
                                  (s1[:, :, frame_index]))
            # print(np.shape(np.rollaxis(rot_matrix[:,:,0].dot(s1[:,:,0]),0)))

            # Save the list as a numpy array
            s1_rotated = np.array(s1_rotated)

            # Fix the axis settings
            self._orientation_free_skeleton = \
                np.rollaxis(np.rollaxis(s1_rotated, 0, 3), 1)

            return self._orientation_free_skeleton

#    @property
#    def num_frames(self):
#        """
#        The number of frames in the video.
#
#        Returns
#        ---------------------------------------
#        int
#          number of frames in the video
#
#        """
#        try:
#            return self._num_frames
#        except AttributeError:
#            self._num_frames = self.skeleton.shape[2]
#
#            return self._num_frames

#    def position_limits(self, dimension, measurement='skeleton'):
#        """
#        Maximum extent of worm's travels projected onto a given axis
#
#        Parameters
#        ---------------------------------------
#        dimension: specify 0 for X axis, or 1 for Y axis.
#
#        Notes
#        ---------------------------------------
#        Dropped frames show up as NaN.
#        nanmin returns the min ignoring such NaNs.
#
#        """
#        d = getattr(self, measurement)
#        if(len(d.shape) < 3):
#            raise Exception("Position Limits Is Only Implemented for 2D data")
#        return (np.nanmin(d[:, dimension, :]),
#                np.nanmax(d[:, dimension, :]))

#    @property
#    def contour(self):
#        return self.get_contour(keep_redundant_points=True)
#
#    @property
#    def contour_without_redundant_points(self):
#        return self.get_contour(keep_redundant_points=False)
#
#    def get_contour(self, keep_redundant_points=True):
#        """
#        The contour of the worm as one 96-point or 98-point polygon.
#
#        That is:
#
#        Go from ventral_contour shape (49,2,n) and
#            dorsal_contour shape (49,2,n) to
#            contour with      shape (96,2,n) or (98,2,n)
#
#        Why 96 instead of 49x2 = 98?
#        Because the first and last points are duplicates, so if
#        keep_redundant_points=False, we omit those on the second set.
#
#        In either case we reverse the contour so that
#        it encompasses an "out and back" contour.
#
#        """
#        if keep_redundant_points:
#            return np.concatenate((self.ventral_contour,
#                                   self.dorsal_contour[::-1, :, :]))
#        else:
#            return np.concatenate((self.ventral_contour,
#                                   self.dorsal_contour[-2:0:-1, :, :]))
#
#    @property
#    def contour_x(self):
#        # Note that this includes 2 redundant points.
#        return self.contour[:, 0, :]
#
#    @property
#    def contour_y(self):
#        # Note that this includes 2 redundant points.
#        return self.contour[:, 1, :]
#
#    @property
#    def skeleton_x(self):
#        return self.skeleton[:, 0, :]
#
#    @property
#    def skeleton_y(self):
#        return self.skeleton[:, 1, :]
#
#    @property
#    def ventral_contour_x(self):
#        return self.ventral_contour[:, 0, :]
#
#    @property
#    def ventral_contour_y(self):
#        return self.ventral_contour[:, 1, :]
#
#    @property
#    def dorsal_contour_x(self):
#        return self.dorsal_contour[:, 0, :]
#
#    @property
#    def dorsal_contour_y(self):
#        return self.dorsal_contour[:, 1, :]
#
#    def __eq__(self, other):
#        """
#        Compare this Normalized worm against another.
#
#        TODO: Idea from @JimHokanson:
#        Do this on a frame by frame basis, do some sort of distance
#        computation rather than all together. This might hide bad frames
#        i.e. besides using correlation for comparison, a normalized distance
#        comparison that could catch extreme outliers would also be useful
#
#        """
#        attribute_list = ['skeleton_x', 'skeleton_y',
#                          'ventral_contour_x', 'ventral_contour_y',
#                          'dorsal_contour_x', 'dorsal_contour_y',
#                          'angles', 'widths', 'length', 'area']
#
#        return utils.compare_attributes(self, other, attribute_list,
#                                        high_corr_value=0.94,
#                                        merge_nans_list=['angles'])
#
#    def __repr__(self):
#        # TODO: This omits the properties above ...
#        return utils.print_object(self)
#
#    def plot_path(self, posture_index):
#        """
#        Plot the path of the contour, skeleton and widths
#
#        Parameters
#        ----------------
#        posture_index: int
#            The desired posture point (along skeleton and contour) to plot.
#
#        """
#        vc = self.ventral_contour[posture_index, :, :]
#        nvc = self.dorsal_contour[posture_index, :, :]
#        skeleton_x = self.skeleton[posture_index, 0, :]
#        skeleton_y = self.skeleton[posture_index, 1, :]
#
#        plt.scatter(vc[0, :], vc[1, :])
#        plt.scatter(nvc[0, :], nvc[1, :])
#        plt.scatter(skeleton_x, skeleton_y)
#        plt.gca().set_aspect('equal', adjustable='box')
#        plt.show()
#
#    def plot_posture(self, frame_index):
#        """
#        Show a scatterplot of the contour, skeleton and widths of frame #frame
#
#        Parameters
#        ----------------
#        frame_index: int
#            The desired frame # to plot.
#
#        """
#        vc = self.ventral_contour[:, :, frame_index]
#        nvc = self.dorsal_contour[:, :, frame_index]
#        skeleton = self.skeleton[:, :, frame_index]
#
#        plt.scatter(vc[:, 0], vc[:, 1], c='red')
#        plt.scatter(nvc[:, 0], nvc[:, 1], c='blue')
#        plt.scatter(skeleton[:, 0], skeleton[:, 1], c='black')
#        plt.gca().set_aspect('equal', adjustable='box')
#        plt.show()
#
#    def plot_contour(self, frame_index):
#        NormalizedWorm.plot_contour_with_labels(
#            self.contour[:, :, frame_index])
#
#    @staticmethod
#    def plot_contour_with_labels(contour, frame_index=0):
#        """
#        Makes a beautiful plot with all the points labeled.
#
#        Parameters:
#        One frame's worth of a contour
#
#        """
#        contour_x = contour[:, 0, frame_index]
#        contour_y = contour[:, 1, frame_index]
#        plt.plot(contour_x, contour_y, 'r', lw=3)
#        plt.scatter(contour_x, contour_y, s=35)
#        labels = list(str(l) for l in range(0, len(contour_x)))
#        for label_index, (label, x, y), in enumerate(
#                zip(labels, contour_x, contour_y)):
#            # Orient the label for the first half of the points in one direction
#            # and the other half in the other
#            if label_index <= len(contour_x) // 2 - \
#                    1:  # Minus one since indexing
#                xytext = (20, -20)                     # is 0-based
#            else:
#                xytext = (-20, 20)
#            plt.annotate(
#                label, xy=(
#                    x, y), xytext=xytext, textcoords='offset points', ha='right', va='bottom', bbox=dict(
#                    boxstyle='round,pad=0.5', fc='yellow', alpha=0.5), arrowprops=dict(
#                    arrowstyle='->', connectionstyle='arc3,rad=0'))  # , xytext=(0,0))

    
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
        
        #for ii in range(0, 250, 10):
        ii = 0
        plt.figure()
        plt.subplot(2,2,1)
            
        plt.plot(wormN.skeleton[ii,:,0], wormN.skeleton[ii,:,1], '.-')
        plt.plot(wormN.ventral_contour[ii,:,0], wormN.ventral_contour[ii,:,1], '.-')
        plt.plot(wormN.dorsal_contour[ii,:,0], wormN.dorsal_contour[ii,:,1], '.-')
        plt.axis('equal')
        
        for d_n in range(4,7):#(1,10):
        
            s_center = skels[:, d_n:-d_n, :]
            s_left = skels[:, :-2*d_n, :]
            s_right = skels[:, 2*d_n:, :]
            
            d_left = s_left - s_center
            d_right = s_center - s_right
            
            ang_l = np.arctan2(d_left[...,0], d_left[...,1])
            ang_r = np.arctan2(d_right[...,0], d_right[...,1])
            
            ang = ang_l-ang_r
            ang[ang > np.pi] -= 2 * np.pi
            ang[ang < -np.pi] += 2 * np.pi
            
            plt.subplot(2,2,2)
            
            dd = np.arange(ang[ii].size) + d_n
            plt.plot(dd, ang[ii], '.-')
        
            plt.subplot(2,1,2)
            plt.plot(ang[:, 0])
          #%%     
        break