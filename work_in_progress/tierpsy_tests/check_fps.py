#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 12:40:17 2017

@author: ajaver
"""

import glob
from tierpsy.helper.params import read_fps

dname = '/Volumes/behavgenom_archive$/Ida/**/MaskedVideos/**/*.hdf5'
fnames = glob.glob(dname, recursive=True)

for f in fnames:
    try:
        fps = read_fps(f)
        print(fps)
    except:
        print('bad')
    