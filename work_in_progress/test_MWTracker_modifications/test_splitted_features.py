# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 15:46:31 2016

@author: ajaver
"""

import matplotlib.pylab as plt
import pandas as pd
import numpy as np
import copy

import open_worm_analysis_toolbox as mv

from MWTracker.featuresAnalysis.obtainFeaturesHelper import WormStatsClass, WormFromTable
from MWTracker.featuresAnalysis.obtainFeatures import getGoodTrajIndexes, getFeatStats, getWormFeaturesFilt


features_file = '/Volumes/behavgenom_archive$/Avelino/GeckoVideo/Results/ControlSet_(N2-unc9-trp5)/Avelino_17112015_2100/CSTCTest_Ch6_18112015_075625_features.hdf5'
#features_file = '/Volumes/behavgenom_archive$/Avelino/GeckoVideo/Results/ControlSet_(N2-unc9-trp5)/Avelino_17112015_2100/CSTCTest_Ch1_17112015_215617_features.hdf5'
#features_file = '/Volumes/behavgenom_archive$/Avelino/GeckoVideo/Results/ControlSet_(N2-unc9-trp5)/Avelino_26112015_1930/CSTCTest_Ch5_27112015_130831_features.hdf5'
#features_file = '/Volumes/behavgenom_archive$/Avelino/GeckoVideo/Results/ControlSet_(N2-unc9-trp5)/Avelino_26112015_1930/CSTCTest_Ch6_27112015_130831_features.hdf5'
skeletons_file = features_file.replace('_features.', '_skeletons.')


##plt.plot(worm.skeleton[::10, :, 1].T, worm.skeleton[::10, :, 0].T)
#with pd.HDFStore(features_file, 'r') as fid:
#    features_means = fid['/features_means']
#
#
#good_traj_index, worm_index_str = getGoodTrajIndexes(skeletons_file)
#
#
#worm_index = good_traj_index[62]
#worm = WormFromTable(
#                skeletons_file,
#                worm_index,
#                use_skel_filter=True,
#                worm_index_str=worm_index_str,
#                micronsPerPixel=1,
#                fps=25,
#                smooth_window=-1)
#
#min_num_skel = 100
#wStats = WormStatsClass()
#


#dd = getWormFeaturesFilt(
#        skeletons_file,
#        features_file,
#        True,
#        False,
#        False,
#        25,
#        {'min_num_skel':100},
#        300)
#%%
with pd.HDFStore(features_file, 'r') as fid:
    features_means = fid['/features_means']
    features_means_split = fid['/features_means_split']
    