#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 11:17:40 2017

@author: ajaver
"""
import os
import glob
import pandas as pd
import numpy as np
import tables

results_dir = '/Volumes/behavgenom_archive$/Avelino/screening/Development/Results'

#search for the features.hdf5 files (they are the only one we need)
fnames = glob.glob(os.path.join(results_dir, '**', '*_features.hdf5'))

#I am ordering the subdirectories first element experiment number, second element cohort number
data_order = {
        'Development_C1_170617' : (1,1),
        'Development_C2_180617' : (1,2),
        'Development_C3_180617' : (1,3),
        'Development_C1_260617' : (2,1),
        'Development_C2_300617' : (2,2),
        'Development_C3_300617' : (2,3)
        }

#%%
#extract useful information from the file name to group the experiments
dat = []
for fname in sorted(fnames):
    bn = os.path.basename(fname)
    bn = bn.replace('_features.hdf5', '')
    subdir = fname.split(os.sep)[-2]
    
    dd = bn.split('_')
    datetime_str = dd[-2] + '_' + dd[-1]
    
    ch_n = int([x[2:] for x in dd if 'Ch' in x][0])
    
    exp_n, cohort_n = data_order[subdir]
    
    dat.append((fname, bn, subdir, datetime_str, ch_n, exp_n, cohort_n))


columns = ['file_name', 'base_name', 'subdir', 'timestamp', 'channel', 'exp_n', 'cohort_n']
files_data = pd.DataFrame(dat, columns=columns)
files_data['timestamp'] = pd.to_datetime(files_data['timestamp'], format='%d%m%Y_%H%M%S')

#in some datasets the files were fragmented (two videos of 1 hour instead of a single video)
#we need to get the delta time between videos in the same set to correct for this
# I am assuiming that in the same directory videos with the same Channel belong to the same sample
files_data['delta_time'] = 0
for gg, dat in files_data.groupby(['subdir', 'channel']):
    delT = (dat['timestamp']-dat['timestamp'].min())/ np.timedelta64(1, 's')
    files_data.loc[delT.index, 'delta_time'] = delT 

#%%
#let's read the files. I am saving it to a pytables hdf5 file. 
#This format allows to save large amounts of data. Other option is to use sql
#but pytables works fine with pandas and can be read with matlab.
#SQL is more flexible it is a bit more tricky to use
with tables.File('development_data.hdf5', "w") as fid:
    #reformat file data to save into pytables. 
    #This part is a bit annoying an to to important (I could have skip it)
    files_data['timestamp'] = files_data['timestamp'].dt.strftime('%d/%m/%Y %H:%M:%S')
    files_data_f = files_data.to_records(index=False)
    dtypes_o = files_data_f.dtype
    
    def _get_s_dtype(x):
        nn = max(map(len, files_data_f[x]))
        return '|S{}'.format(nn)
    dtype_n = np.dtype([(x, _get_s_dtype(x) if 'O' in y else y) for (x,y) in dtypes_o.descr])
    files_data_f = files_data_f.astype(dtype_n)
    data_table = fid.create_table(
                '/',
                'files_data',
                obj=files_data_f
                )
    
    #READ each features.hdf5 file and STORE the data into the hdf5
    
    #I will save all data into a this field, so i want to be sure it was deleted when the file was created (w mode)
    assert not '/features_timeseries' in fid
    for irow, row in files_data.iterrows():
        print(irow, row['file_name'])
        with pd.HDFStore(row['file_name'], 'r') as fid_single:
            df = fid_single['features_timeseries']
        df['cohort_n'] = row['cohort_n']
        df['exp_n'] = row['exp_n']
        df['fname_row'] = irow 
        
        #this value is in frames so let's convert it in to seconds
        fps = 25 #this frames per seconds default in the worm rig
        df['timestamp'] = df['timestamp']/fps 
        #shift the timestamp values in case the videos are cropped 
        df['timestamp'] += row['delta_time']
        
        tab_recarray = df.to_records(index=False)
        if not '/features_timeseries' in fid:
            data_table = fid.create_table(
                '/',
                'features_timeseries',
                obj=tab_recarray)
        else:
            data_table.append(tab_recarray)
        
       