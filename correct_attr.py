#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 16:27:07 2017

@author: ajaver
"""
import tables
import glob
import os
from tierpsy.helper.params import read_unit_conversions, set_unit_conversions, TrackerParams

#fnames = glob.glob('/Volumes/behavgenom_archive$/Avelino/screening/CeNDR/MaskedVideos/CeNDR_Exp_250417/*.hdf5')
#fnames = glob.glob('/Volumes/behavgenom_archive$/Avelino/screening/CeNDR/Results/**/*_features.hdf5')

dname = '/Volumes/behavgenom_archive$/Bertie/BertieRaw/MaskedVideos'
fnames = glob.glob(os.path.join(dname, '**', '*.hdf5'), recursive=True)

params = TrackerParams('filter_worms.json')

microns_per_pixel = params.p_dict['microns_per_pixel']
expected_fps = params.p_dict['expected_fps']
is_light_background = params.p_dict['is_light_background']
print(microns_per_pixel, expected_fps)


for ii, fname in enumerate(fnames):
    dd = read_unit_conversions(fname);
    if dd[0][-1] != 'seconds':
        print(ii, fname)
        with tables.File(fname, 'r+') as fid:
            group_to_save = fid.get_node('/mask')
            set_unit_conversions(group_to_save, expected_fps, microns_per_pixel, is_light_background)
            dd = read_unit_conversions(fname);    

    
        
        #print(fid.get_node('/features_timeseries').attrs['is_light_background'])
        # print(fid.get_node('/full_data').attrs['is_light_background'])
        # fid.get_node('/full_data').attrs['is_light_background'] = 1
        # print(fid.get_node('/full_data').attrs['is_light_background'])
    