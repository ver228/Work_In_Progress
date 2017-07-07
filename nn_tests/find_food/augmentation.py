#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 09:39:27 2017

@author: ajaver
"""
import numpy as np
from scipy.ndimage.interpolation import map_coordinates, affine_transform
from scipy.ndimage.filters import gaussian_filter
from scipy.ndimage import binary_fill_holes
from skimage.morphology import skeletonize, dilation, disk
from skimage.io import imread
import os
import multiprocessing as mp
from functools import partial

from tensorflow.contrib import keras
K = keras.backend
Iterator = keras.preprocessing.image.Iterator
#from keras.preprocessing.image import Iterator
#from keras import backend as K

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

def transform_img(img, transform_matrix, is_h_flip, is_v_flip, elastic_inds):
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


def augment_data(X, 
                 Y,
                 **transform_ags):
    
    transform_matrix, is_h_flip, is_v_flip, elastic_inds = \
    random_transform(*X.shape[:2],**transform_ags)
    
    X_aug = np.zeros_like(X)
    for nn in range(X.shape[-1]):
        X_aug[:, :, nn] = transform_img(X[: ,:, nn], 
                          transform_matrix, 
                          is_h_flip, 
                          is_v_flip, 
                          elastic_inds)
    
    Y_aug = np.zeros_like(Y)
    for nn in range(Y.shape[-1]):
        Y_aug[: ,:, nn] = transform_img(Y[: ,:, nn], 
                          transform_matrix, 
                          is_h_flip, 
                          is_v_flip, 
                          elastic_inds)
        
        #yy = dilation(yy, disk(1))
        #Y_aug[: ,:, nn] = skeletonize(yy>0).astype(np.uint8)
    
    
    
    return X_aug, Y_aug
#%%

#%%
def process_data(images, input_size, pad_size, tile_corners, transform_ags):
    #%%
    def _get_tile_in(img, x,y):
            return img[np.newaxis, x:x+input_size, y:y+input_size]
        
    def _get_tile_out(img, x,y):
        #not very efficient, but i cannot be bother to fix it
        D  = _get_tile_in(img,x,y)
        return  D[:, pad_size:-pad_size, pad_size:-pad_size]
       
    pad_size_s =  ((pad_size,pad_size), (pad_size,pad_size), (0,0))
    X, Y = images
    #normalize image
    X = X.astype(K.floatx())
    X -= np.median(X)
    
    
    X = X[:, :, np.newaxis]
    Y = Y[:, :, np.newaxis]
    
    X = np.lib.pad(X, pad_size_s , 'reflect')
    Y = np.lib.pad(Y, pad_size_s, 'reflect')
    X_aug, Y_aug = augment_data(X,Y, **transform_ags)
    
    #transform into a valid output for the network
    Y_aug = np.concatenate([Y_aug.astype(dtype=K.floatx()), ~Y_aug], axis=2)
    assert np.all(Y_aug[:,:,1] != Y_aug[:,:,0])
    
    #subdivided in tiles
    X_aug_t = [_get_tile_in(X_aug, x, y) for x,y in tile_corners]
    Y_aug_t = [_get_tile_out(Y_aug, x, y) for x,y in tile_corners]
    #%%
    return X_aug_t, Y_aug_t

class ImageMaskGenerator(Iterator):
    
    def __init__(self, 
                 generator,
                 transform_ags,
                 pad_size,
                 input_size,
                 tile_corners,
                 batch_size=32, 
                 epoch_size=None,
                 shuffle=True, 
                 seed=None):
       
        self.generator = generator
        
        if epoch_size is None:
            self.tot_samples = len(self.generator)
        else:
            self.tot_samples = epoch_size
        
        self.transform_ags = transform_ags
        self.pad_size = pad_size
        self.input_size = input_size
        self.output_size = input_size - pad_size*2
        self.tile_corners = tile_corners
        
        super(ImageMaskGenerator, self).__init__(self.tot_samples, batch_size, shuffle, seed)

    def next(self):
        """
        # Returns
            The next batch.
        """
        # Keeps under lock only the mechanism which advances
        # the indexing of each batch.
        f_args = dict(input_size=self.input_size, 
                          pad_size=self.pad_size, 
                          tile_corners=self.tile_corners, 
                          transform_ags=self.transform_ags
                          )
        _process_data = partial(process_data, **f_args)
        
        with self.lock:
            index_array, current_index, current_batch_size = next(self.index_generator)
            #load all the data first (it is easier to avoid colitions)
            images = [self.generator[j] for j in index_array]
            
            
        
        batch_x, batch_y  = zip(*list(map(_process_data, images)))
        
        batch_x = sum(batch_x, [])
        batch_y = sum(batch_y, [])
        
        
        return np.concatenate(batch_x), np.concatenate(batch_y)


class DirectoryImgGenerator(object):
    def __init__(self, main_dir):
        fnames = os.listdir(main_dir)
        fnames = sorted(set(x[2:] for x in fnames))
        
        self.main_dir = main_dir
        self.fnames = fnames

    def __len__(self): 
        return len(self.fnames)

    def __getitem__(self, i):
        return self._get(self.fnames[i])

    def __iter__(self):
        for fname in self.fnames:
            yield self._get(fname)
    
    def _get(self, fname):
            x_name = os.path.join(self.main_dir, 'X_' + fname) 
            y_name = os.path.join(self.main_dir, 'Y_' + fname) 
            
            X = imread(x_name)
            Y = imread(y_name)
            
            Y = binary_fill_holes(Y)
            return X,Y

#%%
def get_sizes(im_size, d4a_size= 24):
    #assuming 4 layers of convolutions
    def _in_size(d4a_size, N = 4): 
        mm = d4a_size
        for n in range(N):
            mm = mm*2 + 2 + 2
        return mm

    def _out_size(d4a_size, N = 4):
        mm = d4a_size -2 -2
        for n in range(N):
            mm = mm*2 - 2 - 2
        return mm


    #this is the size of the central reduced layer. I choose this value manually
    input_size = _in_size(d4a_size, N = 4) #required 444 of input
    output_size = _out_size(d4a_size, N = 4) #set 260 of outpu

    pad_size = int((input_size-output_size)/2)
    ty = im_size[1]-output_size
    tx = im_size[0]-output_size
    tile_corners = [(0,0), 
                    (0, ty),
                    (tx, 0),
                    (tx,ty)
                    ] #corners on how the image is going to be subdivided

    return input_size, output_size, pad_size, tile_corners

if __name__ == '__main__':
    import matplotlib.pylab as plt
    import cv2
    import time
        
    im_size = (512, 512)
    main_dir = '/Users/ajaver/OneDrive - Imperial College London/food/train_set'
    transform_ags = dict(rotation_range=90, 
         shift_range = 0.1,
         horizontal_flip=True,
         vertical_flip=True,
         alpha_range=200,
         sigma=10)
    input_size, output_size, pad_size, tile_corners = get_sizes(im_size)
    gen = ImageMaskGenerator(DirectoryImgGenerator(main_dir), 
                             transform_ags, 
                             pad_size,
                             input_size,
                             tile_corners,
                             batch_size=1)
    assert gen.output_size == output_size
    
#    tic = time.time()
#    for ii, (batch_x, batch_y) in enumerate(gen):
#        toc = time.time()
#        print(ii, toc - tic)
#        tic = toc
        
        
        
        
    batch_x, batch_y = next(gen)
    for ii, (X,Y) in enumerate(zip(batch_x, batch_y)):
        #%%
        plt.figure()
        plt.subplot(1,2,1)
        plt.imshow(np.squeeze(X), cmap='gray')
        plt.subplot(1,2,2)
        I_d = np.squeeze(X).copy()
        patch = I_d[gen.pad_size:-gen.pad_size, gen.pad_size:-gen.pad_size]
        
        I_d[gen.pad_size:-gen.pad_size, gen.pad_size:-gen.pad_size] = patch*Y[:,:,0]
        
        plt.imshow(I_d, cmap='gray')
        #%%
#        Y_d = Y[:,:,0].astype(np.uint8)
#        _, cnts, _ = cv2.findContours(Y_d, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#        for cnt in cnts:
#            x, y  = np.squeeze(cnt).T
#            x += gen.pad_size
#            y += gen.pad_size
#            plt.plot(x,y)
#            nn = gen.pad_size, gen.pad_size + gen.output_size
#            xs = [nn[0], nn[0], nn[1], nn[1], nn[0]]
#            ys = [nn[0], nn[1], nn[1], nn[0], nn[0]]
#            plt.plot(xs,ys)


