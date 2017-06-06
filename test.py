#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 17:22:17 2017

@author: ajaver
"""
import pymysql
import os
import shutil

conn = pymysql.connect(host='localhost', database='single_worm_db')
cur = conn.cursor()

cur.execute('''
    select results_dir, base_name 
    from experiments_full 
    where date >= "2011-08-19 00:00:00" and date <= "2011-09-21 00:00:00" 
    and strain = 'N2';
    ''')
result = cur.fetchall()  

cur.close()
conn.close()

fnames = [os.path.join(x[0], x[1] + '_features.hdf5') for x in result]


dname = '/Users/ajaver/Desktop/feats/N2'

if not os.path.exists(dname):
    os.makedirs(dname)

for fname in fnames:
    shutil.copy(fname, dname)
