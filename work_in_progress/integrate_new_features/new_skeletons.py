#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 18:31:24 2017

@author: ajaver
"""
import numpy as np
import pandas as pd
import tables

from tierpsy_features import SmoothedWorm
from tierpsy.analysis.feat_create.obtainFeaturesHelper import WormFromTable
from tierpsy.helper.params import read_fps


skel_smooth_window = 5
coords_smooth_window_s = 0.25
gap_to_interp_s = 0.25

base_file = '/Volumes/behavgenom_archive$/single_worm/finished/mutants/gpa-10(pk362)V@NL1147/food_OP50/XX/30m_wait/clockwise/gpa-10 (pk362)V on food L_2009_07_16__12_55__4'
base_file = '/Users/ajaver/Documents/GitHub/tierpsy-tracker/tests/data/WT2/Results/WT2'
is_WT2 = True

#base_file = '/Users/ajaver/Documents/GitHub/tierpsy-tracker/tests/data/AVI_VIDEOS/Results/AVI_VIDEOS_4'
#base_file = '/Users/ajaver/Documents/GitHub/tierpsy-tracker/tests/data/GECKO_VIDEOS/Results/GECKO_VIDEOS'
#is_WT2 = False

skeletons_file = base_file + '_skeletons.hdf5'


valid_fields = ['timestamp_raw', 'timestamp_time', 'worm_index_joined', 
                'skeleton_id', 'coord_x', 'coord_y', 'threshold', 'roi_size', 
                'area', 'frame_number', 'is_good_skel']

with pd.HDFStore(skeletons_file, 'r') as fid:
    trajectories_data = fid['/trajectories_data']
trajectories_data = trajectories_data[valid_fields]
trajectories_data.rename(columns = {'worm_index_joined' : 'worm_index', 
                                    'is_good_skel' : 'is_skeletonized'},
                                    inplace=True)
fps = read_fps(skeletons_file)

#%%
if trajectories_data['timestamp_raw'].isnull().all():
    trajectories_data['timestamp_raw'] = trajectories_data['frame_number']
    trajectories_data['timestamp_time'] = trajectories_data['frame_number']*fps

else:
    all_worm_data = []
    for worm_index, worm_data in trajectories_data.groupby('worm_index'):
        #%%
        worm_data = worm_data.dropna(subset = ['timestamp_raw'])
        worm_data = worm_data.drop_duplicates(subset = ['timestamp_raw'], 
                                  keep = 'first')
        worm_data['timestamp_raw'] = worm_data['timestamp_raw'].astype(np.int32)
        #%%
        if not (worm_data['frame_number'] == worm_data['timestamp_raw']).all():
            pass
        
        all_worm_data.append(worm_data)

    trajectories_data_n = pd.concat(all_worm_data)
#%% 

#%%
#
#coords_smooth_window = int(np.round(fps*coords_smooth_window_s))
#gap_to_interp = int(np.round(fps*gap_to_interp_s))
#
#if coords_smooth_window <= 3: #do not interpolate
#    coords_smooth_window = None
#    
#
#
#
#for worm_index, feat_data in trajectories_data.groupby('worm_index'):
#    worm = WormFromTable(skeletons_file,
#                        worm_index,
#                        worm_index_type = 'worm_index_joined'
#                        )
#
#    if is_WT2:
#        worm.correct_schafer_worm()
#        
#    wormN = SmoothedWorm(
#                 worm.skeleton, 
#                 worm.widths, 
#                 worm.ventral_contour, 
#                 worm.dorsal_contour,
#                 skel_smooth_window = skel_smooth_window,
#                 coords_smooth_window = coords_smooth_window,
#                 gap_to_interp = gap_to_interp
#                )
#    #%%
#    dlft_val = (-1, -1, -1,  -1, np.nan, np.nan, np.nan, np.nan, np.nan, -1, False)
#    valid_index = worm.timestamp - worm.first_frame
#    dat = np.array([dlft_val]*wormN.skeleton.shape[0], feat_data.dtypes)
#    worm_df = pd.DataFrame(dat, 
#                           columns = feat_data.columns,
#                           index = worm.timestamp)
#    #%%
#    good = feat_data['timestamp_raw'].isin(worm.timestamp)
#    u_timestamp, ind = np.unique(feat_data.loc[good, 'timestamp_raw'], 
#                                 return_index=True)
#    worm_df.loc[u_timestamp] = feat_data.values[ind]
#    #%%
#    
#    
    
    