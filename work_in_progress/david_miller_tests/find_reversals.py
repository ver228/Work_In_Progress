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
#%%
def get_light_off(light_on, half_win):
    light_off = ~light_on
    light_off = light_off & np.roll(light_off.copy(), half_win) & np.roll(light_off.copy(), -half_win)
    return light_off

def window_reversal(motion_modes, window_size):
    
    #%%
    window_size = window_size if window_size % 2 == 1 else window_size + 1
    
    half_win = int(window_size/2)
    
    prob_rev = np.zeros(motion_modes.size, np.bool)
    is_backward = motion_modes==-1
    
    is_backward = np.pad(is_backward, (half_win,half_win), 'edge')
    for ii in range(prob_rev.size):
        #print(np.sum(is_backward[ii:ii+window_size]))
        prob_rev[ii] = np.any(is_backward[ii:ii+window_size])
        
    
    return prob_rev

def add_is_reversals(feat_timeseries, window_size):
    feat_timeseries['is_rev'] = np.nan
    for worm_index, dat in feat_timeseries.groupby('worm_index'):
        motion_modes = dat['motion_modes'].values
        feat_timeseries.loc[dat.index, 'is_rev'] = window_reversal(motion_modes, window_size)
    

def get_pulses_indexes(light_on, window_size):
    switches = np.diff(light_on.astype(np.int))
    turn_on, = np.where(switches==1)
    turn_off, = np.where(switches==-1)
    
    pulses = dict(
    centre = np.round((turn_on+turn_off)/2),
    before = turn_on - window_size*2,
    after = turn_off + window_size*2,
    )
    return pulses


#%%
def read_feat_events(feat_file):
    fid= tables.File(feat_file, 'r')
    
    features_events = {}
    node = fid.get_node('/features_events')
    for worm_n in node._v_children.keys():
        worm_node = fid.get_node('/features_events/' + worm_n)
        
        for feat in worm_node._v_children.keys():
            if not feat in features_events:
                features_events[feat] = {}
            dat = fid.get_node(worm_node._v_pathname, feat)[:]
            
            
            features_events[feat][worm_n] = dat
            
    #features_events = {feat:np.concatenate(val) for feat, val in features_events.items()}
    return features_events

def get_reversal_probs(results_dir, base_name, window_size):
    feat_file = os.path.join(results_dir, base_name + '_features.hdf5')
    
    mask_dir = replace_subdir(results_dir, 'Results', 'MaskedVideos')
    mask_file = os.path.join(mask_dir, base_name +'.hdf5')
    
    
    light_on = read_light_data(mask_file)
    pulses_indexes = get_pulses_indexes(light_on, window_size)
    
    with pd.HDFStore(feat_file, 'r') as fid:
        feat_timeseries = fid['/features_timeseries']
        
    feat_timeseries['timestamp'] = feat_timeseries['timestamp'].astype(np.int)
    add_is_reversals(feat_timeseries, window_size)
    
    probs = {}
    for key, good in pulses_indexes.items():
        dd = feat_timeseries['timestamp'].isin(good)
        probs[key] = feat_timeseries.loc[dd, 'is_rev'].mean()
    
    return probs

if __name__ == '__main__':
    import os
    import seaborn as sns
    
    results_dir = '/Volumes/behavgenom_archive$/Avelino/screening/David_Miller/Results/ATR_210417/'
    window_size = 250
    
    
    fnames = [x for x in os.listdir(results_dir) if x.endswith('.hdf5')]
    base_names = set(map(remove_ext, fnames))
    
    probs = []
    for base_name in base_names:
        print(base_name)
        dat = get_reversal_probs(results_dir, base_name, window_size)
        exp_name = '-'.join(base_name.split('_')[0:2])
        probs.append((exp_name, dat))

#%%
    data = []
    for k, p in probs:
        for t, val in p.items():
            data.append((k, t, val))

    data = sorted(data, key=lambda x : int(x[0].partition('-')[0][1:]))
    
    df = pd.DataFrame(data=data, columns=['names', 'type', 'P'])
    
    
    plt.figure()
    sns.stripplot(x="names", y="P", hue='type', data=df,
              jitter=True, size=10,  linewidth=0) 
    
    #%%
    data = [(k, (p['centre'] - p['before'])) for k,p in probs]
    data = sorted(data, key=lambda x : int(x[0].partition('-')[0][1:]))
    df = pd.DataFrame(data=data, columns=['exp', 'delP'])
    sns.stripplot(x="exp", y="delP", data=df,
              jitter=True, size=5,  linewidth=0) 
    
    
    #%%
#        l_on = light_on[dat['timestamp']]
#        l_off = light_off[dat['timestamp']]
#        
#        p_on = np.nanmean(prob_rev[l_on])
#        p_off = np.nanmean(prob_rev[l_off])
#        
#        rr = (dat['timestamp'].min(), dat['timestamp'].max())
#        
#        print((p_on, p_off, rr))
#        probs.append((p_on, p_off, rr))
#        
#        if p_on < 1:
#        
#            plt.figure()
#            plt.plot(dat['timestamp'], dat['midbody_speed'])
#            yy = plt.ylim()
#            plt.plot(light_on*yy[1])
#            plt.plot(dat['timestamp'],prob_rev*yy[0])
#            plt.xlim(rr)
        
    #%%
#        r_norm = dat['motion_modes'].copy()
#        r_norm[r_norm==1] = yy[1]
#        r_norm[r_norm==-1] = yy[0]
#        plt.plot(dat['timestamp'], r_norm, 'x')
#%%
def something(A):
    def _sm(x):
        return x+1
    return map(A, _sm)