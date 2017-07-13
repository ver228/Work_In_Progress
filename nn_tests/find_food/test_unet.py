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
from unet_build import w_pix_categorical_crossentropy

main_dir = '/Users/ajaver/OneDrive - Imperial College London/food/train_set/'

#model = load_model('unet_norm_bn-08249-0.0071.h5')
#model = load_model('unet_norm-09599-0.0098.h5')

#import tensorflow as tf
#keras.backend.set_learning_phase(tf.convert_to_tensor(0))
#model_bn = load_model('unet_norm_w-14249-0.1633.h5', custom_objects={'w_pix_categorical_crossentropy': w_pix_categorical_crossentropy})
#model_not_bn = load_model('unet_norm_w_not_bn-06499-0.6399.h5', custom_objects={'w_pix_categorical_crossentropy': w_pix_categorical_crossentropy})

#model1 = load_model('unet_norm_w-19999-0.1208.h5', custom_objects={'w_pix_categorical_crossentropy': w_pix_categorical_crossentropy})
#model2 = load_model('unet_norm_w_bn_bias-06249-0.1954.h5', custom_objects={'w_pix_categorical_crossentropy': w_pix_categorical_crossentropy})
#model_not_bn = load_model('unet_norm_w_not_bn-15999-0.2540.h5', custom_objects={'w_pix_categorical_crossentropy': w_pix_categorical_crossentropy})

models = [
        load_model('unet_norm_w_bn_no_bias-01249-0.4044.h5')#,
        #load_model('unet_norm_w-00499-1.5756.h5')
        ]

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

def background_prediction(Xi, model_t, n_tiles=4, im_size=None):
    Y_pred = np.zeros(Xi.shape)
    for n_t in range(4):
        X = flip_d(Xi, n_t)
        
        if im_size is None:
            im_size = X.shape 
        input_size, output_size, pad_size, tile_corners = get_sizes(im_size)
        x_crop = process_data(X, input_size, pad_size, tile_corners) 
        x_crop = np.concatenate(x_crop)
        y_pred = model_t.predict_on_batch(x_crop)
        Y_pred_s = np.zeros(X.shape)
        N_s = np.zeros(X.shape)
        for (i,j), yy in zip(tile_corners, y_pred):
            Y_pred_s[i:i+output_size, j:j+output_size] += yy[:,:,1]
            N_s[i:i+output_size, j:j+output_size] += 1
        Y_pred += flip_d(Y_pred_s/N_s, n_t)
    return Y_pred
    
if __name__ == '__main__':
    n_tiles=4
    im_size=None
    
    fnames = glob.glob(os.path.join(main_dir, 'X_*'))
    for ivid, fname in enumerate(random.sample(fnames,10)):
        print(ivid)
        Xi = imread(fname)
        
        
        Y_pred = []
        for mod in models:
            yy = background_prediction(Xi, 
                                      mod, 
                                      n_tiles=n_tiles,
                                      im_size=im_size
                                      )
            Y_pred.append(yy)
        
        #%%
        n_rows= len(Y_pred) + 1 
        
        plt.figure()
        plt.subplot(1,n_rows,1)
        plt.imshow(Xi, cmap='gray')
        
        for irow, yy in enumerate(Y_pred):
            plt.subplot(1, n_rows, irow+2)    
            plt.imshow(yy, interpolation='none')
        
    
        
    
    
    