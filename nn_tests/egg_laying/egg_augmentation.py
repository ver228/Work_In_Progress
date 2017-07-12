#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 18:58:42 2017

@author: ajaver
"""

import tables
import numpy as np
import pandas as pd
from math import ceil

if __name__ == '__main__':
    save_name = 'train_data_eggs.hdf5'
    with pd.HDFStore(save_name, "r") as fid:
        coordinates_data = fid['/coordinates_data']
    coordinates_data_g = coordinates_data.groupby('seq_index')
    
    nn = 10
    with tables.File(save_name, "r") as fid:
        seq_x = fid.get_node('/X')[nn]
        seq_y = fid.get_node('/Y')[nn]
    
    coords = coordinates_data_g.get_group(nn)
    
    #%%
    import matplotlib.pylab as plt
    nseq = seq_x.shape[0]
    
    #%%
    ncols = 4
    nrows = int(ceil(nseq/ncols))
    plt.figure(figsize=(2*ncols, 2*nrows))
    for ii in range(nseq):
        ind = ii +1 if ii <7 else ii +2
        
        ax = plt.subplot(nrows, ncols, ind)
        
        plt.imshow(seq_x[ii], cmap='gray', interpolation='none')
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([]) 
    #%%
    x_ini = np.ceil(coords['coord_x'] - coords['roi_size']/2).values.astype(np.int)
    y_ini = np.ceil(coords['coord_y'] - coords['roi_size']/2).values.astype(np.int)
    r_size = coords['roi_size'].values.astype(np.int)
    x_fin = x_ini + r_size
    y_fin = y_ini + r_size
    
    