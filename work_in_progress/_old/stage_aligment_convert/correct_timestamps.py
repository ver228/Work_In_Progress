#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 19:25:46 2017

@author: ajaver
"""

from tierpsy.analysis.compress.extractMetaData import read_and_save_timestamp, get_timestamp
from tierpsy.helper.misc import save_modified_table
import os
import pandas as pd
import numpy as np
import pymysql
import multiprocessing as mp

#%%
def fix_timestamps(masked_file, skeletons_file):
    
    timestamp, timestamp_time = read_and_save_timestamp(masked_file, dst_file='')
    
    
    if os.path.exists(skeletons_file):
        read_and_save_timestamp(masked_file, dst_file=skeletons_file)
    
    with pd.HDFStore(skeletons_file, 'r') as fid:
        trajectories_data = fid['trajectories_data']
    
    ind = trajectories_data['frame_number'].values.astype(np.int32)
    trajectories_data['timestamp_raw'] = timestamp[ind]
    trajectories_data['timestamp_time'] = timestamp_time[ind]
    
    if np.all(np.isnan(timestamp)) or np.all(np.diff(trajectories_data['timestamp_raw'])>=0):
        save_modified_table(skeletons_file, trajectories_data, 'trajectories_data')
    else:
        return (masked_file, skeletons_file)
#%%
def _process_row(row):
    
    fpath = os.path.join(row['results_dir'], row['base_name'])
    masked_file = fpath + '.hdf5'
    skeletons_file = fpath + '_skeletons.hdf5'
    
    if not os.path.exists(masked_file):
        return
    
    return fix_timestamps(masked_file, skeletons_file)
    

if __name__ == '__main__':
#    conn = pymysql.connect(host='localhost', database='single_worm_db')
#    cur = conn.cursor(pymysql.cursors.DictCursor)
#    
#    sql = '''
#    SELECT *
#    FROM experiments_full
#    '''
#    
#    cur.execute(sql)
#    f_data = cur.fetchall()
#    
#    n_batch = 50
#    p = mp.Pool(n_batch)
#    
#    bad_files = []
#    for nn in range(0, len(f_data), n_batch):
#        DD = list(p.map(_process_row, f_data[nn:nn+n_batch]))
#        bad_files += [x for x in DD if x is not None]
#        print(nn, len(f_data), len(bad_files))
    #%%
#    with open('bad_timestamps.txt', 'w') as fid:
#        for m, s in bad_files:
#            fid.write(m + '\n')
    #%%
    import tables
    with open('bad_timestamps.txt', 'r') as fid:
        dd = fid.read()
    
    for masked_file in dd.split('\n'):
        if not os.path.exists(masked_file):
            continue
        with tables.File(masked_file, 'r') as fid:
            timestamp = fid.get_node('/timestamp/raw')[:]
            if np.all(np.isnan(timestamp)):
                print('bad')
                os.remove(masked_file)
