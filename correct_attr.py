#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 16:27:07 2017

@author: ajaver
"""
import tables
import glob

fnames = glob.glob('/Volumes/behavgenom_archive$/Avelino/screening/CeNDR/MaskedVideos/CeNDR_Exp_250417/*.hdf5')

for ii, fname in enumerate(fnames):
    with tables.File(fname, 'r+') as fid:
        print(ii)
        print(fid.get_node('/mask').attrs['is_light_background'])
        fid.get_node('/mask').attrs['is_light_background'] = 1
        print(fid.get_node('/mask').attrs['is_light_background'])
    