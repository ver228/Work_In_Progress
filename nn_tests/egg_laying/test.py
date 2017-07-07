#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 11:30:44 2017

@author: ajaver
"""

import matplotlib.pylab as plt
import numpy as np
#from keras.models import load_model
#
#from egg_train_model import read_field_data
#from egg_trainset import plot_seq
#training_file = 'samples_eggs_resized.hdf5'
#model_path_resized = '/Volumes/behavgenom_archive$/Avelino/neural_networks/eggs_tests/logs/main_20170328_180144/main_resized-008-0.0891.h5'
#
#X_val,Y_val = read_field_data(training_file, 'test')
#
#model = load_model(model_path_resized)
#
#
#prob = model.predict(X_val)
##%%
#
#
##%%
#good = (prob[:,1]>0.5) == Y_val[:,1]
#print(np.sum(good)/Y_val.shape[0])
##%%
#inds, =  np.where(~good)
#
#for ii in inds[:10]:
#    plt.figure(figsize=(12,5))
#    seq = np.rollaxis(X_val[ii], 2, 0)
#    plot_seq(seq)
#    plt.suptitle((prob[ii, :], Y_val[ii, :]))
#%%
import os
import glob
import pandas as pd

results_dir = './results'
fnames = glob.glob(os.path.join(results_dir, '*.csv'))

#%%
results = []
for fname in fnames:
    bn = os.path.basename(fname).replace('_eggs.csv','')
    dat = pd.read_csv(fname)
    
    x_pred, = np.where(dat['egg_prob']> 0.99)
    x_true, = np.where(dat['true_events']> 0.99)
    
    results.append((bn, (x_pred, x_true)))
