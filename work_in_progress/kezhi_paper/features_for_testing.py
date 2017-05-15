#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  9 11:34:19 2017

@author: ajaver
"""

import glob
import os
import pymysql
import pandas as pd

def get_query(base_names):
    bn_str = ','.join(['"'+ x + '"' for x in base_names])
    sql = '''
    SELECT base_name, strain, strain_description, f.*
    FROM experiments_full
    RIGHT JOIN features_means AS f ON experiment_id=id
    WHERE base_name IN ({});
    '''.format(bn_str)
    
    return sql

def read_feats(f_dir):
    conn = pymysql.connect(host='localhost', database='single_worm_db')
    fnames = glob.glob(os.path.join(f_dir, '**', '*.hdf5'), recursive=True)
    base_names = [os.path.basename(x).replace('_eig.hdf5', '') for x in fnames]
    
    sql = get_query(base_names)
    df = pd.read_sql(sql, con=conn)
    conn.close()
    
    return df


training_dir = '/Volumes/behavgenom$/Kezhi/Classifier_DL/training'
testing_dir = '/Volumes/behavgenom$/Kezhi/Classifier_DL/testing_nips'

train_df = read_feats(training_dir)
test_df = read_feats(testing_dir)


train_df.to_csv('train_feat_means.csv')
test_df.to_csv('test_feat_means.csv')
