#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 09:39:27 2017

@author: ajaver
"""
import numpy as np
from scipy.ndimage.interpolation import map_coordinates, affine_transform
from scipy.ndimage.filters import gaussian_filter
from skimage.morphology import skeletonize, dilation, disk
from skimage.io import imread
import os

def random_rotation(rg, h, w):
    theta = np.pi / 180 * np.random.uniform(-rg, rg)
    rotation_matrix = np.array([[np.cos(theta), -np.sin(theta), 0],
                                [np.sin(theta), np.cos(theta), 0],
                                [0, 0, 1]])
    transform_matrix = transform_matrix_offset_center(rotation_matrix, h, w)    
    return transform_matrix


def random_shift(shift_range, h, w):
    tx = np.random.uniform(-shift_range, shift_range) * h
    ty = np.random.uniform(-shift_range, shift_range) * w
    translation_matrix = np.array([[1, 0, tx],
                                   [0, 1, ty],
                                   [0, 0, 1]])
    return translation_matrix


def random_zoom(zoom_range, h, w):
    if zoom_range[0] == 1 and zoom_range[1] == 1:
        zx, zy = 1, 1
    else:
        zx, zy = np.random.uniform(zoom_range[0], zoom_range[1], 2)
    zoom_matrix = np.array([[zx, 0, 0],
                            [0, zy, 0],
                            [0, 0, 1]])

    transform_matrix = transform_matrix_offset_center(zoom_matrix, h, w)
    
    return transform_matrix

def apply_transform_img(x,
                    transform_matrix,
                    fill_mode='nearest',
                    cval=0.):
    final_affine_matrix = transform_matrix[:2, :2]
    final_offset = transform_matrix[:2, 2]
    xt = affine_transform(x,
                        final_affine_matrix,
                        final_offset,
                        order=0,
                        mode=fill_mode,
                        cval=cval
                        )
    return xt


def transform_matrix_offset_center(matrix, x, y):
    o_x = float(x) / 2 + 0.5
    o_y = float(y) / 2 + 0.5
    offset_matrix = np.array([[1, 0, o_x], [0, 1, o_y], [0, 0, 1]])
    reset_matrix = np.array([[1, 0, -o_x], [0, 1, -o_y], [0, 0, 1]])
    transform_matrix = np.dot(np.dot(offset_matrix, matrix), reset_matrix)
    return transform_matrix

def elastic_transform(h, w, alpha_range, sigma):
    alpha = np.random.uniform(0, alpha_range)
    random_state = np.random.RandomState(None)
    
    dx = gaussian_filter((random_state.rand(h, w ) * 2 - 1), sigma, mode="constant", cval=0) * alpha
    dy = gaussian_filter((random_state.rand(h, w ) * 2 - 1), sigma, mode="constant", cval=0) * alpha
    x,y = np.meshgrid(np.arange(h), np.arange(w), indexing='ij')
    x = x + dx 
    y = y + dy 
    
    elastic_inds = np.reshape(x, (-1, 1)), np.reshape(y, (-1, 1))
    
    return elastic_inds
    
    
def random_transform(h, 
                     w, 
                     rotation_range=90, 
                     shift_range = 0.1,
                     horizontal_flip=True,
                     vertical_flip=True,
                     alpha_range=200,
                     sigma=10):
    
    rot_mat = random_rotation(rotation_range, h, w)
    shift_mat = random_shift(shift_range, h, w)
    
    transform_mat = np.dot(shift_mat, rot_mat)
    
    elastic_inds = elastic_transform(h, w, alpha_range, sigma)
    
    is_h_flip =  horizontal_flip and np.random.random() < 0.5
    is_v_flip =  vertical_flip and np.random.random() < 0.5
        

    return transform_mat, is_h_flip, is_v_flip, elastic_inds

def transform_img(img, transform_mat, is_h_flip, is_v_flip, elastic_inds):
    final_affine_matrix = transform_matrix[:2, :2]
    final_offset = transform_matrix[:2, 2]
    img_aug = affine_transform(
            img,
            final_affine_matrix,
            final_offset,
            order=0,
            mode='reflect',
            output=np.float32,
            cval=0.)
    if is_h_flip:
        img_aug = img_aug[::-1, :] 
    if is_v_flip:
        img_aug = img_aug[:, ::-1] 
    img_aug = map_coordinates(img_aug, elastic_inds, order=1).reshape((img.shape))
    return img_aug


def directory_img_generator(main_dir):
    fnames = os.listdir(main_dir)
    fnames = sorted(set(x[2:] for x in fnames))
    
    for fname in fnames:
        x_name = os.path.join(main_dir, 'X_' + fname) 
        y_name = os.path.join(main_dir, 'Y_' + fname) 
        
        X = imread(x_name)
        Y = imread(y_name)
        
        yield X,Y




#%%
#X_aug = map_coordinates(X, indices, order=1).reshape(shape_d)
#Y_aug = map_coordinates(Y.astype(np.float32), indices, order=1).reshape(shape_d)
#Y_aug = skeletonize(Y_aug>0).astype(np.uint8)
#    return X_aug, Y_aug


#    
#    img = apply_transform_img(xx, transform_x, 2)
#    if horizontal_flip and np.random.random() < 0.5:
#        img = img[::-1, :, :]
#    if vertical_flip and np.random.random() < 0.5:
#        img = img[:, ::-1, :]
#    return img, yr

#data_gen_args = dict(featurewise_center=True,
#                     featurewise_std_normalization=True,
#                     rotation_range=90.,
#                     width_shift_range=0.1,
#                     height_shift_range=0.1,
#                     zoom_range=0.2)
#image_datagen = ImageDataGenerator(**data_gen_args)
#mask_datagen = ImageDataGenerator(**data_gen_args)

main_dir = '/Users/ajaver/OneDrive - Imperial College London/food/train_set'

#def _elastic_transform(dd):
#    return elastic_transform(*dd, alpha_range, sigma)
#gen = map(_elastic_transform, directory_img_generator(main_dir))




#%%
pad_size = 25
for ii, (X,Y) in enumerate(directory_img_generator(main_dir)):
    
    pads = ((pad_size,pad_size), (pad_size,pad_size))
    X = np.lib.pad(X,pads , 'reflect')
    Y = np.lib.pad(Y, pads, 'reflect')

    Y = Y.astype(np.float32)
    transform_matrix, is_h_flip, is_v_flip, elastic_inds = \
    random_transform(*X.shape)
    
    X_aug = transform_img(X, 
                          transform_matrix, 
                          is_h_flip, 
                          is_v_flip, 
                          elastic_inds)
    
    Y_aug = transform_img(Y, 
                          transform_matrix, 
                          is_h_flip, 
                          is_v_flip, 
                          elastic_inds)
    
    Y_aug = dilation(Y_aug, disk(1))
    Y_aug = skeletonize(Y_aug>0).astype(np.uint8)
    
    
    import matplotlib.pylab as plt
    import cv2
    plt.figure()
    plt.imshow(X_aug, cmap='gray')
    _, cnts, _ = cv2.findContours(Y_aug, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    for cnt in cnts:
        plt.plot(*np.squeeze(cnt).T)


    if ii > 20:
        break

#%%

#plt.figure()
#
#for ii, (xt, yt) in enumerate([(X,Y), (X_aug, Y_aug)]):
#    plt.subplot(1,2,ii+1)
#    plt.imshow(xt, cmap='gray')
#    _, cnt, _ = cv2.findContours(yt, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#    cnt  =np.squeeze(cnt[0])
#    plt.plot(*cnt.T)
