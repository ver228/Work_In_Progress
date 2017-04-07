#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 17:13:12 2017

@author: ajaver
"""
import tables
import matplotlib.pylab as plt
import numpy as np
import pandas as pd





def _get_index(events_tot, val_frac, test_frac):
    rand_seed = 1337
    np.random.seed(rand_seed)  # for reproducibility
    
    inds = np.random.permutation(events_tot)
    test_size = np.round(events_tot*test_frac).astype(np.int)
    val_size = np.round(events_tot*val_frac).astype(np.int)
    
    
    all_ind = {'test' : inds[:test_size], 
               'val': inds[test_size:(val_size+test_size)],
               'train' : inds[(val_size+test_size):]}
    
    return all_ind

def add_train_indexes(sample_file, val_frac = 0.1, test_frac = 0.1):
    with pd.HDFStore(sample_file, 'r') as fid:
        egg_events = fid['/eggs_data']
        events_tot = len(egg_events)
    
    all_ind = _get_index(events_tot, val_frac, test_frac)
    with tables.File(sample_file, 'r+') as fid:
        if '/partitions' in fid:
            fid.remove_node('/partitions', recursive=True)
        
            
        grp = fid.create_group('/', 'partitions')
        for field, indexes in all_ind.items():
            fid.create_array(grp, field, obj=indexes)

   
if __name__ == '__main__':
    
    
    
    
    sample_file = 'samples.hdf5'
    
    add_train_indexes(sample_file)