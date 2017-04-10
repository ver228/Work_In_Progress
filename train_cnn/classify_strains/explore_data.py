#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 20:58:04 2017

@author: ajaver
"""

import tables
import matplotlib.pylab as plt
import os
import glob


strain_dir = '/Volumes/SAMSUNG_USB/Classifier_DL/training/ser-6/'
fnames = glob.glob(os.path.join(strain_dir, '*.hdf5'))


for fname in fnames:
    with tables.File(fname, 'r') as fid:
        eig_coef = fid.get_node('/eig_coef')[:]
        
    plt.figure()
    tot_eigens = eig_coef.shape[1]
    for ii in range(tot_eigens):
        plt.subplot(tot_eigens, 1, ii+1)
        plt.plot(eig_coef[:, ii])
    