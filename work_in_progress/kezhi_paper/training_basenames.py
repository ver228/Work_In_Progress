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

from calculate_features import exec_parallel
from check_real_data import read_feat_summary

training_dir = '/Volumes/behavgenom$/Kezhi/Classifier_DL/training'

fnames = glob.glob(os.path.join(training_dir, '**', '*.hdf5'), recursive=True)
base_names = [os.path.basename(x).replace('_eig.hdf5', '') for x in fnames]


sql = '''
SELECT results_dir, base_name
FROM experiments
WHERE base_name IN ({})
'''.format(','.join(["'"+x+"'" for x in base_names]))
conn = pymysql.connect(host='localhost', database='single_worm_db')
cur = conn.cursor()    
cur.execute(sql)
results = cur.fetchall()
conn.close()

train_files = [os.path.join(x[0], x[1] + '_features.hdf5') for x in results]
train_files = [x for x in train_files if os.path.exists(x)]

train_feats = exec_parallel(train_files, read_feat_summary)
train_feats = pd.concat(train_feats)
train_feats.to_csv('train_features.csv')
