#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 19:45:26 2017

@author: ajaver
"""
import tables
import numpy as np
import os
import pymysql

from tierpsy.analysis.contour_orient.correctVentralDorsal import switchCntSingleWorm

if __name__ == '__main__':
    conn = pymysql.connect(host='localhost', database='single_worm_db')
    cur = conn.cursor(pymysql.cursors.DictCursor)
    
    sql = '''
    SELECT *
    FROM experiments_full
    '''
    
    cur.execute(sql)
    f_data = cur.fetchall()
    
    for irow, row in enumerate(f_data):
        fpath = os.path.join(row['results_dir'], row['base_name'])
        masked_file = fpath + '.hdf5'
        skeletons_file = fpath + '_skeletons.hdf5'
        
        
        if os.path.exists(skeletons_file):
            print(irow+1, len(f_data))
            switchCntSingleWorm(skeletons_file)
            
#            with tables.File(skeletons_file, 'r+') as fid:
#                if '/stage_movement' in fid:
#                    exit_flag = fid.get_node('/stage_movement')._v_attrs['has_finished']
#                    if exit_flag > 0:
#                        frame_diffs = fid.get_node('/stage_movement/frame_diffs')[:]
#                        if exit_flag > 1 or np.any(frame_diffs<0):
#                            
#                            print(exit_flag, irow, row['base_name'])
#                            if '/stage_movement' in fid:
#                                fid.remove_node('/stage_movement', recursive=True)
#                            if '/provenance_tracking/STAGE_ALIGMENT' in fid:
#                                fid.remove_node('/provenance_tracking/STAGE_ALIGMENT', recursive=True)
#                            
#                            for ext in ['_features.hdf5', '.wcon.zip']:
#                                fname = fpath + ext
#                                if os.path.exists(fname):
#                                    os.remove(fname)