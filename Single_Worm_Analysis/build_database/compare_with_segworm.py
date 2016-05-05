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

main_dir = '/Users/ajaver/Desktop/Videos/single_worm/agar_4/MaskedVideos/'

from MWTracker.featuresAnalysis.obtainFeaturesHelper import WormFromTable
from MWTracker.featuresAnalysis.obtainFeatures import getMicronsPerPixel, getFPS

files = glob.glob(os.path.join(main_dir, '*.hdf5' ))
files = sorted(files)[0:]
#%%
for mask_id in range(len(files)):
    masked_image_file = files[mask_id]
    skeletons_file = masked_image_file.replace('MaskedVideos', 'Results')[:-5] + '_skeletons.hdf5'
    feat_file = masked_image_file.replace('MaskedVideos', 'Results')[:-5] + '_features.hdf5'
    segworm_feat_file = masked_image_file.replace('MaskedVideos', 'Features')[:-5] + '_features.mat'

    print(mask_id, masked_image_file)
    
    if os.path.exists(segworm_feat_file) and os.path.exists(feat_file):
        with tables.File(feat_file, 'r') as fid:
            if '/features_means' in fid and \
            fid.get_node('/features_means').attrs['has_finished'] and \
            fid.get_node('/features_timeseries').shape[0]>0:
                skeletons = fid.get_node('/skeletons')[:]
                frame_range = fid.get_node('/features_events/worm_1')._v_attrs['frame_range']
            
        #pad the beginign with np.nan to have the same reference as segworm (frame 0)
        skeletons = np.pad(skeletons, [(frame_range[0],0), (0,0), (0,0)], 
                       'constant', constant_values = np.nan)
    
        #load segworm data
        fvars = loadmat(segworm_feat_file, struct_as_record=False, squeeze_me=True)
        segworm_x = -fvars['worm'].posture.skeleton.x.T
        segworm_y = -fvars['worm'].posture.skeleton.y.T
        
        #correct in case the data has different size shape
        max_n_skel = min(segworm_x.shape[0], skeletons.shape[0])
        segworm_x = segworm_x[:max_n_skel]
        segworm_y = segworm_y[:max_n_skel]
        skeletons = skeletons[:max_n_skel]

        #calculate the square root of the mean squared error
        dX = skeletons[:,:,0] - segworm_x
        dY = skeletons[:,:,1] - segworm_y
        R_error = dX*dX + dY*dY
        skel_error = np.sqrt(np.mean(R_error, axis=1))


