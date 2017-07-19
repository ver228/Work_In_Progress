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
from modified_mobilenet import MobileNetE

from tensorflow.contrib import keras
TensorBoard = keras.callbacks.TensorBoard
ModelCheckpoint = keras.callbacks.ModelCheckpoint
Adam = keras.optimizers.Adam

if __name__ == '__main__':
    save_dir = '/Users/ajaver/OneDrive - Imperial College London/egg_laying'
    #save_dir = '/work/ajaver/egg_laying/'
    
    y_weight = 20
    roi_size = 128
    window_size = 5
    y_offset = 2
    im_size = (roi_size, roi_size)
    
    epochs = 20000
    batch_size = 32
    saving_period = 250
    
    #model_name='egg_separable_conv2d'
    #model = model_separable(window_size, roi_size, nb_classes=2, y_offset=y_offset)
    model_name='egg_mobilenet'
    model = model = MobileNetE(roi_size, roi_size, window_size, y_offset = y_offset,nb_classes=2)
    
    log_dir = os.path.join(save_dir, 'logs', '%s_%s' % (model_name, time.strftime('%Y%m%d_%H%M%S')))
    pad=int(np.ceil(np.log10(epochs+1)))
    checkpoint_file = os.path.join(log_dir, '%s-{epoch:0%id}-{loss:.4f}.h5' % (model_name, pad))
    tb = TensorBoard(log_dir=log_dir)
    mcp = ModelCheckpoint(checkpoint_file, 
                          monitor='loss',
                          verbose=1,  
                          mode='auto', 
                          period=saving_period)
    
    save_name = os.path.join(save_dir, 'train_data_eggs.hdf5')
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
    
    gen_d_train = DirectoryImgGenerator(save_name, y_weight, im_size)
    train_generator = ImageMaskGenerator(gen_d_train,
                             transform_ags=transform_ags,
                             window_size=window_size,
                             batch_size=batch_size,
                             y_offset=y_offset
                             )
    
    gen_d_val = DirectoryImgGenerator(save_name, y_weight, im_size, set_type='val')
    val_generator = ImageMaskGenerator(gen_d_val,
                             transform_ags={},
                             window_size=window_size,
                             batch_size=batch_size,
                             y_offset=y_offset
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
    