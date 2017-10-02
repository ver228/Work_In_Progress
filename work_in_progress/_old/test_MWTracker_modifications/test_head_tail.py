# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 04:03:11 2016

@author: ajaver
"""

import pandas as pd

from tierpsy.analysis.ske_orient.checkHeadOrientation import isWormHTSwitched, WormClass
from tierpsy.helper.params import TrackerParams, head_tail_defaults, read_fps


params = TrackerParams('filter_worms.json')


worm_index = 12
mask_file = '/Volumes/behavgenom_archive$/Avelino/screening/CeNDR/MaskedVideos/CeNDR_Set1_160517/BRC20067_worms10_food1-10_Set10_Pos5_Ch6_16052017_165021.hdf5'

skeletons_file = '/Volumes/behavgenom_archive$/Avelino/screening/CeNDR/Results/CeNDR_Set1_160517/BRC20067_worms10_food1-10_Set10_Pos5_Ch6_16052017_165021_skeletons.hdf5'

read_fps(skeletons_file)
#head_tail_param = params.head_tail_param
#head_tail_param = head_tail_defaults(skeletons_file, **head_tail_param)

#worm_data = WormClass(skeletons_file, worm_index)
#is_switched_skel, roll_std = isWormHTSwitched(worm_data.skeleton, **head_tail_param)