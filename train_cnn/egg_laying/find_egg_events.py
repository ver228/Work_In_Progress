#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 11:11:22 2017

@author: ajaver
"""
import os
import cv2
import pandas as pd
import numpy as np
import pymysql
import matplotlib.pylab as plt
import multiprocessing as mp

from keras.models import load_model

from egg_trainset import read_egg_events, get_files
from tierpsy.analysis.ske_create.helperIterROI import generateMoviesROI
from tierpsy.analysis.ske_init.filterTrajectModel import shift_and_normalize

from tierpsy.analysis.ske_create.helperIterROI import getROIfromInd


#%%
def get_possible_eggs(worm_probs, thresh ):
    inds = np.where(worm_probs[:,1]>thresh)[0]
    inds = inds[np.argsort(worm_probs[inds,1])][::-1]
    return inds

def plot_probs(worm_probs, thresh= 0.99, maker='v', col='b'):
    inds = get_possible_eggs(worm_probs, thresh)
    plt.plot(worm_probs[:,1], col)
    plt.plot(inds, worm_probs[inds,1], maker+col)
    
    return inds

def read_seq(masked_file, trajectories_data, ind, roi_size=-1):
    worm_seq = []
    for frame_number in range(ind-2, ind+3):
        output = getROIfromInd(masked_file, trajectories_data, frame_number, 1, roi_size)
        if output is not None:
            row, worm_roi, roi_corner = output
            worm_seq.append(worm_roi)
    return worm_seq

def plot_indexes(inds, roi_size=-1, n_rows = 5):

    
    for iseq, ind in enumerate(inds):
        worm_seq = read_seq(ind, roi_size)
    #for iseq, worm_seq in enumerate(worm_seqs[:5]):
        
        if iseq % n_rows == 0:
            plt.figure()
        
        irow = iseq % n_rows
        
        seq_size = len(worm_seq)
        #seq_size = worm_seq.shape[-1]
        
        for ii in range(seq_size):
            nn = ii+1 + seq_size*irow
            plt.subplot(n_rows, seq_size, nn)
            plt.imshow(worm_seq[ii], interpolation = 'none', cmap='gray')
            #plt.imshow(worm_seq[:, :, ii], interpolation = 'none', cmap='gray')
            plt.axis('off')
 

def get_egg_probabilities(masked_file, trajectories_data, model, roi_size = -1, progress_prefix = ''):
    #%%
    tot_frames = trajectories_data['frame_number'].max() + 1
    progress_prefix = progress_prefix + ' Searching egg events'
    ROIs_generator = generateMoviesROI(masked_file, 
                                       trajectories_data,
                                       roi_size =roi_size,
                                       progress_prefix = progress_prefix)
    roi_model = model.input_shape[1]
    buff_size = model.input_shape[-1]
    worm_buff = []
    seq_dat = []
    worm_probs = np.full((tot_frames, 2), np.nan)
    for worms_in_frame in ROIs_generator:
        assert len(worms_in_frame) == 1 #we are only dealing with one worm case
        for ind, roi_dat in worms_in_frame.items():
            row_data = trajectories_data.loc[ind]
            frame_number = row_data['frame_number']
            
            worm_img, roi_corner = roi_dat
            
            worm_img = worm_img.astype(np.float)
            worm_img = shift_and_normalize(worm_img)
                
            if worm_img.shape[0] != roi_model:
                worm_img = cv2.resize(worm_img, (roi_model,roi_model))
            
    
            if len(worm_buff) < buff_size:
                worm_buff.append(worm_img)
            else:
                worm_buff = worm_buff[1:] + [worm_img]
                worm_seq = np.array(worm_buff)
                #worm_seq = shift_and_normalize(worm_seq)
                seq_dat.append((frame_number-1, np.rollaxis(worm_seq, 0, 3)))
    
        if (len(seq_dat)+1) % 100 == 0:
            frame_numbers, worm_seq_batch = map(np.array, zip(*seq_dat))
            
            worm_prob_batch = model.predict(worm_seq_batch, verbose=0)
            worm_probs[frame_numbers, :] = worm_prob_batch
            seq_dat = []
            #return worm_probs
    
    if len(seq_dat) > 0:
        frame_numbers, worm_seqs = zip(*seq_dat)
        worm_seqs = np.array(worm_seqs)
        worm_prob = model.predict(worm_seqs, verbose=0)
        worm_probs[frame_numbers, :] = worm_prob
    #%%
    return worm_probs

def process_data(input_d):
    #%%
    base_name, eggs = input_d
    
        
    masked_file, skel_file = get_files(cur, base_name)
    
    with pd.HDFStore(skel_file, 'r') as fid:
        trajectories_data = fid['/trajectories_data']
    #trajectories_data = trajectories_data[trajectories_data['frame_number']< 1000]
    #%%
    worm_probs_resized = get_egg_probabilities(masked_file, 
                                               trajectories_data, 
                                               model_resized, 
                                               roi_size = -1,
                                               progress_prefix = base_name + ' model resized -> ' )
    #%%
    results = pd.DataFrame(worm_probs_resized, columns=['no_egg_prob', 'egg_prob'])
    results['true_events'] = np.zeros(results.shape[0])
    results.loc[eggs['frame_number'].values, 'true_events'] = 1
    #%%
    save_name = os.path.join(save_results_dir, base_name + '_eggs.csv')
    results.to_csv(save_name)
    
    return (base_name, results)

if __name__ == '__main__':
    #%%
    save_results_dir = './results'
    if not os.path.exists(save_results_dir):
        os.makedirs(save_results_dir)
    
    #%%
    #model_trained_path = 'model_egg_laying3_epocs20_20170308_194818.h5'
    #model_trained_path = 'model_egg_laying_diff_20170309_193209.h5'
    
    model_paths = '/Volumes/behavgenom_archive$/Avelino/neural_networks/eggs_tests/logs/main_20170328_180144/'
    model_path_resized = os.path.join(model_paths, 'main_resized-008-0.0891.h5')
    model_resized = load_model(model_path_resized)
    
    
    egg_events = read_egg_events()
    
    #process only files that has not been finished
    files_done = [x.replace('_eggs.csv', '') for x in os.listdir(save_results_dir) if x.endswith('_eggs.csv')]
    idone = egg_events.base_name.isin(files_done)
    egg_events = egg_events[~idone]
    
    conn = pymysql.connect(host='localhost', db = 'single_worm_db')
    cur = conn.cursor()
    
    vid_group = egg_events.groupby('base_name')
    #%%
    tot = len(vid_group)
    
    
    
    results = []
    gg = [x for x in vid_group]
    for ii, dd in enumerate(gg):
        try:
            print('{} of {}'.format(ii, tot))
            results.append(process_data(dd))
        except:
            pass
    