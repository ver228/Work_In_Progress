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
import random
import matplotlib.pylab as plt
from skimage.transform import resize
from skimage.morphology import binary_erosion


from tensorflow.contrib import keras
K = keras.backend
Iterator = keras.preprocessing.image.Iterator
to_categorical =  keras.utils.to_categorical

import sys
sys.path.append('../find_food')
from augmentation import random_transform, transform_img

def crop_seq(seq_x, coords, rand_d_roi=0, rand_shift_x=0, rand_shift_y=0):
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
    
    r_size = coords['roi_size'].values.astype(np.int)
    assert np.all(r_size==r_size[0])
    r_size = r_size[0] + rand_d_roi
    
    
    j_ini = np.ceil(coords['coord_x'] - r_size/2).values.astype(np.int)
    i_ini = np.ceil(coords['coord_y'] - r_size/2).values.astype(np.int)
    
    j_ini += rand_shift_x
    i_ini += rand_shift_y
    
    
    j_fin = j_ini + r_size
    i_fin = i_ini + r_size
    i_ini, i_fin = _correct_range(i_ini, i_fin, seq_x.shape[0])
    j_ini, j_fin = _correct_range(j_ini, j_fin, seq_x.shape[1])
    
    seq_x_r = np.zeros((r_size, r_size, seq_x.shape[-1]))
    for ns, (i_0,i_f, j_0, j_f) in enumerate(zip(i_ini, i_fin,j_ini, j_fin)):
        seq_x_r[..., ns] = seq_x[i_0:i_f, j_0:j_f, ns]
        
    return seq_x_r

def plot_seq(seq):   
    nseq = seq.shape[-1]
    ncols = 4
    nrows = int(ceil(nseq/ncols))
    plt.figure(figsize=(2*ncols, 2*nrows))
    for ii in range(nseq):
        ind = ii +1 if ii <7 else ii +2
        ax = plt.subplot(nrows, ncols, ind)
        
        plt.imshow(seq[..., ii], cmap='gray', interpolation='none')
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])

def normalize_seq(seq):
    seq_e = seq>0
    for nn in range(seq.shape[-1]):
        seq_e[..., nn] -= binary_erosion(seq_e[..., nn])
    seq[seq>0] -= np.median(seq[seq_e])
    seq /= 255.
    
    return seq

class DirectoryImgGenerator(object):
    def __init__(self, file_name, y_weight, im_size):
        self.file_name = file_name
        self.y_weight = y_weight
        self.im_size = im_size
        
        with pd.HDFStore(self.file_name, "r") as fid:
            coordinates_data = fid['/coordinates_data']
            
        self.coordinates_data_g = coordinates_data.groupby('seq_index')
        self.tot = len(self.coordinates_data_g)
        
    def __len__(self): 
        return self.tot

    def __getitem__(self, i):
        return self._get(i)

    def __iter__(self):
        for fname in self.fnames:
            yield self._get(fname)
    
    def get_random(self):
        ii = random.randint(0, self.tot)
        return self._get(ii)
    
    def _get(self, nn):
        coords = self.coordinates_data_g.get_group(nn)
        with tables.File(self.file_name, "r") as fid:
            seq_x = fid.get_node('/X')[nn]
            seq_x = np.rollaxis(seq_x, 0, 3)
            seq_x = seq_x.astype(np.float32)
            
            
            seq_y = fid.get_node('/Y')[nn]
            seq_y = to_categorical(seq_y,2)
            
            seq_y[:,1] = seq_y[:,1]*y_weight
            
        
        seq_x_crop = crop_seq(seq_x, coords)
        seq_x_crop = normalize_seq(seq_x_crop)
        #frac_y = np.mean(fid.get_node('/Y'))
    
        seq_x_crop = resize(seq_x_crop, im_size, mode='reflect')
    
        return seq_x_crop, seq_y

def process_data(seq_x, seq_y, window_size = 4, transform_ags = {}):
    if len(transform_ags) > 0:
        h,w = seq_x.shape[:-1]
        transform = random_transform(h,w, **transform_ags)
        seq_x = transform_img(seq_x, *transform)
    
    #divide in smaller sequence in random order
    n_seq = seq_x.shape[-1]
    inds = range(n_seq - window_size)
    
    seq_x_d = [seq_x[:,:,i:i+window_size] for i in inds]
    seq_y_d = [seq_y[i:i+window_size] for i in inds]
    
    return seq_x_d, seq_y_d
    


class ImageMaskGenerator(Iterator):
    def __init__(self, 
                 generator,
                 transform_ags,
                 window_size = 4,
                 batch_size=32, 
                 epoch_size=None,
                 shuffle=True, 
                 seed=None
                 ):
       
        self.generator = generator
        
        if epoch_size is None:
            self.tot_samples = len(self.generator)
        else:
            self.tot_samples = epoch_size
        
        self.transform_ags = transform_ags
        self.batch_size = batch_size
        self.window_size = window_size
        
        #i really do not use this functionality i could reimplement it in the future
        super(ImageMaskGenerator, self).__init__(self.tot_samples, batch_size, shuffle, seed)

    def next(self):
        """
        # Returns
            The next batch.
        """
        
        seq_x, seq_y = self.generator.get_random()
        
        n_seq_t = seq_x.shape[-1] - window_size
        
        seq_x_t = []
        seq_y_t = []
        for ii in range(int(ceil(self.batch_size/n_seq_t))):
            xx, yy = process_data(seq_x, seq_y, window_size, transform_ags)
            seq_x_t += xx
            seq_y_t += yy
        
        
        #sample and only select batch_size samples
        D = list(zip(seq_x_t, seq_y_t))
        D = random.sample(D, self.batch_size)
        seq_x_t, seq_y_t = map(np.stack, zip(*D))
        
        
        return seq_x_t, seq_y_t

#%%
if __name__ == '__main__':
    save_dir = '/Users/ajaver/OneDrive - Imperial College London/egg_laying'
    save_name = os.path.join(save_dir, 'train_data_eggs.hdf5')
    y_weight = 10
    im_size = (128, 128)
    transform_ags = dict(
            rotation_range=90, 
             shift_range = 0.1,
             zoom_range = (0.75, 1.5),
             same_zoom = True,
             horizontal_flip=True,
             vertical_flip=True,
             elastic_alpha_range=500,
             elastic_sigma=25
             )
    window_size = 4
    
    
    gen_d = DirectoryImgGenerator(save_name, y_weight, im_size)
    
    gen = ImageMaskGenerator(gen_d,
                             transform_ags=transform_ags,
                             window_size=window_size,
                             batch_size=20)
    
    batch_x, batch_y = next(gen)
    
    #%% plot batch
    for nn in range(batch_x.shape[0]):
        seq_x = batch_x[nn]
        seq_y = batch_y[nn]
        ncols = seq_y.shape[0]
        
        plt.figure()
        for ii in range(ncols):
            plt.subplot(1, ncols, ii+1)
            plt.imshow(seq_x[...,ii])
            plt.title(seq_y[ii])
        
    
    