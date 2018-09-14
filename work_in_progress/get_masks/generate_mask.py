#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 10:25:30 2018

@author: avelinojaver
"""
import tables
import pandas as pd
import numpy as np
import matplotlib.pylab as plt

from tierpsy.analysis.ske_create.helperIterROI import getAllImgROI
from tierpsy.analysis.ske_create.getSkeletonsTables import getWormMask

if __name__ == '__main__':
    #CHANGE THIS TO THE CORRECT PATHs
    mask_file = '/Users/avelinojaver/OneDrive - Imperial College London/tierpsy_examples/aggregation/N2_1_Ch1_29062017_182108_comp3.hdf5'
    skel_file = mask_file.replace('.hdf5', '_skeletons.hdf5')

    #read the ROI data
    with pd.HDFStore(skel_file, 'r') as ske_file_id:
        trajectories_data = ske_file_id['/trajectories_data']
    
    #group the data by frame to easily be able to access to it
    traj_group_by_frame = trajectories_data.groupby('frame_number')
    
    #this is an example with only one frame but you can put a loop here
    frame_number = 50
        
    with tables.File(mask_file) as fid:
        #read the frame data
        img = fid.get_node('/mask')[frame_number]
        
        #read the data from all the worms in this frame
        frame_data = traj_group_by_frame.get_group(frame_number)
        
        #this functions crop all the ROIs of all the worms located in the image
        worms_in_frame = getAllImgROI(img, frame_data)
        
        #now i want to pass this into a binary mask with the segmentation
        labeled_mask = np.zeros_like(img, dtype=np.uint8)
        for iworm, (ind, (worm_img, roi_corner)) in enumerate(worms_in_frame.items()):
            
            row_data = trajectories_data.loc[ind]
            #here is where the ROI is really segmented. It uses threshold plus some morphology operations to clean a bit
            worm_mask, worm_cnt, cnt_area = getWormMask(worm_img, 
                                         row_data['threshold'], 
                                         strel_size=5,
                                         min_blob_area=row_data['area'] / 2, 
                                         is_light_background = True
                                         )
            #now I want to put the ROI mask into the larger labelled image
            xi,yi = roi_corner
            ss = worm_mask.shape[0]

            #here I am saving only the pixels located to the worm. 
            #This is safer than assigned the whole ROI in case of overlaping regions.
            m_roi = labeled_mask[yi:yi+ss, xi:xi+ss].view()
            m_roi[worm_mask>0] += iworm
        
    #visualize the results
    fig, axs = plt.subplots(1,2, sharex=True, sharey=True)
    axs[0].imshow(img)
    axs[1].imshow(labeled_mask)
    
    