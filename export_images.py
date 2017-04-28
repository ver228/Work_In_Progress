#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 18:36:12 2017

@author: ajaver
"""

import os
import tables
import cv2

fname = '/Volumes/behavgenom_archive$/Avelino/full_images/test_hdf5b_Ch2_07032017_221020.hdf5'
exp_dir = fname.rpartition('.')[0]
if not os.path.exists(exp_dir):
    os.makedirs(exp_dir)


with tables.File(fname, 'r') as fid:
    mask_g = fid.get_node('/mask')
    for frame_n in range(mask_g.shape[0]):
        img = mask_g[frame_n]
        
        img_name = os.path.join(exp_dir, '%03i.png' % frame_n)
        cv2.imwrite(img_name, img)
        