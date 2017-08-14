#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 16:11:21 2017

@author: ajaver
"""

import matplotlib.pylab as plt
import tables
import pandas as pd
import numpy as np

import statsmodels.stats.multitest as smm
from scipy.stats import ttest_ind

if __name__ == '__main__':
    all_data = pd.read_csv('regions_stats.csv')
    exp_df = pd.read_csv('exp_info.csv', index_col=0)
    #%% Just for debugging, if i do not find pulses it will show some graphs
    problem_files = exp_df.loc[~exp_df['has_valid_light'], 'mask_file'].values
    for mask_file in problem_files:
        with tables.File(mask_file) as fid:
            mean_intensity = fid.get_node('/mean_intensity')[:]
            
            plt.figure()
            plt.plot(mean_intensity)
    
    #%%
    #set true if you want to summarize 
    if False:
        #get the number of experiments (I am using lenght as proxy)
        #n_val_exp = all_data_r.groupby(['strain', 'exp_type']).agg('count')
        plt.figure()
        for ii, feat in enumerate(['video_duration', 'before', 'after', 'short_pulses', 'inter_pulses','long_pulse']):
            plt.subplot(2,3,ii+1)
            exp_df[feat].plot()
            plt.title(feat)
            
    #add the experiment information from exp_df dataframe 
    
    #let's get p-values of controls vs atr samples. 
    #This is a naive approach, probably it will be better to compare the "change" between regions
    #e.g. How much does the speed change before and during a pulse in the control with respect to the atr.
    all_data = all_data.join(exp_df[['strain', 'exp_type']], on='exp_id')
    
    exp_pvals = []
    for group, group_data in all_data.groupby(['strain', 'region', 'stat', 'feat']):
        good = group_data['exp_type'] == 'EtOH'
        ctr = group_data.loc[good, 'value'].values
        atr = group_data.loc[~good, 'value'].values
        
        
        _, p = ttest_ind(ctr, atr)
        
        exp_pvals.append(list(group) + [p])
    
    exp_pvals_df = pd.DataFrame(exp_pvals, columns = ['strain', 'region', 'stat', 'feat', 'p-values'])
    
    #%%
    
    exp_pvals_df = exp_pvals_df.dropna()
    exp_pvals_df['p-values_corr'] = np.nan
    for strain, g_data in exp_pvals_df.groupby('strain'):
        reject, pvals_corrected, alphacSidak, alphacBonf = \
            smm.multipletests(g_data['p-values'].values, method = 'fdr_tsbky')
        exp_pvals_df.loc[g_data.index, 'p-values_corr'] = pvals_corrected
        
    
#%%
    import seaborn as sns
    for strain, s_data in exp_pvals_df.groupby('strain'):
        print('{}\t{}\n'.format(strain, (s_data['p-values_corr']<=0.1).sum()))
        s_data = s_data.sort_values(['p-values_corr'])
        print(s_data.head(n=10))
        
        
        plt.figure()
        for ii, (irow, row) in enumerate(s_data.head(n=9).iterrows()):
            good = (all_data['region'] == row['region']) & \
            (all_data['stat'] == row['stat']) & \
            (all_data['feat'] == row['feat']) & \
            (all_data['strain'] == strain)
            
            plt.subplot(3,3,ii+1)
            dat = all_data[good]
            sns.stripplot(x='exp_type', y='value', data=dat, jitter=True)
            plt.title((row['feat'], row['stat']))
            
        plt.suptitle(strain)
        break

