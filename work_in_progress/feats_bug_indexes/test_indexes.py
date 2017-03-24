#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 18:53:48 2017

@author: ajaver
"""
import pandas as pd
import tables

from tierpsy.helper.tracker_param import tracker_param
from tierpsy.analysis.feat_create.obtainFeaturesHelper import WormFromTable
from tierpsy.analysis.feat_create.obtainFeatures import getWormFeaturesFilt

skeletons_file = './recording51.2r_X1_skeletons.hdf5'
features_file = skeletons_file.replace('_skeletons.hdf5', '_features.hdf5')

with pd.HDFStore(skeletons_file, 'r') as fid:
    trajectories_data = fid['/trajectories_data']

worm_indexes = trajectories_data['worm_index_joined'].unique()

worm = WormFromTable(skeletons_file,1)


param = tracker_param()
is_single_worm = False
use_manual_join = False
use_skel_filter = True
fps = 25

getWormFeaturesFilt(
    skeletons_file,
    features_file,
    use_skel_filter,
    use_manual_join,
    **param.feats_param)
