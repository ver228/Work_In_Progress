#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 22:13:20 2017

@author: ajaver
"""
import os
import numpy as np
import torch
from torch import nn
from torch.autograd import Variable

_f_dir = os.path.dirname(os.path.realpath(__file__))
_eigenworms_f = os.path.join(_f_dir, 'pca_components.npy')
_eigenworms_n = np.load(_eigenworms_f)
eigenworms_components_full = torch.from_numpy(_eigenworms_n).float()

#%%
class EigenWorms(nn.Module):
    def __init__(self, n_components = 6):
        super().__init__()
        self.eigen_components = nn.Parameter(eigenworms_components_full[:n_components], requires_grad=False)
        self.n_angles = self.eigen_components.size(1)
        
    def _unwrap_t(self, angles):
        '''
        unwrap angles, adapted from https://github.com/numpy/numpy/blob/v1.13.0/numpy/lib/function_base.py#L2118-L2170
        '''
        
        d_angles = angles[:, 1:] - angles[:, :-1]
        
        ddmod = torch.remainder(d_angles + np.pi, 2*np.pi) - np.pi
        
        good = (ddmod == -np.pi) * (d_angles > 0) #instead of &
        ddmod[good] = np.pi
        
        ph_correct = ddmod - d_angles
        ph_correct[d_angles.abs() < np.pi] = 0
        ph_correct = ph_correct.cumsum(1)
        ph_correct += angles[:, 1:]
        
        angles[:, 1:] = ph_correct
        
    def transform(self, skels):
        
        d_skels = skels[:, 1:, :] - skels[:, :-1, :]
        
        segment_len = (d_skels**2).sum(2).sqrt().mean(1)
        
        angles = torch.atan2(d_skels[:, :, 0], d_skels[:, :, 1])
        
        self._unwrap_t(angles)
        
        mean_angle = angles.mean(1)
        angles -= angles.mean(1).view(-1, 1)
        
        eigenworms = torch.matmul(angles, self.eigen_components.t())
        
        head_coords = skels[:, 0, :].contiguous()
    
        return head_coords, segment_len, mean_angle, eigenworms

    def invert(self, head_coords, segment_len, mean_angle, eigenworms):
        
        angles = torch.matmul(eigenworms, self.eigen_components)
        angles += mean_angle.view(-1, 1)
        
        ske_x = torch.sin(angles).view(-1, self.n_angles, 1)
        ske_y = torch.cos(angles).view(-1, self.n_angles, 1)
        skels_n = torch.cat([ske_x, ske_y], 2)*segment_len.view(-1, 1, 1)
        
        skels_n = torch.cat([head_coords.view(-1, 1, 2),  skels_n], 1)
        skels_n = torch.cumsum(skels_n, dim=1) 
        
        return skels_n
#%%
class SkeletonsMaps(nn.Module):
    def __init__(self, roi_size = 128, n_segments = 49):
        super().__init__()
        
        self.roi_size = roi_size
        self.n_segments = n_segments
        
        X_grid = torch.arange(0, roi_size).view(1, -1).expand(1, 1, roi_size, roi_size)
        Y_grid = torch.arange(0, roi_size).view(-1, 1).expand(1, 1, roi_size, roi_size)
        
        self.X_grid = nn.Parameter(X_grid.contiguous(), requires_grad=False)
        self.Y_grid = nn.Parameter(Y_grid.contiguous(), requires_grad=False)

    def forward(self, skel_coord, skel_width):
        skel_coord = skel_coord.view(-1, 49, 2, 1, 1)
        mu_x = skel_coord[:, :, 0] 
        mu_y = skel_coord[:, :, 1]
        sigma = skel_width.view(1, 49, 1, 1)
        
        dx = self.X_grid.view(1, 1, 128, 128) - mu_x
        dy = self.Y_grid.view(1, 1, 128, 128) - mu_y
        
        skel_maps = (-(dx.pow(2) + dy.pow(2))/(2*sigma.pow(2))).exp_()
        skel_map = skel_maps.sum(1).clamp(0,1)
        
        return skel_map

#%%
if __name__ == '__main__':
    import pandas as pd
    import tables
    from tierpsy.helper.params import read_microns_per_pixel
    from tierpsy.analysis.ske_create.helperIterROI import getROIfromInd

    #mask_file = '/Users/ajaver/OneDrive - Imperial College London/aggregation/N2_1_Ch1_29062017_182108_comp3.hdf5'
    mask_file = '/data/ajaver/onedrive/aggregation/N2_1_Ch1_29062017_182108_comp3.hdf5'
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
        
        skeletons = fid.get_node('/coordinates/skeletons')[skel_id, :, :]/microns_per_pixel
        skel_ss = skeletons[~np.isnan(skeletons[:, 0, 0])]
        
        
    #%%
    skel_length = np.sum(np.linalg.norm(np.diff(skeletons, axis=1), axis=2), axis=1)
    n_segments = skeletons.shape[1]
    
    #%%
    o_segment_length = np.nanmedian(skel_length)/(n_segments-1)
    skel_w_avg = np.nanmean(skel_w,axis=0)

    
    #%%
    is_cuda = True
    skels = torch.from_numpy(skeletons)
    skel_width = torch.from_numpy(skel_w_avg)
    eig = EigenWorms(6)
    s_map = SkeletonsMaps()
    
    if is_cuda:
        skels = skels.cuda()
        skel_width = skel_width.cuda()
        eig = eig.cuda()
        s_map = s_map.cuda()
        
    skels = Variable(skels)
    skel_width = Variable(skel_width)
    
    
    DT = eig.transform(skels)
    skels_n = eig.invert(*DT)
    
    #%%
    import matplotlib.pylab as plt
    frame_i = 1800
    ss = skels.data.cpu().numpy()[frame_i]
    ss_n = skels_n.data.cpu().numpy()[frame_i]
    plt.plot(ss[:,1], ss[:,0])
    plt.plot(ss_n[:,1], ss_n[:,0])
    plt.axis('equal')
    
    #%%
    ini_f = worm_d['frame_number'].min() + 1800
    
    worm_roi_s = []
    roi_corner_s = []
    for tt in range(32):
        print('W {}'.format(tt))
        row, worm_roi, roi_corner = getROIfromInd(mask_file, 
                                                  trajectories_data, 
                                                  frame_number = ini_f + tt, 
                                                  worm_index = w_ind, 
                                                  roi_size=128
                                                  )
        worm_roi_s.append(worm_roi)
        roi_corner_s.append(roi_corner)
    
    #%%
    dd = torch.from_numpy(np.vstack(roi_corner_s)).float()
    if is_cuda:
        dd = dd.cuda()
    
    skel_ss = skels[frame_i:frame_i+32] - Variable(dd.view(-1, 1, 2))
    
    
    sm = s_map(skel_ss, skel_width/4)
    
    #%%
    ss = skel_ss.cpu().data[-1].numpy()
    mm = sm.data.cpu().numpy()[-1]
    plt.figure()
    
    plt.subplot(1,2,1)
    plt.imshow(worm_roi)
    plt.plot(ss[:, 0], ss[:,1])
    
    plt.subplot(1,2,2)
    plt.imshow(mm)
    plt.plot(ss[:, 0], ss[:,1])
    #%%
    from models import AE
    
    mod = AE(256)
    
    #%%
    worm_roi_ss = np.vstack([x[None, None, ...] for x in worm_roi_s])
    
    ww = Variable(torch.from_numpy(worm_roi_ss)).float()