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
import seaborn as sns


exp_set = 'Test_20161027'#'Test_Food'#
database_dir = '/Users/ajaver/OneDrive - Imperial College London/compare_strains_DB'

database_name = 'control_experiments_{}.db'.format(exp_set)

con = create_engine('sqlite:///' + os.path.join(database_dir, database_name))



exp_query = 'SELECT * FROM experiments'
feat_query = 'SELECT * FROM features_means_split'

sql = feat_query + ' AS f JOIN (' + exp_query + ') AS e ON f.video_id=e.video_id'

feats = pd.read_sql_query(sql, con)
feats['Strain'] = feats['Strain'].str.strip()
feats['Pick_type'] = feats['Pick_type'].replace({'Hair':'hair'})

feats['video_timestamp'] = pd.to_datetime(feats['video_timestamp'])
#%%
for feat_str in ['length', 'midbody_speed_pos']:
    plt.figure()
    sns.boxplot(feats['Strain'], feats[feat_str], hue=feats['N_Worms'])

#%%
good = feats['N_Worms']>=5
ffg = feats.loc[good]
ffg['date'] = ffg['video_timestamp'].dt.date
for feat_str in ['length', 'midbody_speed_pos']:
    plt.figure()
    sns.boxplot(ffg['Strain'], ffg[feat_str], hue=ffg['date'])
#%%
good = (feats['N_Worms']>=5) & (feats['Pick_type'] == 'hair')
ffg = feats.loc[good]
ffg['date'] = ffg['video_timestamp'].dt.date
for feat_str in ['length', 'midbody_speed_pos']:
    plt.figure()
    sns.boxplot(ffg['Strain'], ffg[feat_str], hue=ffg['Picker'])
#%%
good = feats['N_Worms']>=5
ffg = feats.loc[good]
ffg['date'] = ffg['video_timestamp'].dt.date
for feat_str in ['length', 'midbody_speed_pos']:
    plt.figure()
    sns.boxplot(ffg['Strain'], ffg[feat_str], hue=ffg['channel'])

#%%
good = (feats['N_Worms']>=5) & (feats['Picker']=='AEJ')
ffg = feats.loc[good]
ffg['date'] = ffg['video_timestamp'].dt.date
for feat_str in ['length', 'midbody_speed_pos']:
    plt.figure()
    sns.boxplot(ffg['Strain'], ffg[feat_str], hue=ffg['Pick_type'])
