# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 19:39:41 2015

@author: ajaver
"""
import pandas as pd
#import matplotlib.pylab as plt
import numpy as np
import h5py
import cv2
import time
import tables
import matplotlib.pylab as plt


#import StringIO
#out = StringIO.StringIO()

#masked_image_file = '/Volumes/behavgenom$/GeckoVideo/Compressed/20150220/CaptureTest_90pc_Ch3_20022015_183607.hdf5'
#trajectories_file = '/Volumes/behavgenom$/GeckoVideo/Trajectories/20150220/CaptureTest_90pc_Ch3_20022015_183607.hdf5'

#masked_image_file = '/Users/ajaver/Desktop/Gecko_compressed/CaptureTest_90pc_Ch2_18022015_230213.hdf5'
#trajectories_file = '/Users/ajaver/Desktop/Gecko_compressed/Trajectory_CaptureTest_90pc_Ch2_18022015_230213.hdf5'

#masked_image_file = '/Users/ajaver/Desktop/Gecko_compressed/CaptureTest_90pc_Ch2_18022015_230213.hdf5'
#trajectories_file = '/Users/ajaver/Desktop/Gecko_compressed/Trajectory_CaptureTest_90pc_Ch2_18022015_230213.hdf5'

#masked_image_file = '/Users/ajaver/Desktop/Gecko_compressed/prueba/CaptureTest_90pc_Ch1_02022015_141431.hdf5'
#trajectories_file = '/Users/ajaver/Desktop/Gecko_compressed/prueba/trajectories/CaptureTest_90pc_Ch1_02022015_141431.hdf5'

#masked_image_file = '/Users/ajaver/Desktop/Gecko_compressed/CaptureTest_90pc_Ch2_18022015_230213.hdf5'
#trajectories_file = '/Users/ajaver/Desktop/Gecko_compressed/Trajectory_CaptureTest_90pc_Ch2_18022015_230213.hdf5'

#masked_image_file = '/Users/ajaver/Desktop/Gecko_compressed/CaptureTest_90pc_Ch3_21022015_210020.hdf5'
#trajectories_file = '/Users/ajaver/Desktop/Gecko_compressed/Trajectory_CaptureTest_90pc_Ch3_21022015_210020.hdf5'

#masked_image_file = '/Users/ajaver/Desktop/Gecko_compressed/prueba/CaptureTest_90pc_Ch1_02022015_141431.hdf5'
#trajectories_file = '/Users/ajaver/Desktop/Gecko_compressed/prueba/trajectories/CaptureTest_90pc_Ch1_02022015_141431.hdf5'
#segworm_file = '/Users/ajaver/Desktop/Gecko_compressed/prueba/trajectories/CaptureTest_90pc_Ch1_02022015_141431_segworm.hdf5'

masked_image_file = '/Users/ajaver/Desktop/Gecko_compressed/20150323/Capture_Ch4_23032015_111907.hdf5'
trajectories_file = '/Users/ajaver/Desktop/Gecko_compressed/20150323/trajectories/Capture_Ch4_23032015_111907.hdf5'
segworm_file = '/Users/ajaver/Desktop/Gecko_compressed/20150323/trajectories/Capture_Ch4_23032015_111907_segworm.hdf5'


#%%

#read that frame an select trajectories that were considered valid by join_trajectories
table_fid = pd.HDFStore(trajectories_file, 'r')
df = table_fid['/plate_worms']
df =  df[df['worm_index_joined'] > 0]

tracks_data = df[['worm_index_joined', 'frame_number', 'coord_x', 'coord_y']].groupby('worm_index_joined').aggregate(['max', 'min', 'count'])

#filter for trajectories that move too little (static objects)
MIN_DISPLACEMENT = 20;

delX = tracks_data['coord_x']['max'] - tracks_data['coord_x']['min']
delY = tracks_data['coord_y']['max'] - tracks_data['coord_y']['min']

good_index = tracks_data[(delX>MIN_DISPLACEMENT) & (delY>MIN_DISPLACEMENT)].index
df = df[df.worm_index_joined.isin(good_index)]

from scipy.ndimage.filters import median_filter
for dat_group in df.groupby('worm_index'):
    dat = dat_group[1][['threshold', 'frame_number']].sort('frame_number')
    df.loc[dat.index,'threshold'] = median_filter(dat['threshold'],1501)
    
    
table_fid.close()

save_csv_name = '/Users/ajaver/Desktop/Gecko_compressed/prueba/trajectories/bCaptureTest_90pc_Ch1_02022015_141431.csv';
df[['worm_index_joined', 'frame_number', 'coord_x', 'coord_y', 'threshold']].to_csv(save_csv_name, index = True, header = True);
#%%
import matlab.engine
eng = matlab.engine.start_matlab()
#eng.addpath(eng.genpath('/Users/ajaver/GitHub_repositories/SegWorm/Only_segWorm'));
eng.addpath(eng.genpath('/Users/ajaver/GitHub_repositories/Multiworm_Tracking/OnlySegWorm/'));
eng.warning('off', 'normWorms:VulvaContourTooShort')
eng.warning('off', 'normWorms:NonVulvaContourTooShort')

data = {'plate_worms_id':matlab.double(list(df.index)), 
'frame_number':matlab.double(list(df['frame_number'])), 
'worm_index_joined':matlab.double(list(df['worm_index_joined'])),
'coord_x':matlab.double(list(df['coord_x'])),
'coord_y':matlab.double(list(df['coord_y'])),
'threshold':matlab.double(list(df['threshold']))};

eng.movie2segwormfun(data, masked_image_file, segworm_file, nargout=0)
try:
    eng.quit()
except:
    pass;
del eng
#%%
#update pytables with the correct index for segworm_file
results_fid = tables.open_file(trajectories_file, 'r+')
tracking_table = results_fid.get_node('/plate_worms')

segworm_fid = h5py.File(segworm_file, 'r')

plate_worms_id = segworm_fid['/segworm_results/plate_worms_id']

for ii in range(plate_worms_id.size):
    tracking_table.cols.segworm_id[int(plate_worms_id[ii])] = ii;
results_fid.flush()
results_fid.close()