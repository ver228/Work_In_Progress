#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 22:40:18 2017

@author: ajaver
"""
import time
import os
import numpy as np

from egg_augmentation import DirectoryImgGenerator, ImageMaskGenerator
from egg_models import model_separable
from modified_mobilenet import MobileNetE, load_saved_model

from tensorflow.contrib import keras
load_model = keras.models.load_model
TensorBoard = keras.callbacks.TensorBoard
ModelCheckpoint = keras.callbacks.ModelCheckpoint
Adam = keras.optimizers.Adam

#SAVE_DIR = '/Users/ajaver/OneDrive - Imperial College London/egg_laying'
SAVE_DIR = '/work/ajaver/egg_laying'

def main(
        model_name = 'egg_mobilenet',
        roi_size = 128,
        window_size = 5,
        y_offset_left = 2,
        y_offset_right = 2,
        is_tiny = False,
        epochs = 20000,
        batch_size = 32,
        saving_period = 50,
        model_path = None
        ):

if __name__ == '__main__':
    
    assert window_size - y_offset_left - y_offset_right > 0
    im_size = (roi_size, roi_size)
    
    if model_path is not None:
        model = load_saved_model(model_path)
    else:
        if 'egg_mobilenet' in model_name:
            model = MobileNetE(roi_size, 
                               roi_size, 
                               window_size, 
                               y_offset_left = y_offset_left,
                               y_offset_right = y_offset_right,
                               nb_classes=2,
                               name = model_name
                               )
        elif 'separable' in model_name:
            #model_name='egg_separable_conv2d'
            #possibly broken
            y_offset_right = 0
            model = model_separable(window_size, roi_size, nb_classes=2, y_offset=y_offset_left)
        
    dd = (model_name,
        window_size,
        y_offset_left,
        y_offset_right,
        roi_size,
        batch_size
        )
    
    #add the training parameters to the model name
    model_name = '{}_W{}-{}-{}_R{}_B{}'.format(*dd)
    if is_tiny:
        model_name = 'T_' + model_name
    
    log_dir = os.path.join(SAVE_DIR, 'logs', '%s_%s' % (model_name, time.strftime('%Y%m%d_%H%M%S')))
    pad=int(np.ceil(np.log10(epochs+1)))
    checkpoint_file = os.path.join(log_dir, '%s-{epoch:0%id}-{loss:.4f}.h5' % (model_name, pad))
    tb = TensorBoard(log_dir=log_dir)
    mcp = ModelCheckpoint(checkpoint_file, 
                          monitor='loss',
                          verbose=1,  
                          mode='auto', 
                          period=saving_period)
    
    save_name = os.path.join(SAVE_DIR, 'train_data_eggs.hdf5')
    transform_ags = dict(
            rotation_range=90, 
             shift_range = 0.1,
             zoom_range = (0.75, 1.5),
             same_zoom = True,
             horizontal_flip=True,
             vertical_flip=True,
             elastic_alpha_range=400,
             elastic_sigma=20,
             int_alpha = (0.5,2.25)
             )
    
    gen_d_train = DirectoryImgGenerator(save_name, 
                                        im_size,
                                        y_weight = 20, 
                                        is_tiny = is_tiny
                                        )
    train_generator = ImageMaskGenerator(gen_d_train,
                             transform_ags=transform_ags,
                             window_size=window_size,
                             batch_size=batch_size,
                             y_offset_left=y_offset_left,
                             y_offset_right=y_offset_right
                             )
    
    gen_d_val = DirectoryImgGenerator(save_name, 
                                      im_size, 
                                      y_weight = 20, 
                                      is_train=False,
                                      is_tiny = is_tiny
                                      )
    val_generator = ImageMaskGenerator(gen_d_val,
                             transform_ags={},
                             window_size=window_size,
                             batch_size=batch_size,
                             y_offset_left=y_offset_left,
                             y_offset_right=y_offset_right
                             )
    
    model.compile(optimizer=Adam(lr=1e-4), 
                  loss='categorical_crossentropy',
                  metrics=['categorical_accuracy'])
    
    model.fit_generator(train_generator,
                        steps_per_epoch = train_generator.tot_samples, 
                        epochs = epochs,
                        validation_data = val_generator,
                        validation_steps = val_generator.tot_samples,
                        verbose = 1,
                        callbacks=[tb, mcp]
                        ) #some how they were breaking the mpc ? this crashes...
    


import fire
if __name__ == '__main__':
    fire.Fire(main)
    
    
    
