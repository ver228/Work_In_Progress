#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 20:34:24 2017

@author: ajaver
"""

from keras.models import load_model
import glob
import os
import tables
import numpy as np
import matplotlib.pylab as plt

#log_dir = '/Users/ajaver/Documents/GitHub/work-in-progress/work_in_progress/skeletons_CNN/main_logs_20170321_210122'
#log_dir = '/Users/ajaver/Documents/GitHub/work-in-progress/work_in_progress/skeletons_CNN/logs/tiny_20170322_153316'
log_dir = './logs/tiny_20170322_165535'
sample_file = 'N2 on food R_2011_03_09__11_58_06___6___3_sample.hdf5'
sample_file = os.path.join(log_dir, 'input_set.hdf5')


rand_seed = 1337
np.random.seed(rand_seed)

with tables.File(sample_file, 'r') as fid:
    X_set = fid.get_node('/X')
    Y_set = fid.get_node('/Y')
    
    #select a tiny sample
    #X_set = fid.get_node('/mask')
    #Y_set = fid.get_node('/skeleton')
    
    
    tot = X_set.shape[0]
    roi_size = X_set.shape[1]
    
    inds = np.random.permutation(tot)[:128]
    X = X_set[inds, :, :]
    Y = Y_set[inds, :, :]
    #X = X[:, :, :, np.newaxis]
    
    #Y = Y/roi_size
    #Y = (Y-(roi_size/2.))/roi_size*2
    #X = -(X-np.mean(X, axis=(1,2)))
    
    
    
fnames = sorted(glob.glob(os.path.join(log_dir, '*.h5')))

#fnames = fnames[-4:]
fnames = fnames[:10]

for fname in fnames:
    print(fname)
    model = load_model(fname)
    
    Y_pred = model.predict(X)
    roi_size = X.shape[1]
    #%%
    #Y_c = Y*roi_size/2 + roi_size/2.
    Y_pred_c = Y_pred*roi_size/2 + roi_size/2.
    Y_c = Y*roi_size/2 + roi_size/2.
    #Y_pred_c = Y_pred
    
    
    ind = 20
    plt.figure()
    for ind in range(16):
        plt.subplot(4,4,ind+1)
        plt.imshow(np.squeeze(X[ind]), interpolation='None', cmap='gray')
        plt.grid('off')
        
        
        plt.plot(Y_c[ind, :, 0], Y_c[ind, :, 1], '-r')
        plt.plot(Y_c[ind, 0, 0], Y_c[ind, 0, 1], 'sr')
        plt.plot(Y_pred_c[ind, :, 0], Y_pred_c[ind, :, 1], '-b')
        plt.plot(Y_pred_c[ind, 0, 0], Y_pred_c[ind, 0, 1], 'ob')
        #model.save('skels_tiny_{}.h5'.format((i+1)*nb_epoch))
        
    plt.suptitle(os.path.basename(fname))
        #plt.xlim((-1.5,1.5))
        #plt.ylim((-1.5,1.5))
        
#%%
#fname = '/Users/ajaver/Documents/GitHub/work-in-progress/work_in_progress/skeletons_CNN/skels_mod_60.h5'
#with tables.File(fname, 'r') as fid:
#    dd = fid.get_node('/model_weights/convolution2d_1/convolution2d_1_W:0')[:]
#    
#    for ind in range(64):
#        plt.subplot(8,8,ind+1)
#        plt.imshow(np.squeeze(dd[:,:,:,ind]), interpolation='none', cmap='gray')
#        
        
    
    
