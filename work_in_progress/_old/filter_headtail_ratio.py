# -*- coding: utf-8 -*-
"""
Created on Fri May 13 11:58:51 2016

@author: ajaver
"""
import tables
import matplotlib.pylab as plt
import numpy as np
import pandas as pd

from MWTracker.trackWorms.getFilteredSkels import saveModifiedTrajData

from MWTracker.trackWorms.getFilteredSkels import getFilteredSkels, _h_nodes2Array, _h_getMahalanobisRobust, getValidIndexes

#skeletons_file = '/Users/ajaver/Desktop/Videos/single_worm/switched_sample/unc-101 (e1265) on food R_2010_09_24__11_37_44___7___2_skeletons.hdf5'
#skeletons_file = '/Users/ajaver/Desktop/Videos/single_worm/switched_sample/unc-104 (e1265)III on food L_2011_10_18__11_29_31__1_skeletons.hdf5'
skeletons_file = '/Users/ajaver/Desktop/Videos/single_worm/switched_sample/egl-12 (n602)V on food R_2010_07_09__15_02_02___2___7_skeletons.hdf5'

getFilteredSkels(skeletons_file, True)

with pd.HDFStore(skeletons_file, 'r') as table_fid:
    trajectories_data = table_fid['/trajectories_data']

body_scale = 0.90
#%%
def calcArea(cnt):
    signed_area = np.sum(cnt[:-1,0]*cnt[1:,1]-cnt[1:,0]*cnt[:-1,1])
    return np.abs(signed_area/2)
    
#%%
def getPerpContourInd(skeleton, skel_ind, contour_side1, contour_side2, contour_width):
    #get the closest point in the contour from a line perpedicular to the skeleton.
    
    #get the slop of a line perpendicular to the keleton
    dR = skeleton[skel_ind+1] - skeleton[skel_ind-1]
    #m = dR[1]/dR[0]; M = -1/m
    a = -dR[0]
    b = +dR[1]
    
    c = b*skeleton[skel_ind,1]-a*skeleton[skel_ind,0]
    
    max_width_squared = np.max(contour_width)**2
    #modified from https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line
    #a = M, b = -1
    
    #make sure we are not selecting a point that get traversed by a coiled worm
    dist2cnt1 = np.sum((contour_side1-skeleton[skel_ind])**2,axis=1)
    d1 = np.abs(a*contour_side1[:,0] - b*contour_side1[:,1]+ c)
    d1[dist2cnt1>max_width_squared] = np.nan
    cnt1_ind = np.nanargmin(d1)
    
    dist2cnt2 = np.sum((contour_side2-skeleton[skel_ind])**2,axis=1)
    d2 = np.abs(a*contour_side2[:,0] - b*contour_side2[:,1]+ c)
    d2[dist2cnt2>max_width_squared] = np.nan
    cnt2_ind = np.nanargmin(d2)
    return cnt1_ind, cnt2_ind
    
#%%
is_good_skel = trajectories_data['has_skeleton'].values.copy()

thresh_ratio = 2/body_scale


