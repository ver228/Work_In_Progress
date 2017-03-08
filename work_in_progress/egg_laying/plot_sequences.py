#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 18:47:24 2017

@author: ajaver
"""

import h5py
import matplotlib.pylab as plt
import numpy as np

sample_file = 'samples.hdf5'
with h5py.File(sample_file, 'r') as fid:
    events_tot, seq_size, w, h =  fid['/egg_laying'].shape
    
    
    plt.figure(figsize=(20,25))
    
    n_rows = 8
    events_ids = np.round(np.random.rand(n_rows)*events_tot).astype(np.int)
    
    for irow, event_id in enumerate(events_ids):
        
        
        seq_worm = fid['/egg_laying'][event_id]
        for ii, img in enumerate(seq_worm):
            nn = ii+1 + seq_size*irow
            plt.subplot(n_rows, seq_size, nn)
            plt.imshow(img, interpolation='none', cmap='gray')
            plt.axis('off')
            
        
