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

import matplotlib.pylab as plt
from tierpsy.helper.params import read_microns_per_pixel
from tierpsy.analysis.ske_create.helperIterROI import getROIfromInd

from scipy.ndimage.filters import laplace, median_filter, gaussian_filter


mask_file = '/Users/ajaver/OneDrive - Imperial College London/aggregation/N2_1_Ch1_29062017_182108_comp3.hdf5'
feat_file = mask_file.replace('.hdf5', '_featuresN.hdf5')


microns_per_pixel = read_microns_per_pixel(feat_file)

with pd.HDFStore(feat_file, 'r') as fid:
    trajectories_data = fid['/trajectories_data']
    

#%%
skel_data = trajectories_data[(trajectories_data['skeleton_id'] >= 0)]
skel_g = skel_data.groupby('worm_index_joined')
with tables.File(feat_file, 'r') as fid:
    skel_h = fid.get_node('/coordinates/skeletons')[:, 0, 0]
#%%
traj_with_gaps = skel_data.loc[np.isnan(skel_h), 'worm_index_joined'].unique()


w_ind = 264

worm_d = skel_g.get_group(w_ind)
#%%
gaps, = np.where(np.isnan(skel_h[worm_d['skeleton_id']]))
#%%
with tables.File(feat_file, 'r') as fid:
    skel_id = worm_d['skeleton_id'].values
    skel_w = fid.get_node('/coordinates/widths')[skel_id, :]
    skel_w /= microns_per_pixel
    
    skeletons = fid.get_node('/coordinates/skeletons')[skel_id, :, :]
    
#%%
skel_length = np.sum(np.linalg.norm(np.diff(skeletons, axis=1), axis=2), axis=1)/microns_per_pixel
n_segments = skeletons.shape[1]
o_segment_length = np.nanmedian(skel_length)/(n_segments-1)
#%%

skel_w_avg = np.nanmean(skel_w,axis=0)
#%% Read worm and skeleton
#inefficient but we can use it as a test

ini_f = 1947 #1700#
row, worm_roi, roi_corner = getROIfromInd(mask_file, 
                                          trajectories_data, 
                                          frame_number = ini_f, 
                                          worm_index = w_ind, 
                                          roi_size = -1
                                          )
worm_roi = worm_roi.astype(np.float32)
with tables.File(feat_file, 'r') as fid:
    skel_id = skel_id = int(row['skeleton_id'])
    skel = fid.get_node('/coordinates/skeletons')[skel_id]
    
    skel /= microns_per_pixel
    skel -= roi_corner[ None, :] + 0.5
    
plt.figure()
plt.imshow(worm_roi, interpolation=None, cmap='gray')
plt.plot(skel[..., 0], skel[..., 1])
plt.plot(skel[0, 0], skel[0, 1], 'o')
#%%
roi_size = worm_roi.shape[0]
n_segments = skel.shape[0]

skel_w = torch.from_numpy(skel_w_avg + 0.25)
skel_w = Variable(skel_w)


skel_c = torch.from_numpy(skel)
skel_c = Variable(skel_c) 

#%%

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

def optimize_cnt(worm_img, skel_prev, skel_width, segment_length,  n_epochs = 1000):
    
    
    #this is the variable that is going t obe modified
    skel_r = skel_prev.data #+ torch.zeros(*skel_prev.size()).normal_()
    skel_r = torch.nn.Parameter(skel_r)
    
    optimizer = optim.Adam([skel_r], lr=0.1)
    for ii in range(n_epochs):
        skel_map = get_skel_map(skel_r, skel_width)
        #skel_map += 1e-3
        
        p_w = (skel_map*worm_img)
        
        skel_map_inv = (-skel_map).add_(1)
        worm_img_inv = (-worm_img).add_(1)
        p_bng = (skel_map_inv*worm_img_inv)
        
        #p_bng = torch.sqrt(p_bng)
        
        
        #c_loss = F.binary_cross_entropy(p_w, p_bng)
        c_loss = -(p_bng*torch.log(p_w + 1.e-3) + p_w*torch.log(p_bng + 1.e-3)).mean()
        
        ds = skel_r[1:] - skel_r[:-1]
        dds = ds[1:] - ds[:-1]
        #seg_mean = seg_sizes.mean()
        
        cont_loss = ds.norm(p=2)
        curv_loss = dds.norm(p=2)
        
        seg_sizes = ((ds).pow(2)).sum(1).sqrt()
        d1 = seg_sizes-segment_length*0.9
        d2 = seg_sizes-segment_length*1.5
        seg_loss = (torch.exp(-d1) + torch.exp(d2)).mean()
        
        
        #(seg_sizes-segment_length).cosh().mean()
        #seg_loss = ((seg_sizes - segment_length)).cosh().mean()
        #seg_mean_loss = ((seg_mean-seg_sizes).abs() + 1e-5).mean()
        
        loss = 100*c_loss + 50*seg_loss + cont_loss +  curv_loss
        #loss = 50*c_loss + seg_loss
        optimizer.zero_grad()
        loss.backward()
        
        #torch.nn.utils.clip_grad_norm([skel_r], 0.001)
        optimizer.step()
        
        if ii % 250 == 0:
            print(ii,
                  loss.data[0], 
                  c_loss.data[0],
                  seg_loss.data[0], 
                  cont_loss.data[0],
                  curv_loss.data[0]
                  )
    return skel_r, skel_map
         
