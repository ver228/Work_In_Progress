# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 15:30:11 2016

@author: worm_rig
"""

import os
import tables
import h5py
import time
import numpy as np
import json


from MWTracker.helperFunctions.timeCounterStr import timeCounterStr
from MWTracker.compressVideos.compressVideo import initMasksGroups
from MWTracker.helperFunctions.miscFun import print_flush

def getWormEnconderParams(fname):
    def numOrStr(x):
        x = x.strip()
        try:
            return int(x)
        except:
            return x
    with open(fname, 'r') as fid:  
        return {a.strip() : numOrStr(b) for a,b in 
          [x.split('=') for x in fid.read().split('\n') if x[0].isalpha()]}


plugin_param_file = 'wormencoder.ini'
assert os.path.exists(plugin_param_file)

plugin_params = getWormEnconderParams(plugin_param_file)

#original_file = 'D:\\Test_14102016\\Capture_Ch1_12102016_191719.hdf5'
#new_file = 'D:\\Test.hdf5'
original_file = '/Users/ajaver/Documents/Data/Test_14102016/Capture_Ch1_12102016_191719.hdf5'
new_file = '/Users/ajaver/Documents/Data/Test_14102016/Test.hdf5'   

expected_fps = 25


save_full_interval = plugin_params['UNMASKEDFRAMES']
buffer_size = plugin_params['MASK_RECALC_RATE']

mask_params = {'min_area' : plugin_params['MINBLOBSIZE'],
'max_area' : plugin_params['MAXBLOBSIZE'],
'thresh_C' : plugin_params['THRESHOLD_C'],
'thresh_block_size' : plugin_params['THRESHOLD_BLOCK_SIZE'],
'dilation_size' : plugin_params['DILATESIZE']}
 

base_name = new_file.rpartition('.')[0].rpartition(os.sep)[-1]
progressTime = timeCounterStr('Reformating Gecko plugin hdf5 video.')

with tables.File(original_file, 'r') as fid_old, \
    h5py.File(new_file, 'w') as fid_new:
    
    mask_old = fid_old.get_node('/mask')

    tot_frames, im_height, im_width = mask_old.shape

    
    mask_new, full_new =  initMasksGroups(fid_new, tot_frames, im_height, im_width, 
    expected_fps, True, save_full_interval)
    
    

    mask_new.attrs['plugin_params'] = json.dumps(plugin_params)
    
    img_buff_ini = mask_old[:buffer_size]
    full_new[0] = img_buff_ini[0]
    
    mask = mask_old[buffer_size] != 0
    mask_new[:buffer_size] = img_buff_ini*mask
    
    
    for frame in range(buffer_size, tot_frames):
        mask_new[frame] = mask_old[frame]
        
        if frame % 500 == 0:
            # calculate the progress and put it in a string
            progress_str = progressTime.getStr(frame)
            print_flush(base_name + ' ' + progress_str)
        
    #tag as finished reformatting
    mask_new.attrs['has_finished'] = 1


