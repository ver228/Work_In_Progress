# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 14:44:55 2016

@author: worm_rig
"""

import os
import glob
import tables
import numpy as np

dilutions = {(0,1):1, (1,1):5, (2,1):20,
            (0,2):100, (1,2):1000, (2,2):10000}
disks = ['R:\\', 'S:\\', 'T:\\']

img_int = {'RT':np.full(6, np.nan), '37':np.full(6, np.nan)}

for diskN, disk in enumerate(disks):
    for nT, T in enumerate(['RT', '37']):
        dirname = os.path.join(disk, 'Videos', 'LawnExp_' + T + '_211016')
        fnames = glob.glob(os.path.join(dirname, '**', '*.hdf5'))
        for fname in fnames:
            nCh = int(fname.partition('_Ch')[-1].partition('_')[0])
            dilution = dilutions[(diskN, nCh)]
            try:
                with tables.File(fname, 'r') as fid:
                    img = fid.get_node('/mask')[0]
            except:
                continue
            
            img_int[T][diskN*2 + nCh-1] = np.median(img)
            


            
            