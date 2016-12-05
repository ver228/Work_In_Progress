# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 04:03:11 2016

@author: ajaver
"""

import pandas as pd

from MWTracker.helperFunctions.tracker_param import tracker_param
from MWTracker.trackWorms.getWormTrajectories import getWormTrajectories
from MWTracker.trackWorms.correctTrajectories import correctTrajectories
from MWTracker.trackWorms.getSkeletonsTables import trajectories2Skeletons, _getSmoothTrajectories


masked_image_file = '/Users/ajaver/Desktop/Videos/tiffs/MaskedVideos/recording 8.1_X1.hdf5'

json_file = '/Users/ajaver/Documents/GitHub/Multiworm_Tracking/fluorescence/pharynx.json'

trajectories_file = '/Users/ajaver/Desktop/Videos/tiffs/Results/recording 8.1_X1_trajectories.hdf5'
skeletons_file = '/Users/ajaver/Desktop/Videos/tiffs/Results/recording 8.1_X1_skeletons.hdf5'
params = tracker_param(json_file)


#getWormTrajectories(masked_image_file,trajectories_file, **params.trajectories_param)
#correctTrajectories(trajectories_file, False, params.join_traj_param)

trajectories2Skeletons(masked_image_file,skeletons_file,trajectories_file,
                    **params.skeletons_param)

#%%
with pd.HDFStore(trajectories_file) as fid:
    plate_worms = fid['/plate_worms']
with pd.HDFStore(skeletons_file) as fid:
    trajectories_data = fid['/trajectories_data']

#%%
skel_file2 = '/Users/ajaver/Desktop/Videos/tiffs/Results/recording 8.1_X1_skeletons.hdf5'
with pd.HDFStore(skel_file2) as fid:
    trajectories_data2 = fid['/trajectories_data']

