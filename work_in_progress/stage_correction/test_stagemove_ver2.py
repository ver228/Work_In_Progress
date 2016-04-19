# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 22:01:59 2016

@author: ajaver
"""

import h5py
import tables
import os
import numpy as np
import matplotlib.pylab as plt
from scipy.io import loadmat
import glob
import os
#import pandas as pd

delT = 15

#30 28 20 19

main_dir = '/Users/ajaver/Desktop/Videos/single_worm/agar_3/MaskedVideos/'

from MWTracker.featuresAnalysis.obtainFeaturesHelper import WormFromTable
from MWTracker.featuresAnalysis.obtainFeatures import getMicronsPerPixel, getFPS

files = glob.glob(os.path.join(main_dir, '*.hdf5' ))
files = sorted(files)
#%%
# agar_1 -> 41, 39
# agar_3 -> 23
# agar_4 -> 26, 33, 34

for mask_id in [30, 28, 20, 19]:#range(len(files)):
    masked_image_file = files[mask_id]
    skeletons_file = masked_image_file.replace('MaskedVideos', 'Results')[:-5] + '_skeletons.hdf5'
    feat_file = masked_image_file.replace('MaskedVideos', 'Results')[:-5] + '_features.hdf5'
    segworm_feat_file = masked_image_file.replace('MaskedVideos', 'Features')[:-5] + '_features.mat'

#%%
    print(mask_id, masked_image_file)
    
#    fps, is_default_timestamp = getFPS(skeletons_file, 25)
#    micronsPerPixel = getMicronsPerPixel(skeletons_file)
#    
#    worm = WormFromTable(skeletons_file, 1, \
#        use_skel_filter = True, use_manual_join = False, \
#        micronsPerPixel = 1,fps=fps, smooth_window = 5)
#    
#    continue
    try:
        with tables.File(feat_file, 'r') as fid:
            if '/features_means' in fid and \
            fid.get_node('/features_means').attrs['has_finished'] and \
            fid.get_node('/features_timeseries').shape[0]>0:
                skeletons = fid.get_node('/skeletons')[:]
                frame_range = fid.get_node('/features_events/worm_1')._v_attrs['frame_range']
            
            #pad the beginign with np.nan to have the same reference as segworm
            skeletons = np.pad(skeletons, [(frame_range[0],0), (0,0), (0,0)], 
                           'constant', constant_values=np.nan)
    except (OSError):
        continue
    
    
    
    if os.path.exists(segworm_feat_file):
        fvars = loadmat(segworm_feat_file)
        micronsPerPixels_x = fvars['info']['video'][0][0]['resolution'][0][0]['micronsPerPixels'][0][0]['x'][0][0][0][0]
        micronsPerPixels_y = fvars['info']['video'][0][0]['resolution'][0][0]['micronsPerPixels'][0][0]['y'][0][0][0][0]
        
        segworm_x = -fvars['worm']['posture'][0][0]['skeleton'][0][0]['x'][0][0].T
        segworm_y = -fvars['worm']['posture'][0][0]['skeleton'][0][0]['y'][0][0].T
        
        #%%
        # it seems there is a bug in segworm and the flag for dropped frames is the same as stage movements...
        #FLAG_DROPPED = 2;
        #FLAG_STAGE = 3;
        frame_annotations = fvars['info']['video'][0][0]['annotations'][0][0]['frames'][0][0][0];
        
        
        
        #%%
        
        max_n_skel = min(segworm_x.shape[0], skeletons.shape[0])
        
        #%%
        seg_x = segworm_x
        seg_y = segworm_y
                
        skel_x = skeletons[:,:,0];
        skel_y = skeletons[:,:,1];
        
        dXo = skel_x[:max_n_skel] - seg_x[:max_n_skel]
        dYo = skel_y[:max_n_skel] - seg_y[:max_n_skel]
        
        shift_x = np.nanmedian(dXo)
        shift_y = np.nanmedian(dYo)
        
        #skel_x -= shift_x
        #skel_y -= shift_y
        #%%        
#        pos_coord = ((x_sign*XX, y_sign*YY) for XX, YY in \
#        [(skel_x_ori, skel_y_ori), (skel_y_ori, skel_x_ori)] \
#        for x_sign in (1,-1) for y_sign in (1,-1))
#        
#        R_min = np.inf
#        
#        for XX, YY in pos_coord:
#            dXo = XX[:max_n_skel] - seg_x[:max_n_skel]
#            dYo = YY[:max_n_skel] - seg_y[:max_n_skel]
#            
#            shift_x = np.nanmedian(dXo)
#            shift_y = np.nanmedian(dYo)
#            
#            #print(shift_x, shift_y)
#            dX = dXo - shift_x
#            dY = dYo - shift_y
#            
#            
#            R = dX*dX + dY*dY
#            
#            R_tot = np.nanmean(R)
#            if R_tot < R_min:
#                skel_x, skel_y = XX - shift_x, YY - shift_y
#                R_min = R_tot
#                R_error = R
        
        #%%
        
        dX = skel_x[:max_n_skel] - seg_x[:max_n_skel]
        dY = skel_y[:max_n_skel] - seg_y[:max_n_skel]
        R_error = dX*dX + dY*dY
        
        skel_error = np.sqrt(np.mean(R_error, axis=1))
                
        
        #%%
        w_xlim = w_ylim = (-10, skel_error.size+10)
        
        plt.figure()
        plt.subplot(3,1,1)
        plt.plot(skel_error, '.')
        plt.ylim((0, np.nanmax(skel_error)))
        plt.xlim(w_xlim)
        plt.title(mask_id)
        plt.ylabel('Error')
        
        plt.subplot(3,1,2)
        plt.plot(skel_y[:,1], 'b') 
        plt.plot(seg_y[:,1], 'r')
        plt.xlim(w_ylim)
        plt.ylabel('Y coord')
        
        plt.subplot(3,1,3)
        plt.plot(skel_x[:,1], 'b') 
        plt.plot(seg_x[:,1], 'r')
        plt.xlim(w_xlim)
        plt.ylabel('X coord')
        plt.xlabel('Frame Number')
        #%%
        plt.figure()
        #plt.subplot(3,1,1)        
        plt.plot(skel_x[::delT].T, skel_y[::delT].T, 'b')    
        plt.plot(seg_x[::delT].T, seg_y[::delT].T, 'r')
        plt.axis('equal')
        plt.title(mask_id)
        #%%
    else:
        plt.figure()
        plt.title(mask_id)
        plt.plot(skeletons[::delT,:, 0].T, skeletons[::delT,:, 1].T, 'b') 
        plt.axis('equal')
        #%%
    #%%
