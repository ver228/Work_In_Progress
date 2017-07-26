#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 21:45:14 2017

@author: ajaver
"""
import os
import matplotlib.pylab as plt
import pandas as pd

import sys
sys.path.append("../find_food")


from skimage.io import imread
from skimage.transform import resize
import random
import numpy as np

import keras.backend as K

from augmentation import get_sizes, ImageMaskGenerator

class DirectoryImgGenerator(object):
    def __init__(self, 
                 main_dir, 
                 im_size=None, 
                 weight_params={}
                 ):
        
        self.main_dir = main_dir
        self.weight_params = weight_params
        self.im_size = im_size
        
        fnames = os.listdir(main_dir)
        fnames = [x for x in fnames if x.endswith('.bmp')]
        self.fnames = fnames
        
        
        
    def __len__(self): 
        return len(self.fnames)

    def __getitem__(self, i):
        return self._get(self.fnames[i])

    def __iter__(self):
        for fname in self.fnames:
            yield self._get(fname)
    
    def get_random(self):
        fname = random.choice(self.fnames)
        
        return self._get(fname)
    
    def _get(self, fname):
        print(fname)
        
        im_file = os.path.join(self.main_dir, fname) 
        csv_file = os.path.splitext(im_file)[0] + '_eggs.csv'
        
        X = imread(im_file)
        Yo = np.zeros_like(X)
        
        df = pd.read_csv(csv_file)
        inds = np.ravel_multi_index([df['y'].astype(np.int), df['x'].astype(np.int)], X.shape)
        Yo.flat[inds] = 1
        
        if self.im_size is not None:
            #resize refit image to be between 0-1
            X = resize(X, self.im_size, mode='reflect')*255
            Yo = resize(Yo, self.im_size, mode='reflect')>0
        
        
        Y = keras.utils.to_categorical(Yo, 2)
        Y = np.reshape(Y, (Yo.shape[0], Yo.shape[1], 2))
        
        
        def _normalize_weigths_by_class(_Y):
            #normalize the weights for the classes
            W_label = np.zeros(_Y.shape, K.floatx()) 
            lab_w = np.mean(_Y)
            
            dd = _Y>0
            W_label[dd] = 1/lab_w 
            W_label[~dd] = 1/(1-lab_w)
            return W_label
        
        
        
        W = _normalize_weigths_by_class(Yo)
            
        # I can add the weights directly to the predictions because 
        #keras uses y_true * log(y_pred) so y_true can be any number larger than 0
        #and
        # categorical_accuracy uses the maximum argument as the real prediction
        Y = Y*W[..., None]
            
            
        return X,Y

if __name__ == '__main__':
    transform_ags = dict(
            rotation_range=90, 
             shift_range = 0.1,
             zoom_range = (0.9, 1.5),
             horizontal_flip=True,
             vertical_flip=True,
             elastic_alpha_range=400,
             elastic_sigma=20,
             int_alpha=(0.5,2.25)
             )

    im_size = ((2048, 2048))
    n_tiles = 16
    
    main_dir = '/Users/ajaver/OneDrive - Imperial College London/egg_counter/example/'
    
    gen_d = DirectoryImgGenerator(main_dir)
    
    input_size, output_size, pad_size, tile_corners = get_sizes(im_size, n_tiles=n_tiles)
    
    
    gen = ImageMaskGenerator(gen_d, 
                             transform_ags, 
                             pad_size,
                             input_size,
                             tile_corners,
                             batch_size=16
                             )
#%%
    X,Y = gen_d.get_random()
    
    plt.figure()
    plt.subplot(1,2,1)
    plt.imshow(X, cmap='gray')
    plt.subplot(1,2,2)
    plt.imshow(Y[:,:,1])
    

    #%%
    for nn, (batch_x, batch_y) in enumerate(gen):
        if nn > 1:
            break
    
        for ii, (X,Y) in enumerate(zip(batch_x, batch_y)):
            #%%
            xx = np.squeeze(X)
            bot = np.min(xx)
            top = np.max(xx)
            
            ybot = np.min(Y)
            ytop = np.max(Y)
            yy_n = (Y-ybot)/(ytop-ybot)
            
            
            xi = (((xx-np.min(xx))*255)).astype(np.uint)
            xi = np.clip(xi, 0, 255)
            
            plt.figure(figsize=(12,4))
            plt.subplot(1,3,1)
            plt.imshow(xi, cmap='gray')
            
            plt.subplot(1,3,2)
            I_y = xx.copy()
            patch = (yy_n[:,:,0]*(top-bot))+bot
            I_y[gen.pad_size:-gen.pad_size, gen.pad_size:-gen.pad_size] = patch        
            plt.imshow(I_y)
            
            plt.subplot(1,3,3)
            
            I_w = xx.copy()
            patch = (yy_n[:,:,1]*(top-bot))+bot
            I_w[gen.pad_size:-gen.pad_size, gen.pad_size:-gen.pad_size] = patch        
            plt.imshow(I_w)
            