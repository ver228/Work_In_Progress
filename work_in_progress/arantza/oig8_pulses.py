#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 10:44:56 2017

@author: ajaver
"""

import tables
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import os
import seaborn as sns
    
from scipy.stats import ttest_ind
from tierpsy.helper.misc import replace_subdir, remove_ext
from tierpsy.helper.params import read_fps

def read_light_data(mask_file):
    with tables.File(mask_file) as fid:
        mean_intensity = fid.get_node('/mean_intensity')[:]
    
    
    med = np.median(mean_intensity)
    mad = np.median(np.abs(mean_intensity-med))
    #the MAD is releated to sigma by the factor below as explained here:
    #wiki (https://en.wikipedia.org/wiki/Median_absolute_deviation#relation_to_standard_deviation)
    s = mad*1.4826 
    
    #... and since the median should be equal to the mean in a gaussian dist
    # we can use 6 sigma as our threshold
    light_on = mean_intensity >  med + s*6
    
    return light_on

def get_pulses_indexes(light_on, window_size):
    switches = np.diff(light_on.astype(np.int))
    turn_on, = np.where(switches==1)
    turn_off, = np.where(switches==-1)
    
    assert turn_on.size == turn_off.size
    
    delP = turn_off - turn_on
    
    good = delP>window_size/2
    
    
    return turn_on[good], turn_off[good]



def get_names(results_dir, base_name):
    feat_file = os.path.join(results_dir, base_name + '_features.hdf5')
    
    mask_dir = replace_subdir(results_dir, 'Results', 'MaskedVideos')
    if not os.path.exists(mask_dir):
        mask_dir = results_dir
    
    mask_file = os.path.join(mask_dir, base_name +'.hdf5')
    
    return feat_file, mask_file

def get_exp_group(base_name):
    for vt in ['control', 'herm', 'male']:
        if vt in base_name:
            return vt
    raise ValueError()
    
    
def _plot_region(feat_dat):
    fig = plt.figure()
    lab_order = ['before', 'during', 'after']
    sns.boxplot(x="region", 
                     y="val",
                     data=feat_dat, 
                     order=lab_order,
                     palette="binary")
    
    ax2 =sns.stripplot(x="region", 
                      y="val",
                      data=feat_dat, 
                      order=lab_order,
                      hue='base_name',
                      jitter=True)
    plt.ylabel('')
    plt.xlabel('')
    ax2.legend_.remove()
    plt.title(exp_group + ' ' + feat_q)
    
    return fig
    
if __name__ == '__main__':
    
    #results_dir = '/Volumes/behavgenom_archive$/Avelino/screening/David_Miller/Results/ATR_210417/'
    results_dir = '/Users/ajaver/OneDrive - Imperial College London/optogenetics/Arantza/Results/oig8'
    
    
    expected_pulse_size_s = 2
    check_window_s = 5
    
    base_window_s = 120
    
    fnames = [x for x in os.listdir(results_dir) if x.endswith('.hdf5')]
    base_names = set(map(remove_ext, fnames))
    
    results = []
    for base_name in sorted(base_names):
        
        print(base_name)
        feat_file, mask_file = get_names(results_dir, base_name)
        
        
        fps = read_fps(feat_file)
        expected_pulse_size = fps*expected_pulse_size_s
        check_window = fps*check_window_s
        base_window = fps*base_window_s
        
        light_on = read_light_data(mask_file)
        turn_on, turn_off = get_pulses_indexes(light_on, expected_pulse_size)
        assert turn_on.size == 1 and turn_off.size == 1
        turn_on = turn_on[0]
        turn_off = turn_off[0]
        
        feat_ranges = {
                'before':(turn_on-base_window, turn_on),
                'during':(turn_on, turn_off),
                'after':(turn_off, turn_off+base_window)
                }
        
        
        
        with pd.HDFStore(feat_file, 'r') as fid:
            feat_timeseries = fid['/features_timeseries']
        
        index_cols = ['worm_index', 'timestamp', 'skeleton_id', 'motion_modes']
        valid_cols = [x for x in feat_timeseries.columns if not x in index_cols]
            
        feat_timeseries['timestamp'] = feat_timeseries['timestamp'].astype(np.int)
        
        #%%
        exp_group = get_exp_group(base_name)
        
        for region, (ini, fin) in feat_ranges.items():
            good = (feat_timeseries['timestamp']>ini) & (feat_timeseries['timestamp']<fin)
            feats = feat_timeseries.loc[good, valid_cols]
            
            feats_q = feats.quantile([0.1, 0.5, 0.9])
            
            for feat, dat_q in feats_q.items():
                for q, val in dat_q.items():
                    feat_q = '{}_{}'.format(feat, int(round(q*100)))
                    
                    results.append((exp_group, base_name, region, feat_q, val))
            
    #%%
    results = pd.DataFrame(results, columns=['exp_group', 'base_name', 'region', 'feat_q', 'val'])
    #%%
    for exp_group, feat_exp in results.groupby('exp_group'):
        for feat_q, feat_dat in feat_exp.groupby('feat_q'):
            fig = _plot_region(feat_dat)
        break
    #%%
    
    
    #%%
    
#%%        
#        for worm_index, dat in feat_timeseries.groupby('worm_index'):
#            l_on = light_on[dat['timestamp']]
#            
#            
#            if not np.any(l_on):
#                continue# and worm_index in [2, 5]:
#            rr = (dat['timestamp'].min(), dat['timestamp'].max())
#            
#            #feat_names = dat.columns#[x for x in dat.columns if 'tail' in x]
#             
#            for ii, feat in enumerate(feat_names):
#                if ii % 5 == 0:
#                    plt.figure(figsize=(20,15))
#                
#                plt.subplot(5,1,(ii%5)+1)
#                plt.plot(dat['timestamp'], np.abs(dat[feat]))
#                yy = plt.ylim()
#                plt.plot(light_on*yy[1], 'o', markersize=3)
#                #plt.plot(dat['timestamp'],prob_rev*yy[0])
#                plt.xlim(rr)
#                plt.title(feat)
#                
#                plt.suptitle(worm_index)
            
       