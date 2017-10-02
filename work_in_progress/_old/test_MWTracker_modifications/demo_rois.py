# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 21:57:30 2015

@author: ajaver
"""
import pandas as pd
import matplotlib.pylab as plt
from tierpsy.analysis.ske_create.helperIterROI import generateMoviesROI
from tierpsy.analysis.ske_create.getSkeletonsTables import getWormMask
from tierpsy.analysis.traj_create.getBlobTrajectories import _thresh_bw

masked_file = "/Volumes/behavgenom_archive$/Avelino/screening/CeNDR/MaskedVideos/CeNDR_Exp_250417/BRC20067_worms10_food1-3_Set4_Pos5_Ch2_25042017_140346.hdf5"
skeletons_file = masked_file.replace('MaskedVideos', 'Results').replace('.hdf5', '_skeletons.hdf5')

with pd.HDFStore(skeletons_file, 'r') as fid:
    trajectories_data = fid['/trajectories_data']
    
roi_generator = generateMoviesROI(masked_file, trajectories_data)

worms_in_frame = next(roi_generator)

for row in worms_in_frame:
    worm_img, roi_corner = worms_in_frame[row]
    row_data = trajectories_data.loc[row]
    worm_mask, worm_cnt, _ = getWormMask(worm_img, 
                                 row_data['threshold'], 
                                 5)

    plt.figure()
    plt.subplot(1,2,1)
    plt.imshow(worm_img, interpolation=None, cmap='gray')
    plt.subplot(1,2,2)
    plt.imshow(worm_mask, interpolation=None, cmap='gray')
    break
    

#import h5py
#import pandas as pd
#import numpy as np
#from skimage.filters import threshold_otsu
#from scipy.signal import medfilt
#import os
#
#from MWTracker.trackWorms.getSkeletonsTables import getWormMask, binaryMask2Contour, getWormROI
#
##/Users/ajaver/Desktop/Videos/Avelino_17112015/MaskedVideos/CSTCTest_Ch1_17112015_205616.hdf5 file_mask = '/Users/ajaver/Desktop/Videos/Avelino_17112015/MaskedVideos/CSTCTest_Ch1_17112015_205616.hdf5'
##file_mask = '/Users/ajaver/Desktop/Videos/tiffs/MaskedVideos/recording 8.1_X1.hdf5'
#
#
#
#file_skel = file_mask.replace('MaskedVideos', 'Results').replace('.hdf5', '_skeletons.hdf5')
#file_traj = file_mask.replace('MaskedVideos', 'Results').replace('.hdf5', '_trajectories.hdf5')
#assert(os.path.exists(file_mask))
#assert(os.path.exists(file_traj))
#assert(os.path.exists(file_skel))
#
#
#with pd.HDFStore(file_skel, 'r') as fid:
#    trajectories_data = fid['/trajectories_data']
#
##with pd.HDFStore(file_traj, 'r') as fid:
##    plate_worms = fid['/plate_worms']
#
#current_frame = 1#2074#261
#with h5py.File(file_mask, 'r') as fid:
#    img = fid['/mask'][current_frame]
#
#row_data = trajectories_data[trajectories_data['frame_number'] == current_frame]
#row_data = row_data.iloc[0]
#
#
#worm_img, roi_corner = getWormROI(img, row_data['coord_x'], row_data['coord_y'], row_data['roi_size'])
#min_mask_area = row_data['area']/2
#
#worm_mask, worm_cnt, _ = getWormMask(worm_img, row_data['threshold'], 10, min_mask_area)
#
##worm_cnt, _ = binaryMask2Contour(worm_mask, min_mask_area = min_mask_area)
#
#
#
#plt.figure()
#plt.imshow(worm_mask, interpolation = 'none', cmap = 'gray')
##plt.plot(worm_cnt[:,0], worm_cnt[:,1], 'r')
#plt.xlim([0, worm_mask.shape[1]])
#plt.ylim([0, worm_mask.shape[0]])
#plt.grid('off')
#
#
