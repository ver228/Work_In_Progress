#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 09:39:27 2017

@author: ajaver
"""
import numpy as np
from scipy.ndimage.interpolation import map_coordinates
from scipy.ndimage.filters import gaussian_filter

def elastic_transform(images, alpha_range=200, sigma=10, random_state=None):
    """Elastic deformation of images as described in [Simard2003]_.
    .. [Simard2003] Simard, Steinkraus and Platt, "Best Practices for
       Convolutional Neural Networks applied to Visual Document Analysis", in
       Proc. of the International Conference on Document Analysis and
       Recognition, 2003.
    """

    alpha = np.random.uniform(0, alpha_range)

    if random_state is None:
        random_state = np.random.RandomState(None)

    shape = images[0].shape
    if len(shape) == 3:
        shape = images[0].shape[1:]

    dx = gaussian_filter((random_state.rand(*shape) * 2 - 1), sigma, mode="constant", cval=0) * alpha
    dy = gaussian_filter((random_state.rand(*shape) * 2 - 1), sigma, mode="constant", cval=0) * alpha

    x, y = np.meshgrid(np.arange(shape[0]), np.arange(shape[1]), indexing='ij')
    indices = np.reshape(x+dx, (-1, 1)), np.reshape(y+dy, (-1, 1))

    results = []
    for image in images:

        if len(images[0].shape) == 3:
            im = np.zeros(image.shape)
            for i, c_image in enumerate(image):
                im[i] = map_coordinates(c_image, indices, order=1).reshape(shape)
        else:
            im = map_coordinates(image, indices, order=1).reshape(shape)

        results.append(im)

    return results

#%%
import os
import matplotlib.pylab as plt
import cv2

main_dir = '/Users/ajaver/OneDrive - Imperial College London/food/train_set'

fnames = os.listdir(main_dir)
fnames = sorted(set(x[2:] for x in fnames))

fname = fnames[0]
x_name = os.path.join(main_dir, 'X_' + fname) 
y_name = os.path.join(main_dir, 'Y_' + fname) 


X = cv2.imread(x_name, -1)
Y = cv2.imread(y_name, -1)

#factor = 2
shape_d = X.shape# [x*factor for x in X.shape]

alpha_range=200
sigma=10

alpha = np.random.uniform(0, alpha_range)
random_state = np.random.RandomState(None)


dx = gaussian_filter((random_state.rand(*shape_d) * 2 - 1), sigma, mode="constant", cval=0) * alpha
dy = gaussian_filter((random_state.rand(*shape_d) * 2 - 1), sigma, mode="constant", cval=0) * alpha
x, y = np.meshgrid(np.arange(shape_d[0]), np.arange(shape_d[1]), indexing='ij')
indices = np.reshape(x+dx, (-1, 1)), np.reshape(y+dy, (-1, 1))
X_aug = map_coordinates(X, indices, order=1).reshape(shape_d)
Y_aug = map_coordinates(Y, indices, order=1).reshape(shape_d)
#%%


#from shapely.geometry.polygon import Polygon


#_, cnt, _ = cv2.findContours(Y, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#cnt  =np.squeeze(cnt[0])
#xx, yy = cnt.T
##%%
#inds = np.ravel_multi_index(cnt.T, shape)
#
#x, y = np.meshgrid(np.arange(shape[0]), np.arange(shape[1]), indexing='ij')
#indices = np.reshape(x+dy, (-1, 1)), np.reshape(y+dx, (-1, 1))
#xs, ys = [x[inds] for x in indices]

#%%
plt.figure()
plt.subplot(2,2,1)
plt.imshow(X, cmap='gray')
#plt.plot(xx, yy)
plt.subplot(2,2,2)
#X_aug[Y_aug==1]=0
plt.imshow(X_aug, cmap='gray')
#plt.plot(xs, ys)
plt.subplot(2,2,3)
plt.imshow(Y, cmap='gray')
plt.subplot(2,2,4)
plt.imshow(Y_aug, cmap='gray')