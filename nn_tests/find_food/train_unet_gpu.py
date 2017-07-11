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

import tensorflow as tf
_EPSILON = 10e-8    
def _to_tensor(x, dtype):
    """Convert the input `x` to a tensor of type `dtype`.
    # Arguments
        x: An object to be converted (numpy array, list, tensors).
        dtype: The destination type.
    # Returns
        A tensor.
    """
    x = tf.convert_to_tensor(x)
    if x.dtype != dtype:
        x = tf.cast(x, dtype)
    return x
    

def w_pix_categorical_crossentropy(w_output, target, from_logits=False):
    """Categorical crossentropy between an output tensor 
    and a target tensor, using precalculated weights for each pixel.
    The weights should be in the last dimmension of the target array."""
    
    output = w_output[:,:,:,:-1]
    w_vec = w_output[:,:,:,-1][:,:,:,None]
    # scale preds so that the class probas of each sample sum to 1
    output /= tf.reduce_sum(output,
                axis=len(output.get_shape()) - 1,
                keep_dims=True)
    epsilon = _to_tensor(_EPSILON, output.dtype.base_dtype)
    output = tf.clip_by_value(output, epsilon, 1. - epsilon)
    
    return - tf.reduce_sum(w_vec * target * tf.log(output),
                           axis=len(output.get_shape()) - 1)


if __name__ == '__main__':
    #main_dir = '/work/ajaver/food/train_set'
    #SAVE_DIR = '/work/ajaver/food/results'
    
    main_dir = '/Users/ajaver/OneDrive - Imperial College London/food/train_set'
    SAVE_DIR = '/Users/ajaver/OneDrive - Imperial College London/food/results'
    
    model = get_unet_model_bn()
    model_name = 'unet_norm_w_bn_bias'
    
    epochs = 20000
    batch_size = 8
    saving_period = 250
    
    im_size = (512, 512)
    
    transform_ags = dict(
            rotation_range=90, 
             shift_range = 0.02,
             zoom_range = (0.9, 1.1),
             horizontal_flip=True,
             vertical_flip=True,
             elastic_alpha_range=400,
             elastic_sigma=20
             )
        
    weight_params = dict(
            sigma=2.5,
            weigth=20
            )
    
    log_dir = os.path.join(SAVE_DIR, 'logs', '%s_%s' % (model_name, time.strftime('%Y%m%d_%H%M%S')))
    pad=int(np.ceil(np.log10(epochs+1)))
    checkpoint_file = os.path.join(log_dir, '%s-{epoch:0%id}-{loss:.4f}.h5' % (model_name, pad))
    tb = TensorBoard(log_dir=log_dir)
    mcp = ModelCheckpoint(checkpoint_file, 
                          monitor='loss',
                          verbose=1,  
                          mode='auto', 
                          period=saving_period)
    
    input_size, output_size, pad_size, tile_corners = get_sizes(im_size)
    
    bs = int(round(batch_size/len(tile_corners)))
    img_generator = ImageMaskGenerator(DirectoryImgGenerator(main_dir, weight_params=weight_params), 
                             transform_ags, 
                             pad_size,
                             input_size,
                             tile_corners,
                             batch_size=bs,
                             epoch_size = bs*20,
                             )
   
    model.compile(optimizer=Adam(lr=1e-5), 
                  loss=w_pix_categorical_crossentropy)
    
    model.fit_generator(img_generator,
                        steps_per_epoch = round(img_generator.tot_samples/batch_size), 
                        epochs = epochs,
                        verbose = 1,
                        callbacks=[tb, mcp]) #some how they were breaking the mpc ? this crashes...
                        
