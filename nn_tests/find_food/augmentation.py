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
                     rotation_range, 
                     shift_range,
                     zoom_range,
                     horizontal_flip,
                     vertical_flip,
                     elastic_alpha_range,
                     elastic_sigma
                     ):
    
    rot_mat = random_rotation(rotation_range, h, w)
    shift_mat = random_shift(shift_range, h, w)
    zoom_mat = random_zoom(zoom_range, h, w)
    
    
    transform_mat = np.dot(shift_mat, rot_mat)
    transform_mat = np.dot(transform_mat, zoom_mat)
    
    elastic_inds = elastic_transform(h, w, elastic_alpha_range, elastic_sigma)
    
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


#%%

#%%
def process_data(images, input_size, pad_size, tile_corners, transform_ags={}):
    #%%
    def _get_tile_in(img, x,y):
            return img[np.newaxis, x:x+input_size, y:y+input_size, :]
        
    def _get_tile_out(img, x,y):
        #not very efficient, but i cannot be bother to fix it
        D  = _get_tile_in(img,x,y)
        return  D[:, pad_size:-pad_size, pad_size:-pad_size, :]
       
    def _cast_tf(D):
        D = D.astype(K.floatx())
        D = D[:, :, np.newaxis]
        return D
    
    def _augment_data(D, 
                      pad_size_s, 
                      transform_matrix, 
                      is_h_flip, 
                      is_v_flip, 
                      elastic_inds
                      ):
        if D is None:
            return None
        
        D = np.lib.pad(D, pad_size_s, 'reflect')
        D_aug = np.zeros_like(D)
        for nn in range(D.shape[-1]):
            D_aug[:, :, nn] = transform_img(D[: ,:, nn], 
                          transform_matrix, 
                          is_h_flip, 
                          is_v_flip, 
                          elastic_inds)
        D_aug = np.array(D_aug)
        return D_aug
    
    
    #read inputs
    Y, W = None, None
    if len(images) == 2:
        X, Y = images
    elif len(images) == 3:
        X, Y, W = images
    else:
        X = images
    
    
    #normalize image
    X = _cast_tf(X)
    X /= 255
    X -= np.median(X)
    
    if Y is not None:
        Y = _cast_tf(Y)
        Y = np.concatenate([Y==1., Y==0.], axis=2).astype(K.floatx()) #two channel cast
        
    if W is not None:
        W = _cast_tf(W)
    
    
    if len(transform_ags) > 0:
        expected_size = [x+pad_size*2 for x in X.shape[:2]] #the expected output size after padding
        transforms = random_transform(*expected_size, **transform_ags)
        pad_size_s =  ((pad_size,pad_size), (pad_size,pad_size), (0,0))
        X,Y,W = [_augment_data(x, pad_size_s, *transforms) for x in [X,Y,W]]
        
        X = [_get_tile_in(X, x, y) for x,y in tile_corners]
        
        if Y is not None:
            Y = [_get_tile_out(Y, x, y) for x,y in tile_corners]
        
        if W is not None:
            W = [_get_tile_out(W, x, y) for x,y in tile_corners]
        
        
    return [x for x in (X,Y,W) if not x is None]

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
            
            
        
        D  = zip(*list(map(_process_data, images))) #process data
        D = [np.concatenate(sum(x, [])) for x in D] #pack data
        
        if len(D) <= 2:
            return D
        else:
            #dirty trick to add a tensor with the weights. \
            #I do not find how to give this cleaningly to the weight function
            return D[0], np.concatenate((D[1], D[2]), axis=3)


class DirectoryImgGenerator(object):
    def __init__(self, main_dir, fill_mask=True, weight_params={}):
        fnames = os.listdir(main_dir)
        fnames = sorted(set(x[2:] for x in fnames))
        
        self.main_dir = main_dir
        self.fnames = fnames
        self.weight_params = weight_params
        self.fill_mask = fill_mask

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
            Yo = imread(y_name)
            
            
            if self.fill_mask:
                Y = binary_fill_holes(Yo)
            else:
                Y = dilation(Yo, disk(1))
            
            if not self.weight_params:
                return X,Y
            else:
                sigma = self.weight_params['sigma']
                weigth = self.weight_params['weigth']
                
                #increase the weights in the border
                W_border = gaussian_filter(Yo.astype(K.floatx()), sigma=2.5)
                W_border *= (sigma**2)*weigth #normalize weights
                
                #normalize the weights for the classes
                W_label = np.zeros_like(W_border) 
                lab_w = np.mean(Y)
                dd = Y>0
                W_label[dd] = 1/lab_w 
                W_label[~dd] = 1/(1-lab_w)
                
                W = W_label + W_border
                return X,Y, W

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

        
    im_size = (512, 512)
    fill_mask = True
    is_weigth = True
    
    main_dir = '/Users/ajaver/OneDrive - Imperial College London/food/train_set'
    transform_ags = dict(
            rotation_range=90, 
             shift_range = 0.02,
             zoom_range = (0.9, 1.1),
             horizontal_flip=True,
             vertical_flip=True,
             elastic_alpha_range=400,
             elastic_sigma=20
             )
        
    weight_params = dict(
            sigma=2.5,
            weigth=10
            )
    
    input_size, output_size, pad_size, tile_corners = get_sizes(im_size)
    gen_d = DirectoryImgGenerator(main_dir, fill_mask, weight_params)
    gen = ImageMaskGenerator(gen_d, 
                             transform_ags, 
                             pad_size,
                             input_size,
                             tile_corners,
                             batch_size=1)
    
    
    assert gen.output_size == output_size
    
    
    
    
    #%%
    batch_x, DD = next(gen)
    batch_y = DD[:,:,:,:-1]
    batch_w = DD[:,:,:,-1][:,:,:,None]
    for ii, (X,Y,W) in enumerate(zip(batch_x, batch_y, batch_w)):
        xx = np.squeeze(X)
        bot = np.min(xx)
        top = np.max(xx)
        
        plt.figure(figsize=(12,4))
        plt.subplot(1,3,1)
        plt.imshow(xx, cmap='gray')
        plt.subplot(1,3,2)
        
        I_y = xx.copy()
        patch = (Y[:,:,0]*(top-bot))+bot
        I_y[gen.pad_size:-gen.pad_size, gen.pad_size:-gen.pad_size] = patch        
        plt.imshow(I_y, cmap='gray')
        
        plt.subplot(1,3,3)
        
        I_w = xx.copy()
        patch = (W[:,:,0]*(top-bot))+bot
        I_w[gen.pad_size:-gen.pad_size, gen.pad_size:-gen.pad_size] = patch        
        plt.imshow(I_w)
#%%
    
    #%%
    import tensorflow as tf
    
    sess = tf.InteractiveSession()
    
    output_w = _to_tensor(DD, DD.dtype)
    target = _to_tensor(Y[::-1], DD.dtype)
    
    
    
    tf.global_variables_initializer().run()
    mm = dd.eval()
#%%
#    K = keras.backend
#    output = K._to_tensor()
#    
#    
#    # scale preds so that the class probas of each sample sum to 1
#    output /= K.reduce_sum(output,
#                            axis=len(output.get_shape()) - 1,
#                            keep_dims=True)
#    # manual computation of crossentropy
#    epsilon = _to_tensor(_EPSILON, output.dtype.base_dtype)
#    output = tf.clip_by_value(output, epsilon, 1. - epsilon)
#    return - tf.reduce_sum(target * tf.log(output),
#                           axis=len(output.get_shape()) - 1)



        
