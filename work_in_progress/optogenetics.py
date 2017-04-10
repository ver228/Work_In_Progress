#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 14:27:38 2017

@author: ajaver
"""

import numpy as np
import cv2

from tierpsy.analysis.compress.selectVideoReader import selectVideoReader
#%%
video_file = '/Volumes/behavgenom_archive$/Avelino/screening/David_Miller/ATR/filter/atr_Ch1_04042017_150500.hdf5'
#video_file = '/Volumes/behavgenom_archive$/Avelino/screening/David_Miller/ATR/filter/atr_Ch1_04042017_150500.mjpg'

vid = selectVideoReader(video_file)
video_stats = []
tot_frames = 0
while 1:
    ret, image = vid.read()
    if ret == 0:
        break
    
    tot_frames += 1
    print(tot_frames)
    
    if image.ndim == 3:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    dat = image[image>1]
    frame_stats = np.percentile(dat, [5, 50, 95])    
    video_stats.append(frame_stats)

video_stats = np.array(video_stats)

import matplotlib.pylab as plt
plt.plot(video_stats)


#%%


