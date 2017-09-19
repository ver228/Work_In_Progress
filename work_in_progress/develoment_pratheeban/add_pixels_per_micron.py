#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import glob
import tables

from tierpsy.helper.params import set_unit_conversions, read_unit_conversions
from tierpsy.helper.misc import remove_ext

'''
L1_Early, L1_Late, L2 - mag x2.0, pixelsPerMicron 0.363
L3 - mag x1.6, pixelsPerMicron 0.289
L4 - mag x1.25, pixelsPerMicron 0.224
New_Adult & Old_Adult - mag x1, pixelsPerMicron 0.178
'''

microns_per_pixel_s = {
    'L1_Early': 1/0.363,
    'L1_Late' : 1/0.363,
    'L2' : 1/0.363,
    'L3' : 1/0.289,
    'L4' : 1/0.224,
    'New_Adult' : 1/0.178,
    'Old_Adult' : 1/0.178,
    }

root_dir = '/Volumes/behavgenom_archive$/Avelino/screening/Pratheeban_Development'


for stage, microns_per_pixel in microns_per_pixel_s.items():
    print(stage)    
    attr_params = dict(
            expected_fps = 25,
            microns_per_pixel = microns_per_pixel,
            is_light_background = 1
            )
    
    fnames = glob.glob(os.path.join(root_dir, stage, '**', '*.hdf5'))
    #filter to get only the maskfiles
    fnames = [x + '.hdf5' for x in set(remove_ext(x) for x in fnames)]
    for fname in fnames:
        read_unit_conversions(fname)
        with tables.File(fname, 'r+') as fid:
            mask_dataset = fid.get_node('/mask')
            full_dataset = fid.get_node("/full_data")
            
            set_unit_conversions(mask_dataset, **attr_params)
            set_unit_conversions(full_dataset, **attr_params)        
