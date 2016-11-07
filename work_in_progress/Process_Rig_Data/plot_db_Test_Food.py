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
import numpy as np

exp_set = 'Test_Food'#'Test_Food'#
database_dir = '/Users/ajaver/OneDrive - Imperial College London/compare_strains_DB'

database_name = 'control_experiments_{}.db'.format(exp_set)

con = create_engine('sqlite:///' + os.path.join(database_dir, database_name))



exp_query = 'SELECT * FROM experiments'
feat_query = 'SELECT * FROM features_means'

sql = feat_query + ' AS f JOIN (' + exp_query + ') AS e ON f.video_id=e.video_id'

feats = pd.read_sql_query(sql, con)
feats['Strain'] = feats['Strain'].str.strip()
feats['video_timestamp'] = pd.to_datetime(feats['video_timestamp'])
feats['date'] = feats['video_timestamp'].dt.date
#%%
for feat_str in ['length', 'midbody_speed_pos']:
    plt.figure()
    sns.boxplot(feats['Strain'], feats[feat_str], hue=feats['N_Worms'])
#%%
for feat_str in ['length', 'midbody_speed_pos']:
    plt.figure()
    sns.boxplot(feats['Strain'], np.log10(feats[feat_str]), hue=feats['Food_Conc'])
#%%
good = feats['N_Worms']>=5
ffg = feats.loc[good]
for feat_str in ['length', 'midbody_speed_pos']:
    plt.figure()
    sns.boxplot(ffg['Strain'], np.log10(ffg[feat_str]), hue=ffg['Food_Conc'])
#%%
for ig, (strain, fg_strain) in enumerate(feats.groupby('Strain')):
    plt.subplot(2,2,ig+1)
    plt.title(strain)
    plt.plot(fg_strain['length'], fg_strain['path_range'], '.')
    plt.ylim([0,200])

#%%
#good = feats['N_Worms']>=5
#ffg = feats.loc[good]
#ffg['date'] = ffg['video_timestamp'].dt.date
#for feat_str in ['length', 'midbody_speed_pos']:
#    plt.figure()
#    sns.boxplot(ffg['Strain'], ffg[feat_str], hue=ffg['date'])
##%%
#good = (feats['N_Worms']>=5) & (feats['Pick_type'] == 'hair')
#ffg = feats.loc[good]
#ffg['date'] = ffg['video_timestamp'].dt.date
#for feat_str in ['length', 'midbody_speed_pos']:
#    plt.figure()
#    sns.boxplot(ffg['Strain'], ffg[feat_str], hue=ffg['Picker'])
##%%
#good = feats['N_Worms']>=5
#ffg = feats.loc[good]
#ffg['date'] = ffg['video_timestamp'].dt.date
#for feat_str in ['length', 'midbody_speed_pos']:
#    plt.figure()
#    sns.boxplot(ffg['Strain'], ffg[feat_str], hue=ffg['channel'])
#
##%%
#good = (feats['N_Worms']>=5) & (feats['Picker']=='AEJ')
#ffg = feats.loc[good]
#ffg['date'] = ffg['video_timestamp'].dt.date
#for feat_str in ['length', 'midbody_speed_pos']:
#    plt.figure()
#    sns.boxplot(ffg['Strain'], ffg[feat_str], hue=ffg['Pick_type'])
