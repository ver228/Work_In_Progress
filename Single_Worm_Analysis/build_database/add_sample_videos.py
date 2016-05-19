# -*- coding: utf-8 -*-
"""
Created on Wed May 18 18:22:12 2016

@author: ajaver
"""
import h5py
import numpy as np

from MWTracker.featuresAnalysis.obtainFeatures import getFPS

mask_file_name = '/Users/ajaver/Desktop/Videos/single_worm/goa-1/goa-1  (sa734)I on food R_2009_07_15__11_24__5.hdf5'


sample_video_name = mask_file_name.replace('.hdf5', '_sample.avi')

#cv2.VideoWriter(sample_video_name, \
#                    cv2.VideoWriter_fourcc('M','J','P','G'), fps, (row_data['roi_size'], row_data['roi_size']), isColor=False)


with h5py.File(mask_file_name, 'r') as fid:
    tot_frames, im_h, im_w = fid['/mask'].shape
    timestamp_ind = fid['/timestamp/raw'][:]
    fps, is_default_timestamp = getFPS(mask_file_name, np.nan)
    
    tot_timestamps = int(timestamp_ind[-1])
    
    tt_vec = np.full(tot_timestamps+1, np.nan)
    
    current_frame = 0
    for ii in range(tot_timestamps):
        tt_vec[ii] = current_frame
        current_timestamp = timestamp_ind[current_frame]
        if current_timestamp <= ii:
            current_frame += 1
    
    
    for ii in range(0, tot_timestamps, 16):
        current_frame = tt_vec[ii]
        img = fid['/mask'][current_frame]
        