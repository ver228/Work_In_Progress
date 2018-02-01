# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 21:57:30 2015

@author: ajaver
"""
import matplotlib.pylab as plt
import h5py
import pandas as pd
import numpy as np
import os

from tierpsy.analysis.ske_create.getSkeletonsTables import getWormMask
from tierpsy.analysis.ske_create.helperIterROI import  getROIfromInd
from tierpsy.analysis.ske_create.segWormPython.mainSegworm import getSkeleton, contour2Skeleton, get_contour_angles


from tierpsy.analysis.ske_create.segWormPython.cython_files.segWorm_cython import circComputeChainCodeLengths


def cnt2angles(contour, ske_worm_segments):
    cnt_worm_segments = 2*ske_worm_segments
    cnt_chain_code_len = circComputeChainCodeLengths(contour)
    worm_seg_length = (cnt_chain_code_len[
                       0] + cnt_chain_code_len[-1]) / cnt_worm_segments
    
    #calculate contour angles
    hi_freq_output, low_freq_output = get_contour_angles(contour, cnt_chain_code_len, cnt_worm_segments, worm_seg_length)
    
    return hi_freq_output, low_freq_output



if __name__ == '__main__':
    #masked_file = '/Users/ajaver/OneDrive - Imperial College London/Tests/different_animals/maggots/MaskedVideos/hodor_ko_l3_control_siamac_1.hdf5'
    masked_file = '/home/ajaver@cscdom.csc.mrc.ac.uk/Downloads/CeleST submission small/demos/CeleST - demo with videos/samples/Results/Sample01/frame001.hdf5'
    skeletons_file = masked_file.replace('MaskedVideos', 'Results').replace('.hdf5', '_skeletons.hdf5')
    
    assert(os.path.exists(masked_file))
    assert(os.path.exists(skeletons_file))
    
    
    with pd.HDFStore(skeletons_file, 'r') as fid:
        trajectories_data = fid['/trajectories_data']
    
    strel_size = 5
    worm_index = 3
    
    ske_morph_segments = 24
    ske_head_angle_thresh = 60
    
    is_light_background = False
        
    tot = trajectories_data.loc[trajectories_data['worm_index_joined'] == worm_index, 'frame_number'].max()
    
    tot = min(tot, 10)
    for frame_number in range(1, tot, 1):
        row, worm_roi, roi_corner = getROIfromInd(masked_file, trajectories_data, frame_number, worm_index)
        
        worm_mask, contour, cnt_area = getWormMask(worm_roi, 
                                                    row['threshold'], 
                                                    strel_size, 
                                                    min_blob_area=row['area'] / 2,
                                                    is_light_background = is_light_background)
        
        #contour = worm_cnt.astype(np.float32)
        if contour.dtype != np.double:
            contour = contour.astype(np.double)
        
        
        
         
        hi_freq_output, low_freq_output = cnt2angles(contour, ske_morph_segments)
        
        #unpack data
        cnt_ang_hi_freq, maxima_hi_freq, maxima_hi_freq_ind, edge_len_hi_freq = hi_freq_output
        cnt_ang_low_freq, maxima_low_freq, maxima_low_freq_ind, edge_len_low_freq = low_freq_output
    
        
        output = getSkeleton(contour, 
                             num_segments=ske_morph_segments,  
                             head_angle_thresh=ske_head_angle_thresh)
        
        skeleton, ske_len, cnt_side1, cnt_side2, cnt_widths, cnt_area = output
        
        
        
        plt.figure()
        plt.subplot(2,1,1)
        plt.plot(cnt_ang_hi_freq)
        plt.plot(maxima_hi_freq_ind, maxima_hi_freq, 'o')
        plt.plot(cnt_ang_low_freq)
        plt.plot(maxima_low_freq_ind, maxima_low_freq, 'o')
    
        
        plt.subplot(2,1,2)
        plt.imshow(worm_mask, interpolation = 'none', cmap = 'gray')
        plt.xlim([0, worm_mask.shape[1]])
        plt.ylim([0, worm_mask.shape[0]])
        plt.grid('off')
        
        if skeleton.size>0:
            plt.plot(skeleton[:,0], skeleton[:,1])
        