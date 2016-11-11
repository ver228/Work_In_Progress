#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 08:19:55 2016

@author: ajaver
"""

import os
import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt
from sqlalchemy import create_engine
import numpy as np

database_dir = '/Users/ajaver/OneDrive - Imperial College London/compare_strains_DB'
database_name = os.path.join(database_dir, 'control_experiments_Test_Food.db')

con = create_engine('sqlite:///' + database_name)

exp_query = 'SELECT * FROM experiments'
feat_query = 'SELECT * FROM features_means_split'

sql = feat_query + ' AS f JOIN (' + exp_query + ') AS e ON f.video_id=e.video_id'

feats = pd.read_sql_query(sql, con)
feats['video_timestamp'] = pd.to_datetime(feats['video_timestamp'])
feats['date'] = feats['video_timestamp'].dt.date

feats = feats[feats['N_Worms'].isin((3, 10))]
#%%
plt.figure()
sns.boxplot(feats['Strain'], feats['length'], hue=feats['N_Worms'])

plt.figure()
sns.boxplot(feats['Strain'], np.log10(feats['midbody_speed_pos']), hue=feats['N_Worms'])
    
#%%
plt.figure()
sns.boxplot(feats['Strain'], feats['length'], hue=feats['Picker'])

plt.figure()
sns.boxplot(feats['Strain'], np.log10(feats['midbody_speed_pos']), hue=feats['Picker'])
#%%
plt.figure()
sns.boxplot(feats['Strain'], feats['length'], hue=feats['Food_Conc']);

plt.figure()
sns.boxplot(feats['Strain'], feats['midbody_speed_pos'], hue=feats['Food_Conc']);
plt.ylim([0, 300])
#%%
for picker, feats_p in feats.groupby('Picker'):
    plt.figure()
    plt.subplot(1,2,1)
    sns.boxplot(feats_p['Strain'], feats_p['length'], hue=feats_p['N_Worms'])
    plt.title(picker)
    
    plt.subplot(1,2,2)
    sns.boxplot(feats_p['Strain'], np.log10(feats_p['midbody_speed_pos']), hue=feats_p['N_Worms'])
    

#%%
for picker, feats_p in feats.groupby('Picker'):
    plt.figure()
    plt.subplot(1,2,1)
    sns.boxplot(feats_p['Strain'], feats_p['length'], hue=feats_p['Food_Conc'])
    plt.title(picker)
    
    plt.subplot(1,2,2)
    sns.boxplot(feats_p['Strain'], np.log10(feats_p['midbody_speed_pos']), hue=feats_p['Food_Conc'])




