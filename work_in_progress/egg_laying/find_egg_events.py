#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 11:11:22 2017

@author: ajaver
"""
import os
import pandas as pd
import numpy as np
import pymysql
from keras.models import load_model

from egg_trainset import _read_egg_events, _get_files
from tierpsy.analysis.ske_create.helperIterROI import generateMoviesROI
from tierpsy.analysis.ske_init.filterTrajectModel import shift_and_normalize

#model_trained_path = 'model_egg_laying3_epocs20_20170308_194818.h5'
model_trained_path = 'model_egg_laying_diff_20170309_193209.h5'
model = load_model(model_trained_path)
roi_size = model.input_shape[2]

egg_events = _read_egg_events()
#%%
conn = pymysql.connect(host='localhost', db = 'single_worm_db')
cur = conn.cursor()

vid_group = egg_events.groupby('base_name')


dd = vid_group.agg({'frame_number': np.min})['frame_number'].copy()
dd.sort()
base_name = dd.index[1]
#list(vid_group.groups.keys())[200]
eggs = vid_group.get_group(base_name)

masked_file, skel_file = _get_files(cur, base_name)

#%%
with pd.HDFStore(skel_file, 'r') as fid:
    trajectories_data = fid['/trajectories_data']

last_frame = trajectories_data['frame_number'].max()
egg_frames = eggs['frame_number'].values
true_eggs = np.zeros(last_frame + 1)
true_eggs[egg_frames] = 1

#%%
progress_prefix = 'Searching egg events'
ROIs_generator = generateMoviesROI(masked_file, 
                                   trajectories_data,
                                   roi_size =roi_size,
                                   progress_prefix = progress_prefix)

worm_buff = []
seq_dat = []
worm_probs = np.full((true_eggs.size, 2), np.nan)

prev_img = None
for worms_in_frame in ROIs_generator:
    assert len(worms_in_frame) == 1 #we are only dealing with one worm case
    for ind, roi_dat in worms_in_frame.items():
        row_data = trajectories_data.loc[ind]
        frame_number = row_data['frame_number']
        
        worm_img, roi_corner = roi_dat
        
        worm_img = worm_img.astype(np.float)
        
        if prev_img is not None:
            mask = (worm_img*prev_img) != 0
            worm_diff = np.zeros_like(worm_img)
            worm_diff[mask] = worm_img[mask] - prev_img[mask]
        
        
            if len(worm_buff) < 4:
                worm_buff.append(worm_diff)
            else:
                worm_buff = worm_buff[1:] + [worm_diff]
                worm_seq = np.array(worm_buff)
                seq_dat.append((frame_number-2, np.rollaxis(worm_seq, 0, 3)))
        
        prev_img = worm_img
#        if len(worm_buff) < 5:
#            worm_buff.append(worm_img)
#        else:
#            worm_buff = worm_buff[1:] + [worm_img]
#            worm_seq = shift_and_normalize(np.array(worm_buff))
#            seq_dat.append((frame_number-2, np.rollaxis(worm_seq, 0, 3)))
#    
    if (len(seq_dat)+1) % 100 == 0:
        frame_numbers, worm_seqs = zip(*seq_dat)
        
        worm_seqs = np.array(worm_seqs)
        worm_prob = model.predict_proba(worm_seqs, verbose=0)
        worm_probs[frame_numbers, :] = worm_prob
        seq_dat = []

if len(seq_dat) > 0:
    frame_numbers, worm_seqs = zip(*seq_dat)
    worm_seqs = np.array(worm_seqs)
    worm_prob = model.predict_proba(worm_seqs, verbose=0)
    worm_probs[frame_numbers, :] = worm_prob
    
#%%
import matplotlib.pylab as plt

plt.plot(worm_probs[:,1])
plt.plot(true_eggs, 'x')
#%%
#from tierpsy.analysis.ske_create.helperIterROI import getROIfromInd
#
#ind = 19653
#worm_seq = []
#for frame_number in range(ind-2, ind+3):
#    output = getROIfromInd(masked_file, trajectories_data, frame_number, 1, roi_size)
#    if output is not None:
#        row, worm_roi, roi_corner = output
#        worm_seq.append(worm_roi)

from egg_trainset import _plot_seq
_plot_seq(np.array(worm_seq))


#%%
#from egg_trainset import _plot_seq
#ind, = np.where(frame_numbers==egg_frames[0])
#
#worm_seq = np.rollaxis(worm_seqs[ind[0]], 2, -3)
#_plot_seq(worm_seq)

##%%
#from tierpsy.analysis.ske_create.helperIterROI import getROIfromInd
#worm_rois = []
#for frame_number in range(egg_frames[0]-2, egg_frames[0]+3):
#    output = getROIfromInd(masked_file, trajectories_data, frame_number, 1, roi_size)
#    row, worm_roi, roi_corner = output
#    worm_rois.append(worm_roi.astype(np.float))
#    
##%%
#worm_seq = shift_and_normalize(np.array([x.T for x in worm_rois]))
#_plot_seq(worm_seq)
##%%
#X = worm_seq[np.newaxis,:,:,:]
#X = np.rollaxis(X, 1, 4)
#worm_prob = model.predict_proba(X, verbose=0)
