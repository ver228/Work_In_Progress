#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 17:13:12 2017

@author: ajaver
"""

import matplotlib.pylab as plt
import numpy as np
import tables
import time
import os

from tensorflow.contrib import keras

layers = keras.layers
Input = keras.layers.Input
Conv2D = keras.layers.Conv2D
SeparableConv2D = keras.layers.SeparableConv2D
MaxPooling2D = keras.layers.MaxPooling2D
GlobalMaxPooling2D = keras.layers.GlobalMaxPooling2D

Dropout = keras.layers.Dropout
Dense = keras.layers.Dense
Reshape = keras.layers.Reshape 
Lambda = keras.layers.Lambda
Activation = keras.layers.Activation
BatchNormalization = keras.layers.BatchNormalization

concatenate = keras.layers.concatenate

Model = keras.models.Model

rand_seed = 1337
np.random.seed(rand_seed)  # for reproducibility
#%%

#%%
def _model_single_image(img_input, name):
    name += '_'
    
    x = Conv2D(32, (3, 3), padding='same', name=name+'conv0')(img_input)
    x = Activation('relu', name=name+'conv0_act')(x)
    x = MaxPooling2D((2, 2), name=name+'conv0_pool')(x)
    
    x = Conv2D(64, (3, 3), padding='same', name=name+'conv1a')(x)
    x = BatchNormalization(name=name+'conv1a_bn')(x)
    x = Activation('relu', name=name+'conv1a_act')(x)
    
    x = Conv2D(64, (3, 3), padding='same', name=name+'conv1b')(x)
    x = BatchNormalization(name=name+'conv1b_bn')(x)
    x = Activation('relu', name=name+'conv1b_act')(x)
    
    x = MaxPooling2D((2, 2), name=name+'conv1_pool')(x)
    
    x = Conv2D(128, (3, 3), padding='same', name=name+'conv2a')(x)
    x = BatchNormalization(name=name+'conv2a_bn')(x)
    x = Activation('relu', name=name+'conv2a_act')(x)
    
    x = Conv2D(128, (3, 3), padding='same', name=name+'conv2b')(x)
    x = BatchNormalization(name=name+'conv2b_bn')(x)
    x = Activation('relu', name=name+'conv2b_act')(x)
    
    
    x = MaxPooling2D((2, 2), name=name+'conv2_pool')(x)
    
    x = Conv2D(256, (3, 3), padding='same', name=name+'conv3a')(x)
    x = BatchNormalization(name=name+'conv3a_bn')(x)
    x = Activation('relu', name=name+'conv3a_act')(x)
    
    x = Conv2D(256, (3, 3), padding='same', name=name+'conv3b')(x)
    x = BatchNormalization(name=name+'conv3b_bn')(x)
    x = Activation('relu', name=name+'conv3b_act')(x)
    
    x = MaxPooling2D((2, 2), name=name+'conv3_pool')(x)
    
    x = Conv2D(512, (3, 3), padding='same', name=name+'conv4a')(x)
    x = BatchNormalization(name=name+'conv4a_bn')(x)
    x = Activation('relu', name=name+'conv4a_act')(x)
    
    x = Conv2D(512, (3, 3), padding='same', name=name+'conv4b')(x)
    x = BatchNormalization(name=name+'conv4b_bn')(x)
    x = Activation('relu', name=name+'conv4b_act')(x)
    
    x = GlobalMaxPooling2D(name=name+'avg_pool')(x)
    
    x = Dense(512, name=name+'dense0', activation='elu')(x)
    x = Dropout(0.4)(x)
    
    return x
    
#%%
def model_window(win_size, roi_size, nb_classes):
    win_size = 4
    roi_size = 100
    nb_classes = 2
    
    input_shape = (win_size, roi_size, roi_size,1)
    input_data = Input(shape=input_shape, name='input_all')
    
    in_layers = [Lambda(lambda x: x[:,ii,:,:], output_shape=(roi_size,roi_size,1))(input_data) for ii in range(win_size)]
    out_layers = [_model_single_image(in_layer, 'input' + str(ii)) for ii, in_layer in enumerate(in_layers)]
    x = layers.add(out_layers)
    x = Dense(512, name='joined0', activation='elu')(x)
    x = Dense(128, name='joined1', activation='elu')(x)
    x = Dense(nb_classes)(x)
    output = Activation('softmax')(x)
        
    model = Model(input_data, output)
    return model

def model_separable(win_size, roi_size, nb_classes, y_offset=0):
    name = 'separable_conv2d'
    
    input_shape = (roi_size, roi_size, win_size)
    input_data = Input(shape=input_shape, name='input_all')
    
    x = Conv2D(32, (3, 3), padding='same', name=name+'conv0')(input_data)
    x = Activation('relu', name=name+'conv0_act')(x)
    x = MaxPooling2D((2, 2), name=name+'conv0_pool')(x)
    
    x = SeparableConv2D(64, (3, 3), use_bias=False, name=name+'conv1a')(x)
    x = BatchNormalization(name=name+'conv1a_bn')(x)
    x = Activation('relu', name=name+'conv1a_act')(x)
    
    x = SeparableConv2D(64, (3, 3), padding='same', name=name+'conv1b')(x)
    x = BatchNormalization(name=name+'conv1b_bn')(x)
    x = Activation('relu', name=name+'conv1b_act')(x)
    
    x = MaxPooling2D((2, 2), name=name+'conv1_pool')(x)
    
    x = SeparableConv2D(128, (3, 3), padding='same', name=name+'conv2a')(x)
    x = BatchNormalization(name=name+'conv2a_bn')(x)
    x = Activation('relu', name=name+'conv2a_act')(x)
    
    x = SeparableConv2D(128, (3, 3), padding='same', name=name+'conv2b')(x)
    x = BatchNormalization(name=name+'conv2b_bn')(x)
    x = Activation('relu', name=name+'conv2b_act')(x)
    
    
    x = MaxPooling2D((2, 2), name=name+'conv2_pool')(x)
    
    x = SeparableConv2D(256, (3, 3), padding='same', name=name+'conv3a')(x)
    x = BatchNormalization(name=name+'conv3a_bn')(x)
    x = Activation('relu', name=name+'conv3a_act')(x)
    
    x = SeparableConv2D(256, (3, 3), padding='same', name=name+'conv3b')(x)
    x = BatchNormalization(name=name+'conv3b_bn')(x)
    x = Activation('relu', name=name+'conv3b_act')(x)
    
    x = MaxPooling2D((2, 2), name=name+'conv3_pool')(x)
    
    x = SeparableConv2D(512, (3, 3), padding='same', name=name+'conv4a')(x)
    x = BatchNormalization(name=name+'conv4a_bn')(x)
    x = Activation('relu', name=name+'conv4a_act')(x)
    
    x = SeparableConv2D(512, (3, 3), padding='same', name=name+'conv4b')(x)
    x = BatchNormalization(name=name+'conv4b_bn')(x)
    x = Activation('relu', name=name+'conv4b_act')(x)
    
    x = GlobalMaxPooling2D(name=name+'avg_pool')(x)
    
    x = Dense(1024, name=name+'dense0', activation='elu')(x)
    x = Dropout(0.4)(x)
    
    x = Dense(1024, name=name+'dense1', activation='elu')(x)
    x = Dropout(0.4)(x)
    
    x = Dense((win_size-y_offset)*nb_classes)(x)
    x = Reshape(((win_size-y_offset), nb_classes))(x)
    
    output = Activation('softmax')(x)
        
    model = Model(input_data, output)
    return model


#def model_separable_large(win_size, roi_size, nb_classes, y_offset=0):
#    name = 'separable_conv2d'
#    
#    input_shape = (roi_size, roi_size, win_size)
#    input_data = Input(shape=input_shape, name='input_all')
#    
#    x = Conv2D(32, (3, 3), padding='same', name=name+'conv0')(input_data)
#    x = Activation('relu', name=name+'conv0_act')(x)
#    x = MaxPooling2D((2, 2), name=name+'conv0_pool')(x)
#    
#    x = SeparableConv2D(64, (3, 3), use_bias=False, name=name+'conv1a')(x)
#    x = BatchNormalization(name=name+'conv1a_bn')(x)
#    x = Activation('relu', name=name+'conv1a_act')(x)
#    
#    x = SeparableConv2D(64, (3, 3), padding='same', name=name+'conv1b')(x)
#    x = BatchNormalization(name=name+'conv1b_bn')(x)
#    x = Activation('relu', name=name+'conv1b_act')(x)
#    
#    x = MaxPooling2D((2, 2), name=name+'conv1_pool')(x)
#    
#    x = SeparableConv2D(128, (3, 3), padding='same', name=name+'conv2a')(x)
#    x = BatchNormalization(name=name+'conv2a_bn')(x)
#    x = Activation('relu', name=name+'conv2a_act')(x)
#    
#    x = SeparableConv2D(128, (3, 3), padding='same', name=name+'conv2b')(x)
#    x = BatchNormalization(name=name+'conv2b_bn')(x)
#    x = Activation('relu', name=name+'conv2b_act')(x)
#    
#    
#    x = MaxPooling2D((2, 2), name=name+'conv2_pool')(x)
#    
#    x = SeparableConv2D(256, (3, 3), padding='same', name=name+'conv3a')(x)
#    x = BatchNormalization(name=name+'conv3a_bn')(x)
#    x = Activation('relu', name=name+'conv3a_act')(x)
#    
#    x = SeparableConv2D(256, (3, 3), padding='same', name=name+'conv3b')(x)
#    x = BatchNormalization(name=name+'conv3b_bn')(x)
#    x = Activation('relu', name=name+'conv3b_act')(x)
#    
#    x = MaxPooling2D((2, 2), name=name+'conv3_pool')(x)
#    
#    x = SeparableConv2D(512, (3, 3), padding='same', name=name+'conv4a')(x)
#    x = BatchNormalization(name=name+'conv4a_bn')(x)
#    x = Activation('relu', name=name+'conv4a_act')(x)
#    
#    x = SeparableConv2D(512, (3, 3), padding='same', name=name+'conv4b')(x)
#    x = BatchNormalization(name=name+'conv4b_bn')(x)
#    x = Activation('relu', name=name+'conv4b_act')(x)
#    
#    x = GlobalMaxPooling2D(name=name+'avg_pool')(x)
#    
#    x = Dense(1024, name=name+'dense0', activation='elu')(x)
#    x = Dropout(0.4)(x)
#    
#    x = Dense(1024, name=name+'dense1', activation='elu')(x)
#    x = Dropout(0.4)(x)
#    
#    x = Dense((win_size-y_offset)*nb_classes)(x)
#    x = Reshape(((win_size-y_offset), nb_classes))(x)
#    
#    output = Activation('softmax')(x)
#        
#    model = Model(input_data, output)
#    return model

if __name__ == '__main__':
    win_size = 4
    nb_classes = 2
    roi_size = 128
    y_offset=2
    mod = model_separable(win_size, roi_size, nb_classes, y_offset)