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
from scipy.ndimage.filters import laplace, median_filter, gaussian_filter

import matplotlib.pylab as plt
from tierpsy.helper.params import read_microns_per_pixel
from tierpsy.analysis.ske_create.helperIterROI import getROIfromInd


EIGENWORMS_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pca_components.npy')
EIGENWORMS_COMPONENTS = np.load(EIGENWORMS_FILE)
EIGENWORMS_COMPONENTS = EIGENWORMS_COMPONENTS.astype(np.float32)
#%%
EIGENWORMS_COMPONENTS_T = Variable(torch.from_numpy(EIGENWORMS_COMPONENTS))
#%%

def _h_eigenworms_full(skeleton, n_components = 4):
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
def sample_skels(seed_skel, search_ranges, n_components = 6, n_grids = 2000):
    #convert to eigenworms
    DT = _h_eigenworms_full(seed_skel, n_components)
    head_x, head_y, segment_l, mean_angle, eigenworms = DT
    
    #sample from grid
    dx = head_x + np.random.uniform(*search_ranges['x'], size = n_grids)
    dy = head_y + np.random.uniform(*search_ranges['y'], size = n_grids)
    d_ang = mean_angle + np.random.uniform(*search_ranges['ang'], size = n_grids)
    d_seg = segment_l*np.random.uniform(*search_ranges['seg'], size = n_grids)
    
    d_eig1 = eigenworms[:4, None] + np.random.uniform(*search_ranges['eig'], size = (4,n_grids))
    
    eig_56 = [x/2 for x in search_ranges['eig']]
    d_eig2 = eigenworms[4:, None] + np.random.uniform(*eig_56, size = (2,n_grids))
    
    d_eig = np.vstack((d_eig1, d_eig2)).T
    

    angles = np.dot(d_eig, EIGENWORMS_COMPONENTS[:n_components])
    angles += d_ang[:, None]
    
    ske_x = np.sin(angles)*d_seg[:, None]
    ske_x = np.hstack((dx[:, None],  ske_x))
    ske_x = np.cumsum(ske_x, axis=1)
    
    
    ske_y = np.cos(angles)*d_seg[:, None]
    ske_y = np.hstack((dy[:, None],  ske_y))
    ske_y = np.cumsum(ske_y, axis=1)
    
    skels_n = np.concatenate((ske_x[..., None], ske_y[..., None]), axis=2).astype(np.float32)
    
    
    return skels_n

def get_loss_from_map(skel, skel_w):
    skel_map = get_skel_map(skel, skel_w)
    
    p_w = (skel_map*w_roi)
    
    skel_map_inv = (-skel_map).add_(1)
    worm_img_inv = (-w_roi).add_(1)
    p_bng = (skel_map_inv*worm_img_inv)
    c_loss = -(p_bng*torch.log(p_w + 1.e-3) + p_w*torch.log(p_bng + 1.e-3)).mean()
    
    return c_loss.data[0]
#%%
def _get_laplacian_border(w_roi):
    dm = gaussian_filter(w_roi, 1, mode='reflect')
    #dm = median_filter(w_roi, 3, mode='reflect')
    dl = laplace(dm, mode='reflect')
    w_roi_border = np.abs(dl)
    bot = w_roi_border.min()
    top = w_roi_border.max()
    w_roi_border = (w_roi_border-bot)/(top-bot+1) + 1e-3
    return w_roi_border


if __name__ == '__main__':
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
        
    
    skel_length = np.sum(np.linalg.norm(np.diff(skeletons, axis=1), axis=2), axis=1)/microns_per_pixel
    n_segments = skeletons.shape[1]
    
    
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
    roi_size = worm_roi.shape[0]
    n_segments = skel.shape[0]
    
    
    #%% get grid
    #I need to make an object here...
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
    n_iter = 1
    beam_size = 3
    
    ini_search = {
            'x': (-5,5),
            'y': (-2,2),
            'ang': (-np.pi/16, np.pi/16),
            'seg': (0.97, 1.03),
            'eig': (-0.5, 0.5)
            }
    
