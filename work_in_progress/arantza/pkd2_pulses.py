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

def get_light_off(light_on, half_win):
    light_off = ~light_on
    light_off = light_off & np.roll(light_off.copy(), half_win) & np.roll(light_off.copy(), -half_win)
    return light_off

def window_reversal(motion_modes, window_size):
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
    if not os.path.exists(mask_dir):
        mask_dir = results_dir
    
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


def find_pulse_rev_frac(feat_timeseries, index, window_size):
    w_ini = index
    w_fin = index+window_size
    good = (feat_timeseries['timestamp']>=w_ini) & (feat_timeseries['timestamp']<=w_fin)
    
    w_dat = feat_timeseries.loc[good]
    
    has_reversal = []
    for worm_index, g_dat in w_dat.groupby('worm_index'):
        has_reversal.append(np.any(g_dat['motion_modes'] == -1))
    
    rev_frac = np.mean(has_reversal)
    
    return rev_frac

def find_rev_frac(results_dir, base_name, expected_pulse_size_s, check_window_s):
    feat_file, mask_file = get_names(results_dir, base_name)
    
    fps = read_fps(feat_file)
    expected_pulse_size = fps*expected_pulse_size_s
    check_window = fps*check_window_s
    
    light_on = read_light_data(mask_file)
    with pd.HDFStore(feat_file, 'r') as fid:
        feat_timeseries = fid['/features_timeseries']
        
    feat_timeseries['timestamp'] = feat_timeseries['timestamp'].astype(np.int)
    #%%
    #find the indexes where the pulses start and end
    switches = np.diff(light_on.astype(np.int))
    turn_on, = np.where(switches==1)
    turn_off, = np.where(switches==-1)
    assert turn_on.size == turn_off.size
    #%%
    #find the reversal fraction for each pulse
    rev_fracs = []
    for ini, fin in zip(turn_on, turn_off):
        if fin-ini < expected_pulse_size/2:
            #the pulse is too short, let's ignore it
            continue
        
        before = find_pulse_rev_frac(feat_timeseries, ini-expected_pulse_size, check_window)
        centre = find_pulse_rev_frac(feat_timeseries, ini, check_window)
        after = find_pulse_rev_frac(feat_timeseries, fin+expected_pulse_size, check_window)

        
        rev_fracs.append((before, centre, after))
    return rev_fracs

def get_names(results_dir, base_name):
    feat_file = os.path.join(results_dir, base_name + '_features.hdf5')
    
    mask_dir = replace_subdir(results_dir, 'Results', 'MaskedVideos')
    if not os.path.exists(mask_dir):
        mask_dir = results_dir
    
    mask_file = os.path.join(mask_dir, base_name +'.hdf5')
    
    return feat_file, mask_file

if __name__ == '__main__':
    import os
    import seaborn as sns
    
    #results_dir = '/Volumes/behavgenom_archive$/Avelino/screening/David_Miller/Results/ATR_210417/'
    results_dir = '/Users/ajaver/OneDrive - Imperial College London/optogenetics/Arantza/Results/control_pulse'
    
    
    expected_pulse_size_s = 2
    check_window_s = 5
    
    
    fnames = [x for x in os.listdir(results_dir) if x.endswith('.hdf5')]
    base_names = set(map(remove_ext, fnames))
    
    probs = []
    for base_name in base_names:
        
        feat_file, mask_file = get_names(results_dir, base_name)
    
        fps = read_fps(feat_file)
        expected_pulse_size = fps*expected_pulse_size_s
        check_window = fps*check_window_s
        
        light_on = read_light_data(mask_file)
        with pd.HDFStore(feat_file, 'r') as fid:
            feat_timeseries = fid['/features_timeseries']
            
        feat_timeseries['timestamp'] = feat_timeseries['timestamp'].astype(np.int)
        
        for worm_index, dat in feat_timeseries.groupby('worm_index'):
            l_on = light_on[dat['timestamp']]
            
            if np.any(l_on):# and worm_index in [2, 5]:
                rr = (dat['timestamp'].min(), dat['timestamp'].max())
                
                #feat_names = dat.columns#[x for x in dat.columns if 'tail' in x]
                 
                #feat_names = [x for x in dat.columns if 'speed' in x]
                #feat_names = ['tail_width', 'tail_motion_direction', 'head_bend_mean', 'tail_bend_mean', 'tail_bend_sd', 'eigen_projection_6', 'length']
                #feat_names = ['tail_bend_mean', 'tail_bend_sd', 'eigen_projection_6', 'length', 'tail_width']
                
                feat_names = ['midbody_speed', 'tail_width']#'eigen_projection_6', 
                
                n_rows = 2
                for ii, feat in enumerate(feat_names):
                    if ii % n_rows == 0:
                        fig = plt.figure(figsize=(20,12))
                    
                    irow = (ii%n_rows)+1
                    plt.subplot(n_rows,1,irow)
                    plt.plot(dat['timestamp'], dat[feat])
                    yy = plt.ylim()
                    plt.plot(light_on*yy[1], 'o', markersize=3)
                    #plt.plot(dat['timestamp'],prob_rev*yy[0])
                    plt.xlim(rr)
                    plt.title(feat)
                    
                    plt.suptitle(worm_index)
                    if irow == n_rows or ii == len(feat_names)-1:
                        plt.xlabel('Frame Number')
                    
                if worm_index == 5:
                    fig.savefig('{}.png'.format(worm_index))
        
    #%%
