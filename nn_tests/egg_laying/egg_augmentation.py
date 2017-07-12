#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 18:58:42 2017

@author: ajaver
"""

import os
import tables
import numpy as np
import pandas as pd
from math import ceil

if __name__ == '__main__':
    save_dir = '/Users/ajaver/OneDrive - Imperial College London/egg_laying'
    save_name = os.path.join(save_dir, 'train_data_eggs.hdf5')
    with pd.HDFStore(save_name, "r") as fid:
        coordinates_data = fid['/coordinates_data']
    coordinates_data_g = coordinates_data.groupby('seq_index')
    
    
    nn = 1501
    with tables.File(save_name, "r") as fid:
        seq_x = fid.get_node('/X')[nn]
        seq_y = fid.get_node('/Y')[nn]
    
    coords = coordinates_data_g.get_group(nn)
    
    
    #%%
    def _correct_range(ini, fin, n_size):
        less_n = ini<0
        if np.any(less_n):
            fin[less_n] -= ini[less_n]
            ini[less_n] = 0
        
        more_n = fin > n_size
        if np.any(more_n):
            ini[more_n] += n_size - fin[more_n]
            fin[more_n] = n_size
        return ini, fin
    
    rand_shift = 0
    rand_d_roi = 0
    
    j_ini = np.ceil(coords['coord_x'] - coords['roi_size']/2).values.astype(np.int)
    i_ini = np.ceil(coords['coord_y'] - coords['roi_size']/2).values.astype(np.int)
    r_size = coords['roi_size'].values.astype(np.int)
    assert np.all(r_size==r_size[0])
    r_size = r_size[0]
    
    j_ini += rand_shift
    i_ini += rand_shift
    r_size += rand_d_roi
    
    j_fin = j_ini + r_size
    i_fin = i_ini + r_size
    i_ini, i_fin = _correct_range(i_ini, i_fin, seq_x.shape[1])
    j_ini, j_fin = _correct_range(j_ini, j_fin, seq_x.shape[2])
    
    seq_x_r = np.zeros((seq_x.shape[0], r_size, r_size))
    for ns, (i_0,i_f, j_0, j_f) in enumerate(zip(i_ini, i_fin,j_ini, j_fin)):
        seq_x_r[ns] = seq_x[ns, i_0:i_f, j_0:j_f]
    
    
    #%%
    seq = seq_x_r
    
    import matplotlib.pylab as plt
    nseq = seq.shape[0]
    ncols = 4
    nrows = int(ceil(nseq/ncols))
    plt.figure(figsize=(2*ncols, 2*nrows))
    for ii in range(nseq):
        ind = ii +1 if ii <7 else ii +2
        
        ax = plt.subplot(nrows, ncols, ind)
        
        plt.imshow(seq[ii], cmap='gray', interpolation='none')
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([]) 