# -*- coding: utf-8 -*-
"""
Created on Wed May 18 18:22:12 2016

@author: ajaver
"""
import h5py
import numpy as np
import cv2
import os

from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from MWTracker.featuresAnalysis.obtainFeatures import getFPS

def createSmallVideo(mask_file_name, sample_video_name ='', time_factor = 12, 
                     size_factor = 4, expected_fps=30):
    #%%
    if not sample_video_name:
        sample_video_name = mask_file_name.replace('.hdf5', '_sample.avi')
    with h5py.File(mask_file_name, 'r') as fid:
        masks = fid['/mask']
        tot_frames, im_h, im_w = masks.shape
        im_h, im_w = im_h//size_factor, im_w//size_factor
        
        fps, is_default_timestamp = getFPS(mask_file_name, expected_fps)
        if '/timestamp/raw' in fid:
            timestamp_ind = fid['/timestamp/raw'][:]
        else:
            timestamp_ind = np.arange(tot_frames)
        
        
        tot_timestamps = int(timestamp_ind[-1])
        #%%
        #make sure to compensate for missing frames, so the video will have similar length.
        tt_vec = np.full(tot_timestamps+1, np.nan)
        current_frame = 0
        for ii in range(tot_timestamps+1):
            tt_vec[ii] = current_frame
            current_timestamp = timestamp_ind[current_frame]
            if current_timestamp <= ii:
                current_frame += 1
        #%%
        vid_writer = cv2.VideoWriter(sample_video_name, \
                            cv2.VideoWriter_fourcc(*'XVID'), fps/2, (im_w,im_h), isColor=False)
        
        for ii in range(0, tot_frames, time_factor*2):
            current_frame = tt_vec[ii]
            img = masks[current_frame]
            im_new = cv2.resize(img, (im_w,im_h))
            vid_writer.write(im_new)
        vid_writer.release()
    
#%%
if __name__ == '__main__':
    main_dir = '/Users/ajaver/Desktop/Videos/single_worm/global_sample_v2/'
    engine_v2 = create_engine(r'mysql+pymysql://ajaver:@localhost/single_worm_db_v2')
    Base = automap_base()
    Base.prepare(engine_v2, reflect=True)
    ProgressMask = Base.classes.progress_masks
    
    session_v2 = Session(engine_v2)
    
    all_mask_files = session_v2.query(ProgressMask.mask_file).all()
    
    for ii, dd in enumerate(all_mask_files[578:]):
        fname, = dd
        if fname is not None:
            print(ii, os.path.split(fname)[-1])
            createSmallVideo(fname)
            
        
    