#    data = [(exp_name, np.mean(frac_a), np.mean(frac_b))for exp_name, (frac_a, frac_b) in probs]
#    
#    #%%
#    
#    data = [[(exp_name, a,b) for a,b in zip(*dd)] for exp_name, dd in probs]
#    data = sum(data, [])
#    
#    #%%
#    data = sorted(data, key=lambda x : int(x[0].partition('-')[0][1:]))
#    df = pd.DataFrame(data=data, columns=['names', 'before', 'after'])
#    
#    plt.figure()
#    sns.boxplot(x="names", y="before", data=df)
#    sns.stripplot(x="names", y="before", data=df,
#              jitter=True, size=5,  linewidth=0, color="k")
#    plt.xlabel('Strains Numbers')
#    plt.ylabel('Change in Reversal Fraction Light OFF to ON')
#    plt.savefig('Change Fraction Before Pulse.png')
#    
#    #%%
#    
#    plt.figure()
#    sns.boxplot(x="names", y="after", data=df)
#    sns.stripplot(x="names", y="after", data=df,
#              jitter=True, size=5,  linewidth=0, color="k")
#    plt.xlabel('Strains Numbers')
#    plt.ylabel('Change in Reversal Fraction Light ON to OFF')
#    plt.savefig('Change Fraction After Pulse.png')
#    #%%
#    
#    for region_type in ['before', 'after']:
#        for frac_type in ['A7-B3', 'A9-B1']:
#            gg = df.groupby('names')
#            a = gg.get_group(frac_type)[region_type].values
#            b = gg.get_group('A10-B0')[region_type].values    
#            t, pprob = ttest_ind(a, b)
#            print(frac_type, region_type, pprob)
#    #%%
#    base_name = [x for x in base_names if 'A10_B0' in x][0]
#    feat_file, mask_file = get_names(results_dir, base_name)
#    
#    light_on = read_light_data(mask_file)
#    with pd.HDFStore(feat_file, 'r') as fid:
#        feat_timeseries = fid['/features_timeseries']
#    feat_timeseries['timestamp'] = feat_timeseries['timestamp'].astype(np.int)
#    #%%
#    fps = read_fps(feat_file)
#    
#    for worm_index, dat in feat_timeseries.groupby('worm_index'):
#        #print(worm_index)
#        if worm_index !=15:
#            continue
#        yy = dat['head_speed']
#        xx_i = dat['timestamp']
#        xx = xx_i/fps
#        
#        rr = (np.min(yy), np.max(yy))
#        pulse = light_on[xx_i]
#        pulse = pulse*(rr[1]-rr[0]) + rr[0]
#        
#        plt.figure(figsize=(12, 5))
#        plt.plot(xx, yy)
#        plt.plot(xx, pulse, 'o')
#        
#        plt.xlabel('Time (s)')
#        plt.ylabel('Midbody Speed (microns/s)')
#        #plt.savefig('Strain_A_Speed.png')
##%%
##    probs = []
##    for base_name in base_names:
##        print(base_name)
##        dat = get_reversal_probs(results_dir, base_name, window_size)
##        exp_name = '-'.join(base_name.split('_')[0:2])
##        probs.append((exp_name, dat))
#
###%%
##    data = []
##    for k, p in probs:
##        for t, val in p.items():
##            data.append((k, t, val))
##
##    data = sorted(data, key=lambda x : int(x[0].partition('-')[0][1:]))
##    
##    df = pd.DataFrame(data=data, columns=['names', 'type', 'P'])
##    
##    
##    plt.figure()
##    sns.stripplot(x="names", y="P", hue='type', data=df,
##              jitter=True, size=10,  linewidth=0) 
##    
##    #%%
##    data = [(k, (p['centre'] - p['after'])) for k,p in probs]
##    data = sorted(data, key=lambda x : int(x[0].partition('-')[0][1:]))
##    df = pd.DataFrame(data=data, columns=['exp', 'delP'])
##    plt.figure()
##    sns.stripplot(x="exp", y="delP", data=df,
##              jitter=True, size=5,  linewidth=0) 
##    #%%
##    from scipy.stats import ttest_ind
##    gg = df.groupby('exp')
##    
##    
##    a = gg.get_group('A7-B3')['delP'].values
##    b = gg.get_group('A9-B1')['delP'].values
##    t, pprob = ttest_ind(a, b)
#    #%%
##        l_on = light_on[dat['timestamp']]
##        l_off = light_off[dat['timestamp']]
##        
##        p_on = np.nanmean(prob_rev[l_on])
##        p_off = np.nanmean(prob_rev[l_off])
##        
##        rr = (dat['timestamp'].min(), dat['timestamp'].max())
##        
##        print((p_on, p_off, rr))
##        probs.append((p_on, p_off, rr))
##        
##        if p_on < 1:
##        
##            plt.figure()
##            plt.plot(dat['timestamp'], dat['midbody_speed'])
##            yy = plt.ylim()
##            plt.plot(light_on*yy[1])
##            plt.plot(dat['timestamp'],prob_rev*yy[0])
##            plt.xlim(rr)
#        
#    #%%
##        r_norm = dat['motion_modes'].copy()
##        r_norm[r_norm==1] = yy[1]
##        r_norm[r_norm==-1] = yy[0]
##        plt.plot(dat['timestamp'], r_norm, 'x')