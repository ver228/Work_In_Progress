#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 15:27:15 2017

@author: ajaver
"""
import numpy as np
import pandas as pd
import time

#this might not work if the data does not fit in memory. It might require a more 
#intelligent processing if this is the case.
with pd.HDFStore('development_data.hdf5') as fid:
    features_timeseries = fid['/features_timeseries']
#%%
index_columns = ['worm_index', 'timestamp', 'skeleton_id', 'cohort_n', 'exp_n', 'fname_row', 'motion_modes']
features_columns = [x for x in features_timeseries.columns if x not in index_columns]
#%%
#The signs of most of the features are wrong since we do not have the ventral/dorsal orientation
#so let's take the absolute value
good_sign_feats = ['head_tip_speed', 'head_speed', 'midbody_speed', 'tail_speed', 'tail_tip_speed']

for feat in features_columns:
    if not feat in good_sign_feats:
        features_timeseries[feat] = features_timeseries[feat].abs()


#%%
#
def top10(x):
    return np.nanpercentile(x, 10)
def top90(x):
    return np.nanpercentile(x, 90)

fps = 25
window_seconds = 60*3

# I round data by minute to reduce the computational cost
features_timeseries['timestamp_m'] = (features_timeseries['timestamp']/window_seconds).round().astype(np.int)

frame_averages = {}
for key, dat in features_timeseries.groupby(('exp_n', 'cohort_n')):
    tic = time.time()
    print(key)
    
    cols = ['timestamp_m'] +  features_columns
    gg = dat[cols].groupby('timestamp_m')
    frame_averages[key] = gg.agg(['median', top10, top90])
    
    print(time.time()-tic)
#%%
import matplotlib.pylab as plt

strC = 'rbg'


for feat in ['midbody_speed']:#features_columns:
    for stat in ['median', 'top10', 'top90']:
        plt.figure()
        for key, df in frame_averages.items():
            exp_n, cohort_n = key
            xx = df.index*window_seconds/60
            yy = df[feat][stat]
            
            plt.subplot(2,1,exp_n)
            plt.plot(xx, yy, strC[cohort_n-1])
            plt.title('Exp {}'.format(exp_n))
            plt.xlim([0, 129])
            
            if exp_n == 2:
                plt.xlabel('time (minutes)')
            else:
                plt.gca().set_xticks([])
            
        plt.suptitle('{} {}'.format(stat, feat))
            
        
#%%


