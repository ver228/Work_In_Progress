#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 16:11:21 2017

@author: ajaver
"""

import matplotlib.pylab as plt
import tables
import pandas as pd
if __name__ == '__main__':
    all_data = pd.read_csv('regions_stats.csv')
    exp_df = pd.read_csv('exp_info.csv', index_col=0)
    
    problem_files = exp_df.loc[~exp_df['has_valid_light'], 'mask_file'].values
    for mask_file in problem_files:
        with tables.File(mask_file) as fid:
            mean_intensity = fid.get_node('/mean_intensity')[:]
            
            plt.figure()
            plt.plot(mean_intensity)
    
    
    
    if False:
        #get the number of experiments (I am using lenght as proxy)
        #n_val_exp = all_data_r.groupby(['strain', 'exp_type']).agg('count')
        plt.figure()
        for ii, feat in enumerate(['video_duration', 'before', 'after', 'short_pulses', 'inter_pulses','long_pulse']):
            plt.subplot(2,3,ii+1)
            exp_df[feat].plot()
            plt.title(feat)
    
    all_data = all_data.join(exp_df[['strain', 'exp_type']], on='exp_id')
    
    for group, group_data in all_data.groupby(['strain', 'region', 'stat', 'feat']):
        good = group_data['exp_type'] == 'EtOH'
        ctr = group_data.loc[good, 'value'].values
        atr = group_data.loc[~good, 'value'].values