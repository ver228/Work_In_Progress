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
from train_unet_gpu import w_pix_categorical_crossentropy



main_dir = '/Users/ajaver/OneDrive - Imperial College London/food/train_set/'

#model = load_model('unet_norm_bn-08249-0.0071.h5')
#model = load_model('unet_norm-09599-0.0098.h5')

#import tensorflow as tf
#keras.backend.set_learning_phase(tf.convert_to_tensor(0))
model_bn = load_model('unet_norm_w-11999-0.2499.h5', custom_objects={'w_pix_categorical_crossentropy': w_pix_categorical_crossentropy})
model_not_bn = load_model('unet_norm_w_not_bn-05749-0.7758.h5', custom_objects={'w_pix_categorical_crossentropy': w_pix_categorical_crossentropy})
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

def background_prediction(Xi, model_t):
    Y_pred = np.zeros(Xi.shape)
    for n_t in range(4):
        X = flip_d(Xi, n_t)
        
        im_size = X.shape 
        input_size, output_size, pad_size, tile_corners = get_sizes(im_size)
        x_crop = process_data(X, input_size, pad_size, tile_corners) 
        x_crop = np.concatenate(x_crop)
        y_pred = model_t.predict_on_batch(x_crop)
        Y_pred_s = np.zeros(X.shape)
        N_s = np.zeros(X.shape)
        for (i,j), yy in zip(tile_corners, y_pred):
            Y_pred_s[i:i+output_size, j:j+output_size] += yy[:,:,0]
            N_s[i:i+output_size, j:j+output_size] += 1
        Y_pred += flip_d(Y_pred_s/N_s, n_t)
    return Y_pred
    
fnames = glob.glob(os.path.join(main_dir, 'X_*'))


for ivid, fname in enumerate(random.sample(fnames,1)):
    print(ivid)
    Xi = imread(fname)
    Y_pred_bn = background_prediction(Xi, model_bn)
    Y_pred_not_bn = background_prediction(Xi, model_not_bn)
    #%%
    plt.figure()
    plt.subplot(1,3,1)
    plt.imshow(Xi, cmap='gray')
    plt.subplot(1,3,2)    
    plt.imshow(Y_pred_bn, interpolation='none')
    plt.subplot(1,3,3)    
    plt.imshow(Y_pred_not_bn, interpolation='none')
    
    #%%
    
    
    
    