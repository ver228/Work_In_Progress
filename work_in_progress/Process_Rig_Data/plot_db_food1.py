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
database_name = os.path.join(database_dir, 'control_experiments_Test_20161027.db')

con = create_engine('sqlite:///' + database_name)

exp_query = 'SELECT * FROM experiments'
feat_query = 'SELECT * FROM features_means_split'

sql = feat_query + ' AS f JOIN (' + exp_query + ') AS e ON f.video_id=e.video_id'

feats = pd.read_sql_query(sql, con)
feats['video_timestamp'] = pd.to_datetime(feats['video_timestamp'])
feats['date'] = feats['video_timestamp'].dt.date

#feats = feats[feats['N_Worms'].isin((3, 10))]
#%%



def plot_2boxes(feat1_str, feat2_str, main_div, sub_div, feat1_ylim, feat2_ylim):
    main_fig = plt.figure()
    plt.subplot(2,1,1)
    frame_top = sns.boxplot(feats[main_div], feats[feat1_str], hue=feats[sub_div])
    frame_top.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    frame_top.set_ylim(feat1_ylim)
    frame_top.set_xlabel('')
    
    plt.subplot(2,1,2)
    frame_bot = sns.boxplot(feats[main_div], feats[feat2_str], hue=feats[sub_div])
    frame_bot.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    frame_bot.set_ylim(feat2_ylim)
    return main_fig
    
def plot_2boxes_group(feat1_str, feat2_str, main_div, sub_div, group_div, feat1_ylim, feat2_ylim):
    main_fig = plt.figure()
    for ii, (picker, feats_p) in enumerate(feats.groupby(group_div)):
        feats_p = feats_p.sort_values(by=[main_div,  'N_Worms'])
        plt.subplot(2,3, ii + 1)
        frame_top = sns.boxplot(feats_p[main_div], feats_p[feat1_str], hue=feats_p[sub_div])
        
        plt.subplot(2,3, 4 + ii)
        framb_bot = sns.boxplot(feats_p[main_div], feats_p[feat2_str], hue=feats_p[sub_div])
        
        
        frame_top.set_title(picker)
        frame_top.set_ylim(feat1_ylim)
        frame_top.set_xlabel('')
        
        framb_bot.set_ylim(feat2_ylim)
        framb_bot.set_xlabel('')
        
        if ii > 0:
            frame_top.set_ylabel('')
            frame_top.get_yaxis().set_ticklabels([])
            framb_bot.set_ylabel('')
            framb_bot.get_yaxis().set_ticklabels([])
         
        framb_bot.legend().set_visible(False)
        frame_top.legend().set_visible(False)
        
        if ii == 0:
            framb_bot.legend(loc='lower center', bbox_to_anchor=(0.5, 1.2),
                             ncol=2, fancybox=True, shadow=True)
        
            
    return main_fig
#%%    
feat1_str = 'length'
feat2_str = 'midbody_speed_pos'
feat1_ylim = [0, 1800]
feat2_ylim = [0, 300]
main_div = 'Strain'
sub_div = 'Picker'
dd = plot_2boxes(feat1_str, feat2_str, main_div, sub_div, feat1_ylim, feat2_ylim)


#%%
feat1_str = 'length'
feat2_str = 'midbody_speed_pos'
main_div = 'Strain'
sub_div = 'N_Worms'
feat1_ylim = [0, 1800]
feat2_ylim = [0, 250]
dd = plot_2boxes(feat1_str, feat2_str, main_div, sub_div, feat1_ylim, feat2_ylim)
#%%
feat1_str = 'length'
feat2_str = 'midbody_speed_pos'
main_div = 'Strain'
sub_div = 'N_Worms'
group_div = 'Picker'
feat1_ylim = [0, 1800]
feat2_ylim = [0, 250]
dd = plot_2boxes_group(feat1_str, feat2_str, main_div, sub_div, group_div, feat1_ylim, feat2_ylim)
dd.savefig('B_1_{}_2_{}_{}_{}_{}.pdf'.format(feat1_str, feat2_str, main_div, sub_div, group_div))

#%%
database_name = os.path.join(database_dir, 'control_experiments_Test_Food.db')

con = create_engine('sqlite:///' + database_name)

exp_query = 'SELECT * FROM experiments'
feat_query = 'SELECT * FROM features_means_split'

sql = feat_query + ' AS f JOIN (' + exp_query + ') AS e ON f.video_id=e.video_id'

feats = pd.read_sql_query(sql, con)
feats['video_timestamp'] = pd.to_datetime(feats['video_timestamp'])
feats['date'] = feats['video_timestamp'].dt.date
#%%
good = feats['N_Worms'].isin((3,10))
feats = feats[good]
#%%
feat1_str = 'length'
feat2_str = 'midbody_speed_pos'
main_div = 'Strain'
sub_div = 'N_Worms'
group_div = 'Picker'
feat1_ylim = [0, 1800]
feat2_ylim = [0, 250]
dd = plot_2boxes_group(feat1_str, feat2_str, main_div, sub_div, group_div, feat1_ylim, feat2_ylim)
dd.savefig('B_1_{}_2_{}_{}_{}_{}.pdf'.format(feat1_str, feat2_str, main_div, sub_div, group_div))
#%%
feat1_str = 'length'
feat2_str = 'midbody_speed_pos'
main_div = 'Strain'
sub_div = 'Food_Conc'
group_div = 'Picker'
feat1_ylim = [0, 1800]
feat2_ylim = [0, 250]
dd = plot_2boxes_group(feat1_str, feat2_str, main_div, sub_div, group_div, feat1_ylim, feat2_ylim)
dd.savefig('B_1_{}_2_{}_{}_{}_{}.pdf'.format(feat1_str, feat2_str, main_div, sub_div, group_div))


#%%
feat1_str = 'length'
feat2_str = 'midbody_speed_pos'
main_div = 'Strain'
sub_div = 'Food_Conc'
feat1_ylim = [0, 1800]
feat2_ylim = [0, 250]
dd = plot_2boxes(feat1_str, feat2_str, main_div, sub_div, feat1_ylim, feat2_ylim)
#%%
good = (feats['N_Worms']==10) & (feats['Food_Conc']==1) & (feats['Strain']!='HW') 
feat_g = feats[good].sort_values(by='Strain')

plt.figure()
plt.subplot(2,1,1)
sns.boxplot(feat_g['Strain'], feat_g['length'])
plt.ylim([0, 1600])
plt.figure()
plt.subplot(2,1,2)
sns.violinplot(feat_g['Strain'], feat_g['midbody_speed_pos'])
#plt.ylim([0, 150])


#%%
database_name = os.path.join(database_dir, 'control_single.db')

con = create_engine('sqlite:///' + database_name)

exp_query = 'SELECT * FROM experiments'
feat_query = 'SELECT * FROM features_means'

sql = feat_query + ' AS f JOIN (' + exp_query + ') AS e ON f.video_id=e.video_id'

feats = pd.read_sql_query(sql, con)
#%%
chg = (feats['gene']!=feats['gene'])
feats.loc[chg, 'gene'] = 'N2'
#%%
feats = feats.sort_values(by='gene')

plt.figure()
plt.subplot(2,1,1)
sns.boxplot(feats['gene'], feats['length'])
plt.ylim([0, 1600])
plt.figure()
plt.subplot(2,1,1)
sns.boxplot(feats['gene'], feats['midbody_speed_pos'])
plt.ylim([0, 350])

