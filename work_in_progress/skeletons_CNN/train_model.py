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
#%%

# for reproducibility
rand_seed = 1337
np.random.seed(rand_seed)  


def test1():
    out_size = (49, 2)
    roi_size = 120
    
    # number of convolutional filters to use
    nb_filters = 32
    # convolution kernel size
    kernel_size = (3, 3)
    
    
    model = Sequential()
    model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1],
                            border_mode='valid',
                            input_shape= (roi_size, roi_size, 1)))
    model.add(Activation('relu'))
    
    model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1]))
    model.add(Activation('relu'))
    #model.add(MaxPooling2D(pool_size=pool_size))
    
    model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1]))
    model.add(Activation('relu'))
    #model.add(MaxPooling2D(pool_size=pool_size))
    
    #model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1]))
    #model.add(Activation('relu'))
    #
    #model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1]))
    #model.add(Activation('relu'))
    
    
    #model.add(Dropout(0.5))
    model.add(Flatten())
    model.add(Dense(2000))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    
    model.add(Dense(500))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))
    
    model.add(Dense(200))
    model.add(Activation('relu'))
    
    
    model.add(Dense(out_size[0]*out_size[1]))
    model.add(Activation('relu'))
    model.add(Reshape((out_size)))
    
    model.compile(loss='mean_absolute_error',
                  optimizer='adam',
                  metrics=['mean_absolute_percentage_error'])
    
#%%
def test2():
    out_size = (49, 2)
    roi_size = 120
    
    
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
    
    model.add(Convolution2D(32, kernel_size[0], kernel_size[1]))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    
    model.add(Flatten())
    model.add(Dense(4000))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    
    model.add(Dense(1000))
    model.add(Activation('relu'))
    
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

def test3():
    out_size = (49, 2)
    roi_size = 120
    
    # number of convolutional filters to use
    nb_filters = 32
    # convolution kernel size
    kernel_size = (3, 3)
    
    
    model = Sequential()
    model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1],
                            border_mode='valid',
                            input_shape= (roi_size, roi_size, 1)))
    model.add(Activation('relu'))
    
    model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1]))
    model.add(Activation('relu'))
    #model.add(MaxPooling2D(pool_size=pool_size))
    
    model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1]))
    model.add(Activation('relu'))
    #model.add(MaxPooling2D(pool_size=pool_size))
    
    #model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1]))
    #model.add(Activation('relu'))
    #
    #model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1]))
    #model.add(Activation('relu'))
    
    
    #model.add(Dropout(0.5))
    model.add(Flatten())
    model.add(Dense(2000))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    
    model.add(Dense(500))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))
    
    model.add(Dense(200))
    model.add(Activation('relu'))
    
    
    model.add(Dense(out_size[0]*out_size[1]))
    model.add(Activation('relu'))
    model.add(Reshape((out_size)))
    
    model.compile(loss='mean_absolute_error',
                  optimizer='adam',
                  metrics=['mean_absolute_percentage_error'])

#%%
#is_debug = False
#
sample_file = 'N2 on food R_2011_03_09__11_58_06___6___3_sample.hdf5'
data = {}
with tables.File(sample_file, 'r') as fid:
    for field in ['test', 'train', 'val']:
        ind = fid.get_node('/index_groups/' + field)[:]
        
        X = fid.get_node('/mask')[ind, :, :][:, :, :, np.newaxis]
        Y = fid.get_node('/skeleton')[ind, :, :]
        data[field] = (X, Y)


#%%
#nb_epoch = 10
#for i in range(20):
#    model.fit(X_train, Y_train, batch_size=128, nb_epoch=nb_epoch,
#                  verbose=1, validation_data=(X_val, Y_val))
#    model.save('skels_mod2_{}.h5'.format((i+1)*nb_epoch))

#%%
model = load_model('skels_mod_60.h5')
#%%
X, Y = data['test']
#X /= 2.
#X += 0.5

import matplotlib.pylab as plt

ind = 900
Y_pred = model.predict(X[ind][np.newaxis, :, :, :])

plt.figure()
plt.imshow(np.squeeze(X[ind]), interpolation='None', cmap='gray')
plt.grid('off')

plt.plot(Y[ind, :, 0], Y[ind, :, 1], '.r')
plt.plot(Y[ind, 0, 0], Y[ind, 0, 1], 'sr')
plt.plot(Y_pred[0, :, 0], Y_pred[0, :, 1], '.b')
plt.plot(Y_pred[0, 0, 0], Y_pred[0, 0, 1], 'ob')









