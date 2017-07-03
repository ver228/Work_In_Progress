#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 17:08:25 2017

@author: ajaver
"""


import pymysql
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

def get_resample(df, strains_lab, min_samples):
    X = []
    Y = []
    for strain, strain_feats in df.groupby('strain'):
        
        X.append(strain_feats.sample(min_samples))
        Y += min_samples*[strains_lab[strain]]
    
    X = pd.concat(X)
    Y = np.array(Y)
    del X['strain']
    del X['base_name']
    return X, Y


if __name__ == '__main__':
    sql = '''
    SELECT base_name, strain, f.* 
    FROM experiments_full 
    RIGHT JOIN features_means AS f ON experiment_id=id 
    WHERE results_dir like '%/finished/WT/%';
    '''
    
    conn = pymysql.connect(host='localhost', database='single_worm_db')
    df = pd.read_sql(sql, con=conn)
    bad_feats = ['experiment_id', 'worm_index', 'n_frames', 'n_valid_skel','first_frame']
    good_feats = [x for x in df.columns if not x in bad_feats]
    df = df[good_feats]
    #%%
    #features that have many nans
    frac_bad = df.isnull().mean()
    good_feats = frac_bad.index[(frac_bad<0.05)] 
    df = df.loc[:, good_feats]
    
    #remove experiments that still have nans
    df = df.dropna()
    
    #remove strains that have too little samples (it seems that it is only AQ3000) 
    min_samples = 15
    n_strains = df['strain'].value_counts()
    bad_strains = n_strains.index[n_strains<min_samples]
    df = df[~df['strain'].isin(bad_strains)]
    
    df.to_csv('all_data.csv', index=False)
    
    strains_lab = {x:ii for ii,x in enumerate(sorted(df['strain'].unique()))}
    
    X_train, Y_train = get_resample(df, strains_lab, min_samples)
    X_test, Y_test = get_resample(df, strains_lab, min_samples)
    #%%
    top_d = []
    for ii in range(10):
        print(ii)
        clf_tree = RandomForestClassifier(n_estimators=10000)
        clf_tree.fit(X_train, Y_train)
        
        proba = clf_tree.predict_proba(X_test)
        top_pred = np.argsort(proba, axis=1)[: ,::-1]
        preds = top_pred==Y_test[:, np.newaxis]
        
        top1 = np.sum(preds[:, 0])/preds.shape[0]
        top2 = np.sum(preds[:, 0:2])/preds.shape[0]
        top_d.append((top1, top2))
    