# -*- coding: utf-8 -*-
"""
Created on Mon May  2 17:47:12 2016

@author: ajaver
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from create_database import Experiment

if __name__ == '__main__':
    segworm_feat_file = '/Users/ajaver/Documents/GitHub/Work_In_Progress/Single_Worm_Analysis/all_files/segworm_feat_files.txt'
    with open(segworm_feat_file, 'r') as fid:
        all_data = fid.read().split('\n')
    
    data = []
    for fullname in all_data:
        if fullname:
            base_name = os.path.split(fullname)[1].replace('_features.mat', '')
            
            data.append((fullname, base_name))
    
    engine_v2 = create_engine(r'mysql+pymysql://ajaver:@localhost/single_worm_db_v2')
    session_v2 = Session(engine_v2)

    base_names = set(x[1] for x in data)
    
    segInDB= session_v2.query(Experiment.base_name).\
    filter(Experiment.base_name.in_(base_names)).all()
    segInDB = set(x[0] for x in segInDB)
    
    #dd = [x for x in data if x[1] in base_names-segInDB]
    #%%
    with open('missing_basenames.txt', 'w') as fid:
        for x in base_names-segInDB:
            fid.write(x + '\n')