with tables.File(skeletons_file, 'r') as ske_file_id:
    skeletons = ske_file_id.get_node('/skeleton')
    contour_side1s = ske_file_id.get_node('/contour_side1')
    contour_side2s = ske_file_id.get_node('/contour_side2')
    contour_widths = ske_file_id.get_node('/contour_width')
    
    tot_frames = contour_widths.shape[0]
    sample_N = contour_widths.shape[1]
    
    ht_limits = int(round(sample_N/6))
    mid_limits = (int(round(3*sample_N/6)), int(round(4*sample_N/6))+1)
    
    for frame_number in [18520]:#range(tot_frames):
        if is_good_skel[frame_number] == 0:
            continue
    
        contour_width = contour_widths[frame_number]
        contour_side1 = contour_side1s[frame_number]
        contour_side2 = contour_side2s[frame_number]
        skeleton = skeletons[frame_number]
        
        #%%
        edge_length = 8
        p1 = contour_side1[:-edge_length]
        p2 = contour_side1[edge_length:]
        points = contour_side1[edge_length/2:-edge_length/2]
        ang2 = np.arctan2(points[:,0] - p2[:,0], points[:,1] - p2[:,1])
        ang1 = np.arctan2(p1[:,0] - points[:,0], p1[:,1] - points[:,1]);
        angles = ang2-ang1
        
        for i in range(angles.size):
            if angles[i] > np.pi:
                angles[i] = angles[i] - 2*np.pi;
            elif angles[i] < -np.pi:
                angles[i] = angles[i] + 2*np.pi;
        angles = angles*180/np.pi;
        
        blurWin = np.full(edge_length, 1./edge_length);
        anglesb = np.convolve(angles, blurWin, 'same');
        #%%
        #the idea is that when the worm coils and there is an skeletons, it is
        #likely to be a cnonsequence of the head/tail protuding, therefore we can
        #use the head/tail withd to get a good ratio of the worm width
        
        #calculate head and tail width
        head_w = contour_width[ht_limits]
        tail_w = contour_width[-ht_limits]
        midbody_w = np.max(contour_width)
        
        '''
        % Does the worm more than double its width from the head/tail?
        % Note: if the worm coils, its width will grow to more than
        % double that at the end of the head.
        '''
        if midbody_w/head_w > thresh_ratio or \
        midbody_w/tail_w > thresh_ratio or max(head_w/tail_w, tail_w/head_w) > thresh_ratio:
            is_good_skel[frame_number] = 0
            continue
        
        
        #calculate the head and tail area (it is an approximation the limits are not super well defined, but it is enough for filtering)
        head_skel_lim = skeleton[np.newaxis, ht_limits]
        tail_skel_lim = skeleton[np.newaxis, -ht_limits]
        
        cnt_side1_ind_h, cnt_side2_ind_h = getPerpContourInd(skeleton, ht_limits, 
                                                             contour_side1, contour_side2,contour_width)
        cnt_side1_ind_t, cnt_side2_ind_t = getPerpContourInd(skeleton, -ht_limits, 
                                                             contour_side1, contour_side2,contour_width)
        
        if cnt_side1_ind_h>cnt_side1_ind_t or cnt_side2_ind_h>cnt_side2_ind_t:
            is_good_skel[frame_number] = 0
            continue
        #if cnt_side1_ind_h>cnt_side1_ind_t:
        #    cnt_side1_ind_h, cnt_side1_ind_t = cnt_side1_ind_t, cnt_side1_ind_h
        #if cnt_side2_ind_h>cnt_side2_ind_t:
        #    cnt_side2_ind_h, cnt_side2_ind_t = cnt_side2_ind_t, cnt_side2_ind_h
        
        
        cnt_head = np.concatenate((contour_side1[:cnt_side1_ind_h+1], head_skel_lim, 
                                   contour_side2[:cnt_side2_ind_h+1][::-1]))
        cnt_tail = np.concatenate((contour_side2[cnt_side2_ind_t:][::-1], tail_skel_lim, 
                                   contour_side1[cnt_side1_ind_t:]))
        
        
        area_head = calcArea(cnt_head)
        area_tail = calcArea(cnt_tail)
        
        '''% Is the tail too small (or the head too large)?
        % Note: the area of the head and tail should be roughly the same size.
        % A 2-fold difference is huge!
        '''
        if area_tail == 0 or area_head==0 \
        or area_head/area_tail > thresh_ratio \
        or area_tail/area_head > thresh_ratio:
            is_good_skel[frame_number] = 0
            continue
        
        #calculate the area of the rest of the body
        cnt_rest = np.concatenate((head_skel_lim, contour_side1[cnt_side1_ind_h:cnt_side1_ind_t+1], 
                                   tail_skel_lim, contour_side2[cnt_side2_ind_h:cnt_side2_ind_t+1][::-1],
                                    head_skel_lim))
        area_rest = calcArea(cnt_rest)
        '''
        % Are the head and tail too small (or the body too large)?
        % Note: earlier, the head and tail were each chosen to be 4/24 = 1/6
        % the body length of the worm. The head and tail are roughly shaped
        % like rounded triangles with a convex taper. And, the width at their
        % ends is nearly the width at the center of the worm. Imagine they were
        % 2 triangles that, when combined, formed a rectangle similar to the
        % midsection of the worm. The area of this rectangle would be greater
        % than a 1/6 length portion from the midsection of the worm (the
        % maximum area per length in a worm is located at its midsection). The
        % combined area of the right and left sides is 4/6 of the worm.
        % Therefore, the combined area of the head and tail must be greater
        % than (1/6) / (4/6) = 1/4 the combined area of the left and right
        % sides.
        '''
        if area_rest/(area_head+area_tail) > thresh_ratio*3:
            is_good_skel[frame_number] = 0
            continue
        #%%
        if True:
            plt.figure()
            plt.plot(cnt_rest[:,0], cnt_rest[:,1], '.-')
            plt.plot(cnt_head[:,0], cnt_head[:,1], '.-')
            plt.plot(cnt_tail[:,0], cnt_tail[:,1], '.-')
            plt.plot(skeleton[:,0], skeleton[:,1], '.-')
            plt.axis('equal')
        #%%
    trajectories_data['is_good_skel'] = is_good_skel

saveModifiedTrajData(skeletons_file, trajectories_data)

