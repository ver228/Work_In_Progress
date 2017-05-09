#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 17:51:53 2017

@author: ajaver
"""

import pandas as pd

ff = '/Users/ajaver/Documents/GitHub/tierpsy-tracker/tests/data/SCHAFER_LAB_SINGLE_WORM/Results/L4_19C_1_R_2015_06_24__16_40_14___features.hdf5'


data = {}
with pd.HDFStore(ff, 'r') as fid:
    for stat in ['P10th', 'P90th', 'medians', 'means']:
        data[stat] = fid['/features_summary/' + stat][:]

