#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 13:57:07 2017

@author: ajaver
"""

import os
import glob
import pandas as pd

from find_pulses import read_light_data

if __name__ == '__main__':
    mask_dir = '/Volumes/behavgenom_archive$/Lidia/MaskedVideos'
    
    fnames = glob.glob(os.path.join(mask_dir, '**', '*.hdf5'), recursive=True)



    data = []
    for fname in fnames:
        day_n = fname.split(os.sep)[-2].rpartition('-')[-1]
        base_name = os.path.basename(fname).replace('.hdf5', '')
        
        strain_n, _, dd = base_name.partition('-') 
        exp_type = dd.partition('_') [0]
        
        data.append((day_n, strain_n, exp_type, fname))
    
    df = pd.DataFrame(data, columns=['day', 'strain', 'exp_type', 'mask_file'])
    
    
    