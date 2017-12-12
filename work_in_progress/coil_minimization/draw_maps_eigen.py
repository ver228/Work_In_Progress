#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 17:46:42 2017

@author: ajaver
"""
import pandas as pd
import numpy as np
import tables
import torch
import torch.optim as optim
from torch.autograd import Variable
import torch.nn.functional as F
import os

import matplotlib.pylab as plt
from tierpsy.helper.params import read_microns_per_pixel
from tierpsy.analysis.ske_create.helperIterROI import getROIfromInd


EIGENWORMS_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pca_components.npy')
EIGENWORMS_COMPONENTS = np.load(EIGENWORMS_FILE)
EIGENWORMS_COMPONENTS = EIGENWORMS_COMPONENTS.astype(np.float32)
#%%
EIGENWORMS_COMPONENTS_T = Variable(torch.from_numpy(EIGENWORMS_COMPONENTS))
#%%

def _h_eigenworms_full(skeleton, n_components = 6):
    '''
    Fully transform the worm skeleton using its eigen components.
    
    The first four vectors are:
        (0,1) the change in head x,y position btw frame
        (2) the change in mean angle btw frames
        (3) each segment mean length
    
    The last six are the eigenvalues    
    
    '''
    skeleton = skeleton.astype(np.float32)
    
    dd = np.diff(skeleton, axis=0)
    
    segment_l = np.mean(np.linalg.norm(dd, axis=1))
    
    angles = np.arctan2(dd[..., 0], dd[..., 1])
    angles = np.unwrap(angles)

    mean_angle = np.mean(angles)
    angles -= mean_angle
    
    
    eigenworms = np.dot(angles, EIGENWORMS_COMPONENTS[:n_components].T)
    
    head_x, head_y = skeleton[0,:]
    
    #pack all the elments of the transform
    DT = head_x, head_y, segment_l, mean_angle, eigenworms
    
    DT = [x if isinstance(x, np.ndarray)else np.array([x]) for x in DT]
    DT = [x.astype(np.float32) for x in DT]
    
    return DT
#%%
def _h_eigenworms_inv(head_x, head_y, segment_l, mean_angle, eigenworms):
    '''
    Convert the eigen value transformed data into xy coordinates
    '''
    
    n_components = eigenworms.size
    angles = np.dot(eigenworms, EIGENWORMS_COMPONENTS[:n_components])
    angles += mean_angle
    
    ske_x = np.cos(angles)*segment_l
    ske_x = np.hstack((head_x,  ske_x))
    ske_x = np.cumsum(ske_x, axis=0) 
    
    ske_y = np.sin(angles)*segment_l
    ske_y = np.hstack((head_y,  ske_y))
    ske_y = np.cumsum(ske_y, axis=0) 
    
    skels_n = np.concatenate((ske_y[..., None], ske_x[..., None]), axis=1)
    
    return skels_n
#%%
def _h_eigenworms_inv_T(head_x, head_y, segment_l, 
                        mean_angle, eigenworms):
    '''
    Convert the eigen value transformed data into xy coordinates
    '''
    
    
    n_components = eigenworms.size(0)
    angles = torch.mm(eigenworms.view(1, -1), EIGENWORMS_COMPONENTS_T[:n_components])
    angles += mean_angle
    
    ske_x = torch.sin(angles)*segment_l
    ske_x = torch.cat([head_x.view(1,1),  ske_x], 1)
    ske_x = torch.cumsum(ske_x, dim=1) 
    
    ske_y = torch.cos(angles)*segment_l
    ske_y = torch.cat([head_y.view(1,1),  ske_y], 1)
    ske_y = torch.cumsum(ske_y, dim=1) 
    
    
    skels_n = torch.cat((ske_x.view(-1, 1), ske_y.view(-1, 1)), 1)
    
    return skels_n
#%%

#%%
mask_file = '/Users/ajaver/OneDrive - Imperial College London/aggregation/N2_1_Ch1_29062017_182108_comp3.hdf5'
feat_file = mask_file.replace('.hdf5', '_featuresN.hdf5')

w_ind = 264
ini_f = 1947

microns_per_pixel = read_microns_per_pixel(feat_file)

with pd.HDFStore(feat_file, 'r') as fid:
    trajectories_data = fid['/trajectories_data']

skel_data = trajectories_data[(trajectories_data['skeleton_id'] >= 0)]
skel_g = skel_data.groupby('worm_index_joined')
worm_d = skel_g.get_group(w_ind)
#%%
with tables.File(feat_file, 'r') as fid:
    skel_id = worm_d['skeleton_id'].values
    skel_w = fid.get_node('/coordinates/widths')[skel_id, :]
    skel_w /= microns_per_pixel
    
    skeletons = fid.get_node('/coordinates/skeletons')[skel_id, :, :]
    
#%%
skel_length = np.sum(np.linalg.norm(np.diff(skeletons, axis=1), axis=2), axis=1)/microns_per_pixel
n_segments = skeletons.shape[1]

#%%
o_segment_length = np.nanmedian(skel_length)/(n_segments-1)
skel_w_avg = np.nanmean(skel_w,axis=0)
#%% Read worm and skeleton
#inefficient but we can use it as a test

row, worm_roi, roi_corner = getROIfromInd(mask_file, 
                                          trajectories_data, 
                                          frame_number = ini_f, 
                                          worm_index = w_ind, 
                                          roi_size = -1
                                          )
worm_roi = worm_roi.astype(np.float32)
roi_size = worm_roi.shape[0]
with tables.File(feat_file, 'r') as fid:
    skel_id = skel_id = int(row['skeleton_id'])
    skel = fid.get_node('/coordinates/skeletons')[skel_id]
    
    skel /= microns_per_pixel
    skel -= roi_corner[ None, :] + 0.5
#%%
DT = _h_eigenworms_full(skel, n_components = 6)

DT = [Variable(torch.from_numpy(x)) for x in DT]
skel_f = _h_eigenworms_inv_T(*DT)
#%%

plt.figure()
plt.imshow(worm_roi, interpolation=None, cmap='gray')
plt.plot(skel[..., 0], skel[..., 1])
plt.plot(skel[0, 0], skel[0, 1], 'o')

ss = skel_f.data.numpy()
plt.plot(ss[:, 0], ss[:, 1])
#%%
roi_size = worm_roi.shape[0]
n_segments = skel.shape[0]

skel_w = torch.from_numpy(skel_w_avg + 0.25)
skel_w = Variable(skel_w)

eig_w = _h_eigenworms_full(skel, roi_size)
eigen_c = [Variable(torch.from_numpy(x)) for x in eig_w]

#%% get grid
X_grid = torch.arange(0, roi_size).view(1, 1, -1).expand(n_segments, roi_size, roi_size)
Y_grid = torch.arange(0, roi_size).view(1, -1, 1).expand(n_segments, roi_size, roi_size)
X_grid = Variable(X_grid)
Y_grid = Variable(Y_grid)

def get_skel_map(skel_coord, skel_width):
    #2D gauss 
    
    mu_x = skel_coord[:,0].contiguous().view(n_segments, 1, 1).expand_as(X_grid)
    mu_y = skel_coord[:,1].contiguous().view(n_segments, 1, 1).expand_as(X_grid)
    sigma = skel_width.view(n_segments, 1, 1).expand_as(X_grid)
    
    dx = X_grid - mu_x
    dy = Y_grid - mu_y

    dd = (-(dx*dx + dy*dy)/(2*sigma*sigma)).exp_()
    skel_map = dd.sum(0).clamp(0,1)
    
    return skel_map

#%%

#%%
def optimize_cnt(worm_img, eig_prev, skel_width, segment_length,  n_epochs = 1000):
    
    
    #this is the variable that is going t obe modified
    
    eig_r = [torch.nn.Parameter(x.data) for x in eigen_prev]#+ torch.zeros(*skel_prev.size()).normal_()
    
    
    optimizer = optim.SGD(eig_r, lr=0.01)
    for ii in range(n_epochs):
        skel_r = _h_eigenworms_inv_T(*eig_r)
        
        skel_map = get_skel_map(skel_r, skel_width)
        skel_map += 1e-3
        #%%
        p_w = (skel_map*worm_img)
        
        skel_map_inv = (-skel_map).add_(1)
        worm_img_inv = (-worm_img).add_(1)
        p_bng = (skel_map_inv*worm_img_inv)
        
        c_loss = F.binary_cross_entropy(p_w, p_bng)
        
        
        ds = skel_r[1:] - skel_r[:-1]
        dds = ds[1:] - ds[:-1]
        #seg_mean = seg_sizes.mean()
        
        cont_loss = ds.norm(p=2)
        curv_loss = dds.norm(p=2)
        
        seg_sizes = ((ds).pow(2)).sum(1).sqrt()
        seg_loss = (seg_sizes-segment_length).cosh().mean()
        
        loss = 50*c_loss #+ seg_loss #+ cont_loss/10 +  curv_loss/10
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if ii % 250 == 0:
            print(ii,
                  loss.data[0], 
                  c_loss.data[0],
                  seg_loss.data[0]
                  )
        
        #print(eig_r.data.numpy())
    return eig_r, skel_r, skel_map
         
#%%
results = []
eigen_prev = [x.clone() for x in eigen_c]
for tt in range(10, 15, 3):
    print('W {}'.format(tt))
    row, worm_roi, roi_corner = getROIfromInd(mask_file, 
                                              trajectories_data, 
                                              frame_number = ini_f + tt, 
                                              worm_index = w_ind, 
                                              roi_size=-1
                                              )

    w_roi = worm_roi.astype(np.float32)
    valid_pix = w_roi[w_roi!=0]
    bot = valid_pix.min()
    top = valid_pix.max()
    w_roi[w_roi==0] = top
    w_roi = (w_roi-bot)/(top-bot+1) + 1e-3
    

    w_roi = torch.from_numpy(w_roi)
    w_roi = Variable(w_roi)


    eig_r, skel_r, skel_map = optimize_cnt(w_roi, 
                                    eigen_prev,
                                    skel_w/4,
                                    o_segment_length,  
                                    n_epochs = 500
                                    )
    
    results.append((skel_r, skel_map))
    
    skel_r, skel_map = results[0]
    
    ss = skel_r.data.numpy()
    #sp = skel_prev.data.numpy()
    #%%
    plt.figure()
    plt.subplot(1,2,1)
    plt.imshow(worm_roi, interpolation=None, cmap='gray')
    #plt.plot(sp[:, 0], sp[:, 1], '-')
    plt.plot(ss[:, 0], ss[:, 1], '.-')
    plt.subplot(1,2,2)
    SS = skel_map
    
    #%%
    
    eigen_prev = [Variable(x.data) for x in eig_r]
    break
