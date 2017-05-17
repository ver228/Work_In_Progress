#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 15 15:29:24 2017

@author: ajaver
"""
import json
import matplotlib.pylab as plt
from tierpsy.helper.params import read_unit_conversions

feat_file = '/Users/ajaver/OneDrive - Imperial College London/Local_Videos/single_worm/global_sample_v3/883 RC301 on food R_2011_03_07__11_10_27___8___1_features.hdf5'
skel_file = feat_file.replace('features.hdf5', 'skeletons.hdf5')
wcon_file = feat_file.replace('_features.hdf5', '.wcon')

read_unit_conversions(skel_file)
read_unit_conversions(feat_file)

with open(wcon_file) as fid: 
    data = json.load(fid)  
tt = data['data'][0]['t']

plt.plot(tt)