#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 14:24:40 2016

@author: ajaver
"""

import tables
import numpy as np
import time

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.utils import np_utils
from keras.models import load_model

import matplotlib as mpl
import matplotlib.pyplot as plt
plt.style.use('seaborn-deep')
mpl.rcParams['image.interpolation'] = 'none'
mpl.rcParams['image.cmap'] = 'gray'

from tierpsy.analysis.ske_init.filterTrajectModel import  reformat_for_model


def read_field_data(filename, field):
    with tables.File(filename, 'r') as fid:
        data = fid.get_node('/', field + '_x')[:]
        label = fid.get_node('/', field + '_y')[:]
    
        
    #if rescale != 1:
    #    data = np.array([imresize(x, rescale) for x in data])
    
    dat_x = reformat_for_model(data)
    
    
    #a worm will be 2 (good worm),3(difficult worm),4 (aggregate)
    good_labels = ((label != 1) & (label <= 4)).astype(np.uint8)
    dat_y = np_utils.to_categorical(good_labels, 2)
    
    return dat_x, dat_y
#%%
def show_images(data, 
                labels = np.zeros([]),
                n_rows = 7, 
                lab_colors = ['red', 'green'], 
                lab_names = ['bad', 'worm']):

    if labels.ndim > 1:
        labels = np.argmax(labels, axis=1)
    
    plt.figure()
    tot_figs = min(n_rows*n_rows, data.shape[0])
    for ii in range(tot_figs): 
        ax = plt.subplot(n_rows,n_rows, ii+1, aspect='equal');
        img = np.squeeze(data[ii])
        img = ((img + 0.5)*255).astype(np.uint8)
        plt.imshow(img);
        plt.axis('off');
        
        if labels.size > 0:
            lab = labels[ii]
            ax.text(3, 8, lab_names[lab], 
                    bbox={'facecolor':lab_colors[lab], 'alpha':0.5, 'pad':1})
    plt.subplots_adjust(wspace=0.01, hspace=0.01)

#%%
def get_model_convnet(X_train, Y_train, X_val, Y_val):
    
    model = Sequential()
    
    batch_size = 128
    nb_classes = 2
    nb_epoch = 50
    
    # input image dimensions
    img_rows, img_cols = X_train.shape[1:3]
    # number of convolutional filters to use
    nb_filters = 32
    # size of pooling area for max pooling
    pool_size = (2, 2)
    # convolution kernel size
    kernel_size = (5, 5)
    
    rand_seed = 1337
    np.random.seed(rand_seed)  # for reproducibility
    
    model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1],
                            border_mode='valid',
                            input_shape= (img_rows, img_cols, 1)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=pool_size))
    
    model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1]))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=pool_size))
    
    #model.add(Dropout(0.5))
    model.add(Flatten())
    model.add(Dense(500))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    
    model.add(Dense(70))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    
    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))
    
    model.compile(loss='categorical_crossentropy',
                  optimizer='adadelta',
                  metrics=['accuracy'])
    
    model.fit(X_train, Y_train, batch_size=batch_size, nb_epoch=nb_epoch,
              verbose=1, validation_data=(X_val, Y_val))
    return model
#%%
def show_bad(model, X, Y):
    pred = model.predict_proba(X)
    
    label_pred = np.argmax(pred, axis=1)
    label_real = np.argmax(Y, axis=1)    
    
    bad_labels = label_pred!=label_real
    
    
    bad_imgs = np.squeeze(X[bad_labels])
    if bad_imgs.ndim == 2:
        bad_imgs = bad_imgs[None, :, :]
    
    print('*****')
    print(sum(bad_labels), len(label_real))
    #%%
    show_images(bad_imgs, labels = label_pred[bad_labels])
    
 #%%    

if __name__ == '__main__':
    filename = '/Users/ajaver/OneDrive - Imperial College London/training_data/sample.hdf5'
    model_trained_path = '/Users/ajaver/Documents/GitHub/Multiworm_Tracking/MWTracker/misc/model_isworm_20161130_002654.h5'
    
    X_train, Y_train = read_field_data(filename, 'train')
    X_val, Y_val = read_field_data(filename, 'val')
    
#    model = get_model_convnet(X_train, Y_train, X_val, Y_val)
#    
#    #%%
#    score = model.evaluate(X_val, Y_val, verbose=0)
#    print('Test score:', score[0])
#    print('Test accuracy:', score[1])
#    
    
#    #%%
#    model_name = 'model_isworm_%s.h5' % time.strftime('%Y%m%d_%H%M%S')    
#    model.save(model_name)
    #%% Show wrongly classified
    model = load_model(model_trained_path)
    show_bad(model, X_val, Y_val)
    #show_bad(model, X_train, Y_train)
    #X_test, Y_test = read_field_data(filename, 'test')
    




