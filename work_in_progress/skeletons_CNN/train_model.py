#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 17:39:21 2017

@author: ajaver
"""
import tables
import numpy as np

#from keras.models import Sequential
#from keras.layers import Dense, Dropout, Activation, Flatten, Reshape, Convolution2D, MaxPooling2D
#from keras.layers.normalization import BatchNormalization
#from keras.utils import np_utils
#from keras.models import load_model
#from keras.optimizers import Adam
import os
import matplotlib.pylab as plt
import time

from keras.models import Sequential
from keras.models import Model

from keras import layers
from keras.layers import Conv2D
from keras.layers import BatchNormalization
from keras.layers import Activation
from keras.layers import Input
from keras.layers import MaxPooling2D
from keras.layers import GlobalMaxPooling2D
from keras.layers import Dense
from keras.layers import Reshape
from keras.layers import Flatten
from keras.layers import Dropout

from keras.models import load_model
from keras.callbacks import TensorBoard, ModelCheckpoint, History
from keras.optimizers import Adam


SAVE_DIR = '/Volumes/behavgenom_archive$/Avelino/skeletons_cnn_tests/'

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
    roi_size = 128
    kernel_size = (3, 3)
    
    #BatchNormalization in the first layer seems to be problematic
    #MaxPooling2D reduce the number of parameters needed, and seems to make convergence possible
    model = Sequential()
    model.add(Convolution2D(32, kernel_size[0], kernel_size[1],
                            border_mode='valid',
                            input_shape= (roi_size, roi_size, 1))) 
    model.add(Activation('relu'))
    
    model.add(Convolution2D(64, kernel_size[0], kernel_size[1]))
    model.add(MaxPooling2D((2,2)))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    
    model.add(Convolution2D(128, kernel_size[0], kernel_size[1]))
    model.add(MaxPooling2D((2,2))) 
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    
    model.add(Convolution2D(64, kernel_size[0], kernel_size[1]))
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
                  optimizer=Adam(lr=5e-4, decay=0.05),
                  metrics=['mean_absolute_percentage_error'])

    return model
#%%
def test4():
    # for reproducibility
    rand_seed = 1337
    np.random.seed(rand_seed)  
    
    out_size = (49, 2)
    roi_size = 128
        
    
    input_shape = (roi_size, roi_size, 1)
    img_input =  Input(shape=input_shape)
    
    x = Conv2D(32, (3, 3), padding='same', name='conv0')(img_input)
    x = Activation('elu', name='conv0_act')(x)
    x = MaxPooling2D((2, 2), name='conv0_pool')(x)
    
    x = Conv2D(64, (3, 3), padding='same', name='conv1a')(x)
    x = BatchNormalization(name='conv1a_bn')(x)
    x = Activation('elu', name='conv1a_act')(x)
    
    x = Conv2D(64, (3, 3), padding='same', name='conv1b')(x)
    x = BatchNormalization(name='conv1b_bn')(x)
    x = Activation('elu', name='conv1b_act')(x)
    
    x = MaxPooling2D((2, 2), name='conv1_pool')(x)
    
    x = Conv2D(128, (3, 3), padding='same', name='conv2a')(x)
    x = BatchNormalization(name='conv2a_bn')(x)
    x = Activation('elu', name='conv2a_act')(x)
    
    x = Conv2D(128, (3, 3), padding='same', name='conv2b')(x)
    x = BatchNormalization(name='conv2b_bn')(x)
    x = Activation('elu', name='conv2b_act')(x)
    
    
    x = MaxPooling2D((2, 2), name='conv2_pool')(x)
    
    x = Conv2D(256, (3, 3), padding='same', name='conv3a')(x)
    x = BatchNormalization(name='conv3a_bn')(x)
    x = Activation('elu', name='conv3a_act')(x)
    
    x = Conv2D(256, (3, 3), padding='same', name='conv3b')(x)
    x = BatchNormalization(name='conv3b_bn')(x)
    x = Activation('elu', name='conv3b_act')(x)
    
    x = GlobalMaxPooling2D(name='avg_pool')(x)
    
    x = Dense(1024, name='dense0', activation='elu')(x)
    x = Dropout(0.4)(x)
    
    x = Dense(512, name='dense1', activation='elu')(x)
    x = Dropout(0.4)(x)
    
    x = Dense(128, name='dense2', activation='elu')(x)
    x = Dropout(0.2)(x)
    
    x = Dense(out_size[0]*out_size[1], activation='elu', name='skeleton')(x)
    x = Reshape((out_size))(x)
    
    
    
    model = Model(img_input, x)
    optimizer = Adam(lr=1e-3)#, decay=0.05)
    model.compile(loss='mean_absolute_error',
                  optimizer=optimizer,
                  metrics=['mean_absolute_error', 'mean_squared_error', 'mean_absolute_percentage_error'])


    return model

def test5():
    # for reproducibility
    rand_seed = 1337
    np.random.seed(rand_seed)  
    
    out_size = (49, 2)
    roi_size = 128
    
    input_shape = (roi_size, roi_size, 1)
    img_input =  Input(shape=input_shape)
    
    x = Conv2D(32, (3, 3), padding='same', use_bias=False, name='conv0')(img_input)
    x = BatchNormalization(name='conv0a_bn')(x)
    x = Activation('relu', name='conv0_act')(x)
    x = MaxPooling2D((2, 2), name='conv0_pool')(x)
    
    x = Conv2D(64, (3, 3), padding='same', use_bias=False, name='conv1a')(x)
    x = BatchNormalization(name='conv1a_bn')(x)
    x = Activation('relu', name='conv1a_act')(x)
    
    residual = Conv2D(128, (1, 1), strides=(2, 2),
                          padding='same', use_bias=False)(x)
    residual = BatchNormalization()(residual)
    x = Conv2D(128, (3, 3), padding='same', use_bias=False, name='block2_sepconv1')(x)
    x = BatchNormalization(name='block2_sepconv1_bn')(x)
    x = Activation('relu', name='block2_sepconv2_act')(x)
    x = Conv2D(128, (3, 3), padding='same', use_bias=False, name='block2_sepconv2')(x)
    x = BatchNormalization(name='block2_sepconv2_bn')(x)
    x = MaxPooling2D((2, 2), padding='same', name='block2_pool')(x)
    x = layers.add([x, residual])
    
    
    residual = Conv2D(512, (1, 1), strides=(2, 2),
                          padding='same', use_bias=False)(x)
    residual = BatchNormalization()(residual)
    x = Activation('relu', name='block3_sepconv1_act')(x)
    x = Conv2D(256, (3, 3), padding='same', use_bias=False, name='block3_sepconv1')(x)
    x = BatchNormalization(name='block3_sepconv1_bn')(x)
    x = Activation('relu', name='block3_sepconv2_act')(x)
    x = Conv2D(512, (3, 3), padding='same', use_bias=False, name='block3_sepconv2')(x)
    x = BatchNormalization(name='block3_sepconv2_bn')(x)
    x = MaxPooling2D((2, 2), padding='same', name='block3_pool')(x)
    x = layers.add([x, residual])
    
    
    x = Conv2D(1024, (3, 3), padding='same', use_bias=False, name='block14_sepconv2')(x)
    x = BatchNormalization(name='block14_sepconv2_bn')(x)
    x = Activation('relu', name='block14_sepconv2_act')(x)
    
    x = GlobalMaxPooling2D(name='avg_pool')(x)
    
    
    #layers seems to be key to capture the worm shape
    #i need to use ELU instead of RELU otherwise the skeletons converges to 0
    x = Dense(1024, name='dense0', activation='elu')(x)
    x = Dropout(0.4)(x)
    
    x = Dense(512, name='dense1', activation='elu')(x)
    x = Dropout(0.4)(x)
    
    x = Dense(256, name='dense2', activation='elu')(x)
    x = Dropout(0.2)(x)
    
    x = Dense(128, name='dense3', activation='elu')(x)
    x = Dropout(0.1)(x)
    
    x = Dense(out_size[0]*out_size[1], activation='elu', name='skeleton')(x)
    x = Reshape((out_size))(x)
    
    
    
    model = Model(img_input, x)
    optimizer = Adam(lr=1e-3)#, decay=0.05)
    model.compile(loss='mean_absolute_error',
                  optimizer=optimizer,
                  metrics=['mean_absolute_error', 'mean_squared_error', 'mean_absolute_percentage_error'])
    
    return model
    
#%%
#model = test5()
model_dir = '/Volumes/behavgenom_archive$/Avelino/skeletons_cnn_tests/logs/resnet_20170322_191529'
model = load_model(os.path.join(model_dir, 'tiny-018-0.0415.h5'))

optimizer = Adam(lr=1e-4, decay=0.05)
model.compile(loss='mean_absolute_error',
                  optimizer=optimizer,
                  metrics=['mean_absolute_error', 'mean_squared_error', 'mean_absolute_percentage_error'])

sample_file = 'N2 on food R_2011_03_09__11_58_06___6___3_sample.hdf5'
sample_file = os.path.join(SAVE_DIR, 'data', sample_file)

rand_seed = 1337
np.random.seed(rand_seed)  
data = {}
with tables.File(sample_file, 'r') as fid:
    for field in ['test', 'train', 'val']:
        ind = fid.get_node('/index_groups/' + field)[:]
        
        X = fid.get_node('/mask')[ind, :, :][:, :, :, np.newaxis]
        Y = fid.get_node('/skeleton')[ind, :, :]
        #normalize
        roi_size = X.shape[1]
        Y = (Y-(roi_size/2.))/roi_size*2
        data[field] = (X, Y)
        
        
#%%
epochs = 200

log_dir = os.path.join(SAVE_DIR, 'logs/main_%s' % time.strftime('%Y%m%d_%H%M%S'))
pad=int(np.ceil(np.log10(epochs+1)))
checkpoint_file = os.path.join(log_dir, 'tiny-{epoch:0%id}-{loss:.4f}.h5' % pad)

history = History()
tb = TensorBoard(log_dir=log_dir)
mcp = ModelCheckpoint(checkpoint_file, verbose=0,  mode='auto', period=1)

model.fit(*data['train'], 
          batch_size=128, 
          epochs=epochs, 
          validation_data=data['val'],
          verbose=1, 
          callbacks=[tb, mcp, history])

#%%
#model = load_model('skels_mod_60.h5')
#%%
X, Y = data['test']

ind = 900
Y_pred = model.predict(X[ind][np.newaxis, :, :, :])

plt.figure()
plt.imshow(np.squeeze(X[ind]), interpolation='None', cmap='gray')
plt.grid('off')

plt.plot(Y[ind, :, 0], Y[ind, :, 1], '.r')
plt.plot(Y[ind, 0, 0], Y[ind, 0, 1], 'sr')
plt.plot(Y_pred[0, :, 0], Y_pred[0, :, 1], '.b')
plt.plot(Y_pred[0, 0, 0], Y_pred[0, 0, 1], 'ob')
