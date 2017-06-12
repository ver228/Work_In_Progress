#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 10:44:56 2017

@author: ajaver
"""

import tables
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import os
import seaborn as sns

from matplotlib.backends.backend_pdf import PdfPages

from collections import OrderedDict
from tierpsy.helper.misc import replace_subdir, remove_ext
from tierpsy.helper.params import read_fps

def read_light_data(mask_file):
    with tables.File(mask_file) as fid:
        mean_intensity = fid.get_node('/mean_intensity')[:]
    
    
    med = np.median(mean_intensity)
    mad = np.median(np.abs(mean_intensity-med))
    #the MAD is releated to sigma by the factor below as explained here:
    #wiki (https://en.wikipedia.org/wiki/Median_absolute_deviation#relation_to_standard_deviation)
    s = mad*1.4826 
    
    #... and since the median should be equal to the mean in a gaussian dist
    # we can use 6 sigma as our threshold
    light_on = mean_intensity >  med + s*6
    
    return light_on

def get_pulses_indexes(light_on, window_size):
    switches = np.diff(light_on.astype(np.int))
    turn_on, = np.where(switches==1)
    turn_off, = np.where(switches==-1)
    
    assert turn_on.size == turn_off.size
    
    delP = turn_off - turn_on
    
    good = delP>window_size/2
    
    
    return turn_on[good], turn_off[good]



def get_names(results_dir, base_name):
    skel_file = os.path.join(results_dir, base_name + '_skeletons.hdf5')
    
    mask_dir = replace_subdir(results_dir, 'Results', 'MaskedVideos')
    if not os.path.exists(mask_dir):
        mask_dir = results_dir
    
    mask_file = os.path.join(mask_dir, base_name +'.hdf5')
    
    return skel_file, mask_file

if __name__ == '__main__':    
    #results_dir = '/Volumes/behavgenom_archive$/Avelino/screening/David_Miller/Results/ATR_210417/'
    results_dir = '/Users/ajaver/OneDrive - Imperial College London/optogenetics/Arantza/Results/oig8'
    
    expected_pulse_size_s = 2
    check_window_s = 5
    
    fnames = [x for x in os.listdir(results_dir) if x.endswith('.hdf5')]
    base_names = set(map(remove_ext, fnames))
    
    vid_type = ['control', 'herm', 'male'] 
    data = OrderedDict()
    time_ranges = OrderedDict()
    for x in vid_type:
        data[x] = pd.DataFrame()
        time_ranges[x] = []
    
    
    for base_name in base_names:
        print(base_name)
        skel_file, mask_file = get_names(results_dir, base_name)
        
        
        fps = read_fps(skel_file)
        expected_pulse_size = fps*expected_pulse_size_s
        check_window = fps*check_window_s
        
        light_on = read_light_data(mask_file)
        
        turn_on, turn_off = get_pulses_indexes(light_on, expected_pulse_size)
        
        assert turn_on.size == 1
        with pd.HDFStore(skel_file, 'r') as fid:
            #blob_features = fid['/blob_features']
            trajectories_data = fid['/trajectories_data']
            
            
        dat = trajectories_data.loc[trajectories_data['worm_label']!=0, ['worm_label', 'frame_number']]
        dat['frame_number'] = dat['frame_number'] - turn_on[0]
        dat['frame_number'] = dat['frame_number'].astype(np.int)
        
        rr = (dat['frame_number'].min(), dat['frame_number'].max())
        for vt in vid_type:
            if vt in base_name:
                data[vt] = pd.concat((data[vt], dat))
                time_ranges[vt].append(rr)
                break
    #%%
    with PdfPages('N_Labels.pdf') as pdf:
        tlabel = {'control':'Males Control', 'herm':'Hermaphrodites', 'male':'Males'}
        
        for vt, dat in data.items():
            ini, fin = zip(*time_ranges[vt])
            
            xl = (max(ini)/fps, min(fin)/fps)
            
            n_worms = dat.loc[dat['worm_label']==1, 'frame_number'].value_counts()
            n_worms = n_worms.sort_index()
            n_cluster = dat.loc[dat['worm_label']==2, 'frame_number'].value_counts()
            n_cluster = n_cluster.sort_index()
            
            fig = plt.figure(figsize=(12,5))
            plt.plot(n_cluster.index/fps, n_cluster.values.astype(np.int))#, '.')
            plt.plot(n_worms.index/fps, n_worms.values.astype(np.int))#, '.')
            plt.plot((0,0), plt.ylim(), 'k:')
            
            
            plt.title(tlabel[vt])
            plt.xlim(xl)
            plt.legend(['Worm Clusters', 'Single Worms'])
            plt.xlabel('Time from Light Pulse (s)')
            plt.ylabel('N Labels')
            
            
            pdf.savefig(fig)
            
            
            