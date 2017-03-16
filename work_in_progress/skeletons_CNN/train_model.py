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
from keras.utils import np_utils
from keras.models import load_model


# for reproducibility
rand_seed = 1337
np.random.seed(rand_seed)  

out_size = (49, 2)
roi_size = 120

# number of convolutional filters to use
nb_filters = 32
# size of pooling area for max pooling
pool_size = (2, 2)
# convolution kernel size
kernel_size = (3, 3)


model = Sequential()
model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1],
                        border_mode='valid',
                        input_shape= (roi_size, roi_size, 1)))
model.add(BatchNormalization())
model.add(Activation('relu'))

model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1]))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=pool_size))

model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1]))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=pool_size))

#model.add(Dropout(0.5))
model.add(Flatten())
model.add(Dense(1000))
model.add(Activation('relu'))
model.add(Dropout(0.2))

model.add(Dense(500))
model.add(Activation('relu'))
model.add(Dropout(0.2))

model.add(Dense(200))
model.add(Activation('relu'))
model.add(Dropout(0.2))


model.add(Dense(out_size[0]*out_size[1]))
model.add(Activation('relu'))
model.add(Reshape((out_size)))

model.compile(loss='mean_absolute_error',
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
sample_file = 'N2 on food R_2011_03_09__11_58_06___6___3_sampleshort.hdf5'
with tables.File(sample_file, 'r') as fid:
    X = fid.get_node('/mask')[:][:, :, :, np.newaxis]
    Y = fid.get_node('/skeleton')[:]

events_tot = X.shape[0]
index = _get_index(events_tot, val_frac=0.2, test_frac=0.05)

X_train, X_val, X_test = [X[index[key]] for key in ['train', 'test', 'val']]
Y_train, Y_val, Y_test = [Y[index[key]] for key in ['train', 'test', 'val']]

#%%
model.fit(X_train, Y_train, batch_size=128, nb_epoch=10,
              verbose=1, validation_data=(X_val, Y_val))