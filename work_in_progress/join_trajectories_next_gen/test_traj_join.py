#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 16:34:43 2017

@author: ajaver
"""

import pandas as pd
import tables
import json
from tierpsy.analysis.traj_join.joinBlobsTrajectories import assignBlobTrajDF, joinGapsTrajectoriesDF
from fix_wrong_merges import  filter_table_by_area

skeletons_file = '/Users/ajaver/OneDrive - Imperial College London/optogenetics/ATR_210417/A10_B0_1.5x_25fps_Ch1_21042017_163235_skeletons.hdf5'

min_area_limit = 50
with pd.HDFStore(skeletons_file, 'r') as fid:
    trajectories_data = fid['/trajectories_data']
    
    trajectories_data['worm_index_auto'] = trajectories_data['worm_index_joined'].copy()
    #return trajectories_data
    trajectories_data = filter_table_by_area(trajectories_data, 
                                               worm_index_type = 'worm_index_auto',
                                               min_area_limit = min_area_limit
                                               )

    if '/blob_features' in fid:
        blob_features = fid['/blob_features']
        blob_features = blob_features.loc[trajectories_data.index]
        
        blob_features['frame_number'] = trajectories_data['frame_number']
        assert blob_features.shape[0] == trajectories_data.shape[0]

    plate_worms = fid['/plate_worms']

if False:
    rr = (1530, 1600)
    good = (plate_worms['frame_number']>rr[0]) & (plate_worms['frame_number']<rr[1])
    plate_worms = plate_worms[good]
    good = (trajectories_data['frame_number']>rr[0]) & (trajectories_data['frame_number']<rr[1])
    trajectories_data = trajectories_data[good]
    blob_features = blob_features[good]


with tables.File(skeletons_file, 'r') as fid:
    dd = fid.get_node('/provenance_tracking/TRAJ_JOIN').read()
    args_j = json.loads(json.loads(dd.decode())['func_arguments'])

#%%
#max_frame = 100;
#plate_worms = plate_worms[plate_worms['frame_number']<=max_frame]
#blob_features = blob_features[blob_features['frame_number']<=max_frame]
#trajectories_data = trajectories_data[trajectories_data['frame_number']<=max_frame]


#%%
#traj_ind_b = assignBlobTrajDF(plate_worms, 
#                            max_allowed_dist=args_j['max_allowed_dist'], 
#                            area_ratio_lim=args_j['area_ratio_lim']
#                            )

#%%
blob_features['worm_index_auto'] = assignBlobTrajDF(blob_features, 
                            max_allowed_dist=200, 
                            area_ratio_lim=args_j['area_ratio_lim']
                            )
#%%
worm_index_new = joinGapsTrajectoriesDF(blob_features, 
                           min_track_size=args_j['min_track_size'],
                           max_time_gap=args_j['max_time_gap'], 
                           area_ratio_lim=args_j['area_ratio_lim'],
                           worm_index_type='worm_index_auto')
    
blob_features['worm_index_auto'] =  worm_index_new
    


#%%
import matplotlib.pylab as plt

plt.figure()
#plt.plot(plate_worms['frame_number'], traj_ind_b, '.r')
plt.plot(trajectories_data['frame_number'], trajectories_data['worm_index_joined'], 'xr')
plt.plot(blob_features['frame_number'], blob_features['worm_index_auto'], '.b')

