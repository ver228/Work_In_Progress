#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 17:39:21 2017

@author: ajaver
"""
import tables
import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten, Reshape, Convolution2D, MaxPooling2D
from keras.layers.normalization import BatchNormalization
from keras.models import load_model

import tensorflow as tf
tf.device('/gpu:0')
# for reproducibility
rand_seed = 1337
np.random.seed(rand_seed)  

out_size = (49, 2)
roi_size = 128


# number of convolutional filters to use
nb_filters = 32
# convolution kernel size
kernel_size = (3, 3)
    

model = Sequential()
model.add(Convolution2D(64, kernel_size[0], kernel_size[1],
                        border_mode='valid',
                        input_shape= (roi_size, roi_size, 1)))
model.add(BatchNormalization())
model.add(Activation('relu'))

model.add(Convolution2D(64, kernel_size[0], kernel_size[1]))
model.add(BatchNormalization())
model.add(Activation('relu'))

model.add(Convolution2D(32, kernel_size[0], kernel_size[1]))
model.add(BatchNormalization())
model.add(Activation('relu'))


model.add(Flatten())
model.add(Dense(2000))
model.add(Activation('relu'))
#model.add(Dropout(0.5))
#
#model.add(Dense(1000))
#model.add(Activation('relu'))

model.add(Dense(500))
model.add(Activation('relu'))

model.add(Dense(200))
model.add(Activation('relu'))


model.add(Dense(out_size[0]*out_size[1]))
model.add(Activation('relu'))
model.add(Reshape((out_size)))

model.compile(loss='mean_squared_error',
              optimizer='adam',
              metrics=['mean_absolute_percentage_error'])
#%%
def _get_index(events_tot, val_frac, test_frac):
    inds = np.random.permutation(events_tot)
    test_size = np.round(events_tot*test_frac).astype(np.int)
    val_size = np.round(events_tot*val_frac).astype(np.int)
    
    
    all_ind = {'test' : inds[:test_size], 
               'val': inds[test_size:(val_size+test_size)],
               'train' : inds[(val_size+test_size):]}
    
    return all_ind

#%%
sample_file = 'N2 on food R_2011_03_09__11_58_06___6___3_sample.hdf5'
with tables.File(sample_file, 'r') as fid:
    
    #select a tiny sample
    tot = fid.get_node('/mask').shape[0]
    inds = np.random.permutation(tot)[:128]
    X = fid.get_node('/mask')[inds, :, :][:, :, :, np.newaxis]
    Y = fid.get_node('/skeleton')[inds, :, :]

model.fit(X, Y, batch_size=128, nb_epoch=200, verbose=1)

#%%
#model.fit(X, Y, batch_size=128, nb_epoch=200, verbose=1)
#
##%%
##nb_epoch = 10
##for i in range(20):
##    model.fit(X_train, Y_train, batch_size=128, nb_epoch=nb_epoch,
##                  verbose=1, validation_data=(X_val, Y_val))
##    model.save('skels_mod_{}.h5'.format((i+1)*nb_epoch))
#
##%%
#
##X, Y = X_train, Y_train
#
##model = load_model('skels_mod_40.h5')
#Y_pred = model.predict(X)
#
###%%
#import matplotlib.pylab as plt
#
#ind = 0
#plt.figure()
#plt.imshow(np.squeeze(X[ind]), interpolation='None', cmap='gray')
#plt.grid('off')
#
#plt.plot(Y[ind, :, 0], Y[ind, :, 1], '.r')
#plt.plot(Y[ind, 0, 0], Y[ind, 0, 1], 'sr')
#plt.plot(Y_pred[ind, :, 0], Y_pred[ind, :, 1], '.b')
#plt.plot(Y_pred[ind, 0, 0], Y_pred[ind, 0, 1], 'ob')
#
#
#





