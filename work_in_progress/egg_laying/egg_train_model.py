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

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers.normalization import BatchNormalization
from keras.utils import np_utils
from keras.models import load_model

from egg_trainset import _plot_seq


rand_seed = 1337
np.random.seed(rand_seed)  # for reproducibility

#%%
def ini_model(img_rows, img_cols, win_size):
    
    nb_classes = 2
    
    
    # number of convolutional filters to use
    nb_filters = 32
    # size of pooling area for max pooling
    pool_size = (2, 2)
    # convolution kernel size
    kernel_size = (5, 5)
    
    
    model = Sequential()
    
    model.add(Convolution2D(nb_filters, 1, 1,
                            border_mode='valid',
                            input_shape= (img_rows, img_cols, win_size)))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    
    model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1]))
#    model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1],
#                            border_mode='valid',
#                            input_shape= (img_rows, img_cols, win_size)))
    
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=pool_size))
    
    model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1]))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=pool_size))
    
    #model.add(Dropout(0.5))
    model.add(Flatten())
    model.add(Dense(500))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    
    model.add(Dense(70))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    
    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))
    
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    
    return model
#%%

def read_field_data(filename, field):
    with tables.File(filename, 'r') as fid:
        indexes = fid.get_node('/partitions/' + field)[:]
        
        X = fid.get_node('/egg_laying_X')[indexes, :, :, :]
        X = np.rollaxis(X, 1, 4)
        
        dat = fid.get_node('/egg_laying_Y')[indexes]
        Y = dat==0
        Y = np_utils.to_categorical(Y, 2)
        
    return X, Y
#%%
def show_bad(model, X, Y):
    pred = model.predict_proba(X)
    
    label_pred = np.argmax(pred, axis=1)
    label_real = np.argmax(Y, axis=1)    
    
    bad_labels = label_pred!=label_real
    bad_ind, = np.where(bad_labels)
    print('*****')
    print(len(bad_ind), len(label_real))
    return bad_ind
#%%
if __name__ == '__main__':
    batch_size = 128
    nb_epoch = 20
    
    training_file = 'samples.hdf5'
    #filename = '/Users/ajaver/OneDrive - Imperial College London/training_data/sample.hdf5'
    #model_trained_path = '/Users/ajaver/Documents/GitHub/Multiworm_Tracking/MWTracker/misc/model_isworm_20161130_002654.h5'
    
    X_train, Y_train = read_field_data(training_file, 'train')
    X_val, Y_val = read_field_data(training_file, 'val')
    
    # input image dimensions
    img_rows, img_cols, win_size = X_train.shape[1:]
    model = ini_model(img_rows, img_cols, win_size)
    model.fit(X_train, Y_train, batch_size=batch_size, nb_epoch=nb_epoch,
              verbose=1, validation_data=(X_val, Y_val))
   
    model_name = 'model_egg_laying_%s.h5' % time.strftime('%Y%m%d_%H%M%S')    
    model.save(model_name)
    
#    model_trained_path = 'model_egg_laying_20170308_105440.h5'
#    model = load_model(model_trained_path)
    #%%
    X_test, Y_test = read_field_data(training_file, 'test')
    score = model.evaluate(X_test, Y_test, verbose=0)
    print('Test score:', score[0])
    print('Test accuracy:', score[1])
    
    score = model.evaluate(X_val, Y_val, verbose=0)
    print('Test score:', score[0])
    print('Test accuracy:', score[1])
    
    #%%
    bad_ind = show_bad(model, X_val, Y_val)
#    for ind in bad_ind:
#            bad_seq = np.rollaxis(X[ind], 2, -3)
#            _plot_seq(bad_seq)
    #%%
    for ind in range(2840, 2855):
        mod = X_train[ind]
        prob = model.predict_proba(mod[np.newaxis, :, :, :])
        bad_seq = np.rollaxis(mod, 2, -3)
        plt.figure()
        _plot_seq(bad_seq)
        plt.suptitle('{} | {}'.format(Y_train[ind], np.round(prob)))
    #%%
    
    
    
    