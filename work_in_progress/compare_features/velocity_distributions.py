#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 11:25:56 2017

@author: ajaver
"""
import os
import glob
import pandas as pd


masks_dir = '/Volumes/SAMSUNG_USB/David_Miller/DM_unc-4_Adult_L4_060417/'
fnames = glob.glob(os.path.join(masks_dir, '*.hdf5'))

time_sets = {}
for fname in fnames:
    base_name = os.path.basename(fname).replace('.hdf5', '')
    time_str = base_name.rpartition('_')[-1]
    time_rounded = round(int(time_str)/100)
    time_sets[base_name] = time_rounded


#%%
results_dir = '/Volumes/SAMSUNG_USB/David_Miller/DM_unc-4_Adult_L4_060417/Results'
feat_files = glob.glob(os.path.join(results_dir, '*_features.hdf5'))
features_timeseries = {}
for feat_file in feat_files:
    base_name = os.path.basename(feat_file).replace('_features.hdf5', '')
    print(base_name)
    with pd.HDFStore(feat_file, 'r') as fid:
        features_timeseries[base_name] = fid['/features_timeseries']
#%%
ind_subplot = {key:ii+1 for ii,key in enumerate(sorted(set(time_sets.values())))}
strain_col = {'unc-4 (c2323)':'b', 'unc-4 (c2323);ceh-12':'r'}


import numpy as np
import matplotlib.pylab as plt

plt.figure()
for bn, tab in features_timeseries.items():
    
    
    dat = tab['midbody_speed'].dropna()
    counts, edges = np.histogram(dat, 501, (-25,45))
    
    binsize = edges[1]-edges[0]
    xx = edges[:-1] + (binsize)/2
    
    yy = counts/dat.size/binsize
    
    
    
    isub = ind_subplot[time_sets[bn]]
    strain = bn.partition('_')[0]
    col = strain_col[strain]
    plt.subplot(2,2, isub)
    plt.plot(xx, yy, col)
    
    #time_str = str(time_sets[bn])
    #strain = bn.partition('_')[0]
    #plt.title('{} {}'.format(time_str, strain))

#%%
feat_stats = tab.quantile([0.05, 0.5, 0.95])
feat_stats.append(tab.mean(skipna=True), ignore_index=True)