#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 23:35:32 2017

@author: ajaver
"""
import os
import glob
import numpy as np
import matplotlib.pylab as plt
from skimage.io import imread
import random
from tensorflow.contrib import keras
load_model = keras.models.load_model

from augmentation import process_data, get_sizes


main_dir = '/Users/ajaver/OneDrive - Imperial College London/food/train_set/'

model = load_model('unet_norm_bn-08249-0.0071.h5')
#model = load_model('unet_norm-09599-0.0098.h5')
#%%
#%%
def flip_d(img_o, nn):
    if nn == 0:
        img = img_o[::-1, :]
    elif nn == 2:
        img = img_o[:, ::-1]
    elif nn == 3:
        img = img_o[::-1, ::-1]
    else:
        img = img_o
    
    return img
    
fnames = glob.glob(os.path.join(main_dir, 'X_*oig-8*'))


Y_p = []
for ivid, fname in enumerate(random.sample(fnames,10)):
    print(ivid)
    #%%
    Xi = imread(fname)
    Y_pred = np.zeros(Xi.shape)
    for n_t in range(4):
        X = flip_d(Xi, n_t)
        
        im_size = X.shape 
        input_size, output_size, pad_size, tile_corners = get_sizes(im_size)
        x_crop,_ = process_data(X,input_size, pad_size, tile_corners) 
        x_crop = np.concatenate(x_crop)
        y_pred = model.predict(x_crop)
        Y_pred_s = np.zeros(X.shape)
        N_s = np.zeros(X.shape)
        for (i,j), yy in zip(tile_corners, y_pred):
            Y_pred_s[i:i+output_size, j:j+output_size] += yy[:,:,0]
            N_s[i:i+output_size, j:j+output_size] += 1
        
        Y_pred += flip_d(Y_pred_s/N_s, n_t)
    
    Y_p.append(Y_pred)
    #%%
    plt.figure()
    plt.subplot(1,2,1)
    plt.imshow(Xi, cmap='gray')
    plt.subplot(1,2,2)    
    plt.imshow(Y_pred, interpolation='none')
    #%%
    
    
    
    