#    ini_search = {
#            'x': (-7,7),
#            'y': (-7,7),
#            'ang': (-np.pi/8, np.pi/8),
#            'seg': (0.5, 1.5),
#            'eig': (-2, 2)
#            }
    
    factor_n = 1.
    skel_seeds = np.array([skel]*beam_size)
    search_ranges = ini_search.copy()
    skel_w = Variable(torch.from_numpy(skel_w_avg))/4
    
    
    results = []
    for tt in range(3, 100, 2):
        print('W {}'.format(tt))
    
        row, worm_roi, roi_corner = getROIfromInd(mask_file, 
                                                      trajectories_data, 
                                                      frame_number = ini_f + tt, 
                                                      worm_index = w_ind, 
                                                      roi_size=-1
                                                      )
        
        valid_max = worm_roi!=0
        w_roi = worm_roi.astype(np.float32)
        valid_pix = w_roi[valid_max]
        bot = valid_pix.min()
        top = valid_pix.max()
        w_roi[w_roi==0] = top
        w_roi = (w_roi-bot)/(top-bot+1) + 1e-3
        #w_roi = (w_roi>0.65).astype(np.float32)
        
        w_roi = Variable(torch.from_numpy(w_roi))
        #search_ranges = {k:(v[0]*factor_n, v[0]*factor_n) for k,v in search_ranges.items()}
        
        new_seeds = []
        for ii_ss, s_seed in enumerate(skel_seeds):
            print(ii_ss+1, beam_size)
            
            skels_n = sample_skels(s_seed, search_ranges, n_grids = 3000)
            skels_n = Variable(torch.from_numpy(skels_n))
            
            losses_r = []
            for ss_fi, ss_f in enumerate(skels_n):
                losses_r.append(get_loss_from_map(ss_f, skel_w))
                if ss_fi % 500 == 0:
                    print(ss_fi)
                
            losses_r = np.array(losses_r)
            
            skels_nn = skels_n.data.numpy()
            ind_o = np.argsort(losses_r)[:beam_size]
            
            new_seeds.append((losses_r[ind_o], skels_nn[ind_o]))
            
        
        top_losses, top_skels = map(np.concatenate, zip(*new_seeds))
        ind_o = np.argsort(top_losses)[:beam_size]
        skel_seeds = top_skels[ind_o]
        
        results.append((tt, worm_roi, skel_seeds))
        
    #%%
    for tt, worm_roi, skel_seeds in results:
        print(tt)
        plt.figure(figsize=(15, 5))
        #%
        for ii, ss in enumerate(skel_seeds):
            plt.subplot(1,5, ii+1)
            plt.imshow(worm_roi, interpolation=None, cmap='gray')
            plt.plot(ss[..., 0], ss[..., 1])
            plt.plot(ss[0, 0], ss[0, 1], 'o')
        plt.suptitle(tt + ini_f)
    #%%
    skel_filt = skels_nn[losses_r<0.5]
    dx = skel_filt[:,0, 0]-45 
    dy = skel_filt[:,0, 1]-33 
    rr = np.sqrt(dx**dx + dy*dy)
    
    ind_o = np.argsort(rr)[:5]
    plt.figure(figsize=(15, 5))
    
    for ii, ss in enumerate(skel_filt[ind_o]):
        plt.subplot(1,5, ii+1)
        plt.imshow(worm_roi, interpolation=None, cmap='gray')
        plt.plot(ss[..., 0], ss[..., 1])
        plt.plot(ss[0, 0], ss[0, 1], 'o')
    #%%
    ss_new = skel_filt[ind_o[0]].copy()
    ss_new[:, 0] = ss_new[:, 0]
    ss_new[:, 1] = ss_new[:, 1]
    ss_old = skel_seeds[0]
    
    plt.figure()
    plt.imshow(worm_roi, interpolation=None, cmap='gray')
    plt.plot(ss_new[..., 0], ss_new[..., 1])
    plt.plot(ss_old[..., 0], ss_old[..., 1])
    #%%
    
  
    