#%%
results = []
skel_prev = skel_c.clone()
for tt in [10]:#range(1, 8, 2):#range(3, 50, 3):
    print('W {}'.format(tt))
    row, worm_roi, roi_corner = getROIfromInd(mask_file, 
                                              trajectories_data, 
                                              frame_number = ini_f + tt, 
                                              worm_index = w_ind, 
                                              roi_size=-1
                                              )
#%%
    w_roi = worm_roi.astype(np.float32)
    valid_pix = w_roi[w_roi!=0]
    bot = valid_pix.min()
    top = valid_pix.max()
    w_roi[w_roi==0] = top
    w_roi = (w_roi-bot)/(top-bot+1) + 1e-3
    
    
    dm = gaussian_filter(w_roi, 1, mode='reflect')
    #dm = median_filter(w_roi, 5, mode='reflect')
    dl = laplace(dm, mode='reflect')
    dl = np.abs(dl)
    w_roi_border = gaussian_filter(dl, 1, mode='reflect')
    
    dd = dm #+ w_roi_border
    dd = dd - dd.min()
    dd = dd/dd.max()
    #plt.imshow(dd)
    #%%
    w_roi = dd
    #%%
    #plt.imshow(w_roi_border, interpolation='none', cmap='gray')
    
    #%%
    w_roi = Variable(torch.from_numpy(w_roi))
    #w_roi_border = Variable(torch.from_numpy(w_roi_border))
    
    
#%%    
    skel_r, skel_map = optimize_cnt(w_roi, 
                                    skel_prev,
                                    skel_w/4,
                                    o_segment_length,  
                                    n_epochs = 500
                                    )
    
    
    results.append((skel_r, skel_map))
    
    
    ss = skel_r.data.numpy()
    sp = skel_prev.data.numpy()
    
    plt.figure()
    plt.imshow(worm_roi, interpolation=None, cmap='gray')
    plt.plot(sp[:, 0], sp[:, 1], '-')
    plt.plot(ss[:, 0], ss[:, 1], '.-')
    
    
    skel_prev = Variable(skel_r.data)
    break
#%%
skel_r, skel_map = results[-1]
    
D = w_roi.data.numpy()
M = skel_map.data.numpy()

plt.figure()
plt.subplot(2,2,1)
plt.imshow(D, interpolation=None, cmap='gray')
s_ori = skel_c.data.numpy()
plt.plot(s_ori[:, 0], s_ori[:, 1], '.-')
s_new = skel_r.data.numpy()
plt.plot(s_new[:, 0], s_new[:, 1], '.-')

plt.subplot(2,2,2)
plt.imshow(M, interpolation=None, cmap='gray')
plt.subplot(2,2,3)
plt.imshow(D*M, interpolation=None, cmap='gray')

plt.subplot(2,2,4)
plt.imshow((1-D)*(1-M), interpolation=None, cmap='gray')
#%%


#plt.figure()
#plt.subplot(1,2,1)
#skel_r, skel_map = results[0]
#M = skel_map.data.numpy()
#plt.imshow(M, interpolation=None, cmap='gray')
#
#plt.subplot(1,2,2)
#skel_r, skel_map = results[14]
#M = skel_map.data.numpy()
#plt.imshow(M, interpolation=None, cmap='gray')
#

#%%
#roi_generator = generateMoviesROI(mask_file, trajectories_data, roi_size=128)
#frame_data = next(roi_generator)
#for irow, (img_roi, roi_corner) in frame_data.items():
#    img_roi_N = (img_roi.astype(np.float32)-90)/255
#    row = trajectories_data.loc[irow]
#    plt.figure()
#    plt.imshow(img_roi_N, interpolation=None, cmap='gray')
#    
#    skel_id = int(row['skeleton_id'])
#    if skel_id > 0:
#        with tables.File(feat_file, 'r') as fid:
#            skel = fid.get_node('/coordinates/skeletons')[skel_id]
#            skel /= microns_per_pixel
#            skel -= roi_corner[ None, :]
#            plt.plot(skel[..., 0], skel[..., 1])
#            plt.plot(skel[0, 0], skel[0, 1], 'o')