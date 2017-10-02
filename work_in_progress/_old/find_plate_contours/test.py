#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 13:20:22 2017

@author: ajaver
"""

from tierpsy.analysis.food_cnt.getFoodContour import getFoodContour

mask_file = '/Users/ajaver/Documents/GitHub/tierpsy-tracker/tests/data/_TEST/N2_worms10_CSCD438313_10_Set12_Pos5_Ch4_25072017_223347.hdf5'
skeletons_file = mask_file.replace('.hdf5', '') + '_skeletons.hdf5'
getFoodContour(mask_file, 
                skeletons_file,
                cnt_method = 'NN',
                solidity_th=0.98,
                batch_size = 100000,
                _is_debug = False
                )