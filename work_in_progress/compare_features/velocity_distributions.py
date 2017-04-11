#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 11:25:56 2017

@author: ajaver
"""
import os
import glob
import pandas as pd
import numpy as np
import tables
import matplotlib.pylab as plt

from tierpsy.analysis.feat_create.obtainFeaturesHelper import WormStats


def read_feat_events(feat_file):
    fid= tables.File(feat_file, 'r')
    
    features_events = {}
    node = fid.get_node('/features_events')
    for worn_n in node._v_children.keys():
        worm_node = fid.get_node('/features_events/' + worn_n)
        
        for feat in worm_node._v_children.keys():
            if not feat in features_events:
                features_events[feat] = {}
            dat = fid.get_node(worm_node._v_pathname, feat)[:]
            features_events[feat][worn_n] = dat
    
    def dict2array(dd):
        return np.concatenate([val for val in dd.values()])
    
    features_events = {feat:dict2array(val) for feat, val in features_events.items()}
    return features_events
#%%
#masks_dir = '/Volumes/SAMSUNG_USB/David_Miller/DM_unc-4_Adult_L4_060417/'
#results_dir = '/Volumes/SAMSUNG_USB/David_Miller/DM_unc-4_Adult_L4_060417/Results'

masks_dir = '/Volumes/behavgenom_archive$/Avelino/screening/David_Miller/MaskedVideos/DM_unc-4_Adult_L4_060417'
results_dir = masks_dir.replace('MaskedVideos', 'Results')

fnames = glob.glob(os.path.join(masks_dir, '*.hdf5'))


time_sets = {}
for fname in fnames:
    base_name = os.path.basename(fname).replace('.hdf5', '')
    time_str = base_name.rpartition('_')[-1]
    time_rounded = round(int(time_str)/100)
    time_sets[base_name] = time_rounded
    
#%%
feat_files = glob.glob(os.path.join(results_dir, '*_features.hdf5'))
features_data = {}
wstat = WormStats()
plate_stats = np.full(len(feat_files), np.nan, wstat.feat_avg_dtype)
for ii, feat_file in enumerate(feat_files):
    base_name = os.path.basename(feat_file).replace('_features.hdf5', '')
    print(base_name)
    with pd.HDFStore(feat_file, 'r') as fid:
        feat_timeseries = fid['/features_timeseries']
        feat_timeseries['motion_modes_f'] = np.nan
        
        for ind in feat_timeseries['worm_index'].unique():
            feats_worm = feat_timeseries[feat_timeseries['worm_index']==ind]
            motion_modes = feats_worm['motion_modes'].fillna(method='ffill')
            feat_timeseries['motion_modes_f'] = motion_modes
        
        dd = {x:feat_timeseries[x] for x in feat_timeseries}
        worm_features_dict = {**dd, **read_feat_events(feat_file)}
        features_data[base_name] = worm_features_dict
        
        plate_stats[ii] = wstat.getWormStats(worm_features_dict)
plate_stats = pd.DataFrame(plate_stats)

plate_stats['base_name'] =[os.path.basename(x).replace('_features.hdf5', '') for x in feat_files]
plate_stats['strain'] = [x.partition('_')[0] for x in plate_stats['base_name'].values]
plate_stats['time_set'] = [time_sets[x] for x in  plate_stats['base_name'].values]
#%%
ind_subplot = {key:ii+1 for ii,key in enumerate(sorted(set(time_sets.values())))}
strain_col = {'unc-4 (c2323)':'b', 'unc-4 (c2323);ceh-12':'r'}

plt.figure()
for ii, (bn, tab) in enumerate(features_data.items()):
    dat = tab['midbody_speed'].dropna()
    counts, edges = np.histogram(dat, 501, (-25,45))
    
    binsize = edges[1]-edges[0]
    xx = edges[:-1] + (binsize)/2
    
    yy = counts/dat.size#/binsize
    yy = np.cumsum(yy)
    
    isub = ind_subplot[time_sets[bn]]
    strain = bn.partition('_')[0]
    col = strain_col[strain]
    ax= plt.subplot(2,2, isub)
    plt.plot(xx, yy, col)
    
    time_str = str(time_sets[bn])
    plt.title(time_str)
    
    print(ii, isub, time_sets[bn])
    #ax.set_yscale('log')
    #strain = bn.partition('_')[0]
    #plt.title('{} {}'.format(time_str, strain))

#%%
#feat_stats = tab.quantile([0.05, 0.5, 0.95])
#feat_stats.append(tab.mean(skipna=True), ignore_index=True)
#%%
for ii, (bn, tab) in enumerate(features_data.items()):

    
    dat = features_data[bn]['forward_time']
    dat = dat[~np.isnan(dat)]
    counts, edges = np.histogram(dat, 25)
    binsize = edges[1]-edges[0]
    xx = edges[:-1] + (binsize)/2
    
    yy = counts/dat.size#/binsize
    
    #yy = np.cumsum(yy)
    isub = ind_subplot[time_sets[bn]]
    strain = bn.partition('_')[0]
    col = strain_col[strain]
    ax= plt.subplot(2,2, isub)
    plt.plot(xx, yy, col)
    
    time_str = str(time_sets[bn])
    plt.title(time_str)

#%%



#%%
#wstat = WormStats()
#
#       feat_stats = np.full(1, np.nan, dtype=self.feat_avg_dtype)
#
#        motion_mode = worm_features_dict['motion_modes'].values
#        for feat_name, feat_props in self.features_info.iterrows():
#            feat_obj = feat_props['feat_name_obj']
#
#            if feat_obj in worm_features._features:
#                tmp_data = worm_features._features[feat_obj].value
#            else:
#                tmp_data = None
#
#            if tmp_data is None:
#                feat_stats[feat_name] = np.nan
#
#            elif isinstance(tmp_data, (int, float)):
#                feat_stats[feat_name] = tmp_data
#
#            else:
#                feat_avg = self._featureStat(
#                    stat_func,
#                    tmp_data,
#                    feat_name,
#                    feat_props['is_signed'],
#                    feat_props['is_time_series'],
#                    motion_mode)
#                for feat_avg_name in feat_avg:
#                    feat_stats[feat_avg_name] = feat_avg[feat_avg_name]
#%%

#'forward_distance'
#'forward_time'
#'backward_distance'
#'backward_time'
#['backward_distance', 'backward_motion_distance_ratio', 'backward_motion_frequency', 'backward_motion_time_ratio', 'backward_time', 'inter_backward_distance', 'inter_backward_time']

