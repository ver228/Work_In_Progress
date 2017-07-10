#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 17:28:34 2017

@author: ajaver
"""
import os
import time
import numpy as np

from tensorflow.contrib import keras
TensorBoard = keras.callbacks.TensorBoard
ModelCheckpoint = keras.callbacks.ModelCheckpoint
K = keras.backend
Adam = keras.optimizers.Adam


#from keras.callbacks import TensorBoard, ModelCheckpoint
#from keras import backend as K
#from keras.optimizers import Adam

from augmentation import get_sizes, ImageMaskGenerator, DirectoryImgGenerator
from unet_build import get_unet_model_bn


def sparse_categorical_crossentropy(y_true, y_pred):
    return K.sparse_categorical_crossentropy(y_pred, y_true)


if __name__ == '__main__':
    main_dir = '/work/ajaver/food/train_set'
    SAVE_DIR = '/work/ajaver/food/results'
    
    #main_dir = '/Users/ajaver/OneDrive - Imperial College London/food/train_set'
    #SAVE_DIR = '/Users/ajaver/OneDrive - Imperial College London/food/results'
    
    #model_name = 'unet_norm'
    
    model = get_unet_model_bn()
    model_name = 'unet_norm_bn'
    
    epochs = 10000
    batch_size = 8
    saving_period = 250
    
    im_size = (512, 512)
    transform_ags = dict(rotation_range=90, 
         shift_range = 0.02,
         horizontal_flip=True,
         vertical_flip=True,
         elastic_alpha_range=200,
         elastic_sigma=10)
    
    log_dir = os.path.join(SAVE_DIR, 'logs', '%s_%s' % (model_name, time.strftime('%Y%m%d_%H%M%S')))
    pad=int(np.ceil(np.log10(epochs+1)))
    checkpoint_file = os.path.join(log_dir, '%s-{epoch:0%id}-{loss:.4f}.h5' % (model_name, pad))
    tb = TensorBoard(log_dir=log_dir)
    mcp = ModelCheckpoint(checkpoint_file, 
                          monitor='categorical_crossentropy',
                          verbose=1,  
                          mode='auto', 
                          period=saving_period)
    
    input_size, output_size, pad_size, tile_corners = get_sizes(im_size)
    
    bs = int(round(batch_size/len(tile_corners)))
    img_generator = ImageMaskGenerator(DirectoryImgGenerator(main_dir), 
                             transform_ags, 
                             pad_size,
                             input_size,
                             tile_corners,
                             batch_size=bs,
                             epoch_size = bs*20,
                             )
   
    model.compile(optimizer=Adam(lr=1e-5), 
                  loss='categorical_crossentropy', 
                  metrics=['categorical_crossentropy'])
    
    model.fit_generator(img_generator,
                        steps_per_epoch = round(img_generator.tot_samples/batch_size), 
                        epochs = epochs,
                        verbose = 1,
                        callbacks=[tb, mcp]) #some how they were breaking the mpc ? this crashes...
                        
    