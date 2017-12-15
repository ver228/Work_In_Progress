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

import glob
from models import AE

from worm_models import SkeletonsMaps, EigenWorms 

if __name__ == '__main__':
    import pandas as pd
    import tables
    from tierpsy.helper.params import read_microns_per_pixel
    from tierpsy.analysis.ske_create.helperIterROI import getROIfromInd

    #load model
    model_dir_root = '/data/ajaver/onedrive/classify_strains/logs/worm_autoencoder'
    dnames = glob.glob(os.path.join(model_dir_root, 'AE_L64*'))
    d = dnames[0]
    embedding_size = int(d.split('AE_L')[-1].partition('_')[0])
    model_path = os.path.join(d, 'checkpoint.pth.tar')
    print(embedding_size)
    model = AE(embedding_size)
    
    
    checkpoint = torch.load(model_path, map_location=lambda storage, loc: storage)
    model.load_state_dict(checkpoint['state_dict'])
    model.eval()
    
    #%%
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
    
    
    
    with tables.File(feat_file, 'r') as fid:
        skel_id = worm_d['skeleton_id'].values
        skel_w = fid.get_node('/coordinates/widths')[skel_id, :]
        skel_w /= microns_per_pixel
        
        skeletons = fid.get_node('/coordinates/skeletons')[skel_id, :, :]/microns_per_pixel
        skel_ss = skeletons[~np.isnan(skeletons[:, 0, 0])]
        
        
    
    skel_length = np.sum(np.linalg.norm(np.diff(skeletons, axis=1), axis=2), axis=1)
    n_segments = skeletons.shape[1]
    
    o_segment_length = np.nanmedian(skel_length)/(n_segments-1)
    skel_w_avg = np.nanmean(skel_w,axis=0)
    #%%
    def shift_and_normalize(data):
        '''
        shift worms values by an approximation of the removed background. I used the top95 of the unmasked area. 
        I am assuming region of the background is kept.
        '''
        data_m = data.view(np.ma.MaskedArray)
        data_m.mask = data==0
        if data.ndim == 3:
            sub_d = np.percentile(data, 95, axis=(1,2)) #let's use the 95th as the value of the background
            data_m -= sub_d[:, None, None]
        else:
            sub_d = np.percentile(data, 95)
            data_m -= sub_d
            
        data /= 255
        return data
    
    worm_roi_s = []
    roi_corner_s = []
    del_t = 3
    for tt in range(-del_t, 32*del_t, del_t):
        print('W {}'.format(tt))
        row, worm_roi, roi_corner = getROIfromInd(mask_file, 
                                                  trajectories_data, 
                                                  frame_number = ini_f + tt, 
                                                  worm_index = w_ind, 
                                                  roi_size = 128
                                                  )
        if tt < 0:
            skel_seed = skeletons[ini_f - worm_d['frame_number'].min()]
            skel_seed -= roi_corner[None, :]
        else:
            worm_roi_s.append(worm_roi[None, :, :]) 
            roi_corner_s.append(roi_corner)
    worm_roi_s = np.array(worm_roi_s)
    
    
    
    worm_roi_s = shift_and_normalize(worm_roi_s.astype(np.float))
    #%%
    plt.figure(figsize=(7,7))
    plt.imshow(worm_roi_s[0].squeeze(), cmap='gray')
    plt.plot(skel_seed[:, 0], skel_seed[:, 1])
    
    #%%
    worm_roi_t = torch.from_numpy(worm_roi_s).float()
    skel_width = torch.from_numpy(skel_w_avg/4).float()
    s_seed = torch.from_numpy(skel_seed[None, :]).expand(worm_roi_s.shape[0], 49, 2).contiguous()
    
    s_map = SkeletonsMaps()
    
    worm_roi_t = worm_roi_t.cuda()
    s_seed = s_seed.cuda()
    skel_width = skel_width.cuda()
    model = model.cuda()
    s_map = s_map.cuda()
    
    worm_roi_t = Variable(worm_roi_t)
    s_seed = Variable(s_seed)
    skel_width = Variable(skel_width)
    #%%
    maps_o = s_map(s_seed, skel_width)
    mm = maps_o - worm_roi_t
    #%%
    bot = worm_roi_t.min()
    top = worm_roi_t.max()
    worm_roi_n = (worm_roi_t.squeeze() - bot)/(top-bot)
    
    
    p_w = (maps_o*worm_roi_n) + 1.e-5
    
    skel_map_inv = (-maps_o).add_(1)
    worm_img_inv = (-worm_roi_n.squeeze()).add_(1)
    p_bng = (skel_map_inv*worm_img_inv) + 1.e-5
    
    #p_bng = torch.sqrt(p_bng)
    
    
    #c_loss = F.binary_cross_entropy(p_w, p_bng)
    c_loss = -(p_bng*torch.log(p_w) + p_w*torch.log(p_bng)).mean()