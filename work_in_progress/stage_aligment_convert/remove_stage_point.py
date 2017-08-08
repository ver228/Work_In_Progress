#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 19:45:26 2017

@author: ajaver
"""
import tables
import os
import pymysql

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
        print(irow, len(f_data))
        fpath = os.path.join(row['results_dir'], row['base_name'])
        masked_file = fpath + '.hdf5'
        skeletons_file = fpath + '_skeletons.hdf5'
        
        
        if os.path.exists(skeletons_file):
            with tables.File(skeletons_file, 'r+') as fid:
                if '/stage_movement' in fid:
                    fid.remove_node('/stage_movement', recursive=True)
                if '/provenance_tracking/STAGE_ALIGMENT' in fid:
                    fid.remove_node('/provenance_tracking/STAGE_ALIGMENT', recursive=True)
            