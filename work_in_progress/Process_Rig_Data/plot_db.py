#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 08:19:55 2016

@author: ajaver
"""

import os
import pandas as pd
import matplotlib.pylab as plt
from sqlalchemy import create_engine


database_dir = '/Users/ajaver/OneDrive - Imperial College London/compare_strains_DB'
database_name = os.path.join(database_dir, 'control_experiments_firstRun.db')

con = create_engine('sqlite:///' + database_name)

exp_cols = ['video_id', 'Camera_N', 'Focus', 'N_Worms', 'Pick_time', 'Pick_type',
       'Picker', 'Rig_Pos', 'Set_N', 'Strain', 'video_timestamp']

exp_query = 'SELECT ' + ','.join(exp_cols) + ' FROM experiments'
feat_query = 'SELECT * FROM features_means_split'

sql = feat_query + ' AS f JOIN (' + exp_query + ') AS e ON f.video_id=e.video_id'

feats = pd.read_sql_query(sql, con)
feats['Strain'] = feats['Strain'].str.strip()
feats['Strain'] = feats['Strain'].replace({'HW':'HA', 'Ha':'HA'})
feats['Picker'] = feats['Picker'].replace({'AEV':'AEJ'})
feats['video_timestamp'] = pd.to_datetime(feats['video_timestamp'])
#%%
import seaborn as sns
for feat_str in ['length', 'midbody_speed_pos']:
    plt.figure()
    sns.boxplot(feats['Strain'], feats[feat_str], hue=feats['N_Worms'])

#%%
import seaborn as sns
good = feats['N_Worms']>=5
ffg = feats.loc[good]
ffg['date'] = ffg['video_timestamp'].dt.date
for feat_str in ['length', 'midbody_speed_pos']:
    plt.figure()
    sns.boxplot(ffg['Strain'], ffg[feat_str], hue=ffg['date'])
#%%
import seaborn as sns
good = feats['N_Worms']>=5
ffg = feats.loc[good]
ffg['date'] = ffg['video_timestamp'].dt.date
for feat_str in ['length', 'midbody_speed_pos']:
    plt.figure()
    sns.boxplot(ffg['Strain'], ffg[feat_str], hue=ffg['Picker'])
#%%
import seaborn as sns
good = feats['N_Worms']>=5
ffg = feats.loc[good]
ffg['date'] = ffg['video_timestamp'].dt.date
for feat_str in ['length', 'midbody_speed_pos']:
    plt.figure()
    sns.boxplot(ffg['Strain'], ffg[feat_str], hue=ffg['Camera_N'])

#%%
import seaborn as sns
good = feats['N_Worms']>=5
ffg = feats.loc[good]
ffg['date'] = ffg['video_timestamp'].dt.date
sns.factorplot(x=ffg['Strain'], y=ffg[feat_str], hue=ffg['Picker'], \
              col=ffg['date'], kind='box')
#for feat_str in ['length', 'midbody_speed_pos']:
#    plt.figure()
#    sns.boxplot(ffg['Strain'], ffg[feat_str], hue=ffg['Camera_N'])
#%%
for group_name, group in ffg.groupby('date'):
    print(group)
    plt.figure()
    sns.boxplot(group['Strain'], group[feat_str], hue=group['Picker'])
    plt.title(group_name)