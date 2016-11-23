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



#%%

def _filter_feats(con, feats, filt_path_range = 10, filt_frac_good = 0.75, tab_name = 'features_means'):
    #
    feats_ind = pd.read_sql_query('SELECT worm_index, n_frames, n_valid_skel, path_range, video_id FROM %s' % tab_name, con)
    feats_ind['frac_good'] = feats_ind['n_valid_skel']/feats_ind['n_frames']
    good = (feats_ind['path_range'] > filt_path_range) & (feats_ind['frac_good']>filt_frac_good)
    good_ind = feats_ind.loc[good, ['worm_index', 'video_id']]
    good_ind = [tuple(x) for x in good_ind.values.astype(np.int)]
    #all the tuples are uniqu
    assert len(good_ind) == len(set(good_ind))

    good_rows = [(row['worm_index'], row['video_id']) in good_ind for ii, row in feats.iterrows()]
    
    return good_rows
                 
def _read_feats(con, tab_name = 'features_means_split'):
    experiments = pd.read_sql_query('SELECT * FROM experiments', con)
    feats = pd.read_sql_query('SELECT * FROM %s' % tab_name, con)
    feats = feats.merge(experiments, on='video_id')
    
    feats['video_timestamp'] = pd.to_datetime(feats['video_timestamp'])
    feats['date'] = feats['video_timestamp'].dt.date
    feats['worm_index'] = feats['worm_index'].astype(np.int)
    return feats
                 
                 
def get_feats_db(database_name, filt_path_range = 10, filt_frac_good = 0.75, 
                 tab_name = 'features_means_split'):
    con = create_engine('sqlite:///' + database_name)
    
    feats = _read_feats(con, tab_name)
    
    #let's use the full features to do the filtering
    tab_name_c = tab_name.replace('_split', '')
    good_rows = _filter_feats(con, feats, filt_path_range, filt_frac_good, tab_name = tab_name_c)
    
    return feats.loc[good_rows, :]
    
#%%
def plot_boxes(feats, feat_str, main_div, sub_div):
    #violinplot
    ff = sns.boxplot(feats[main_div], feats[feat_str], hue=feats[sub_div])
    #ff = sns.violinplot(feats[main_div], feats[feat_str], hue=feats[sub_div])
    ff.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    return ff

def plot_boxes_group(feats, feat_str, main_div, sub_div, group_div, feat_ylim=[]):
    plt.figure()
    
    groups = feats.groupby(group_div)
    for ii, (picker, feats_p) in enumerate(groups):
        feats_p = feats_p.sort_values(by=[main_div,  sub_div])
        
        plt.subplot(3,1, ii + 1)
        ff = plot_boxes(feats_p, feat_str, main_div, sub_div)
        
        plt.title(picker)
        if ii < len(groups)-1:
            ff.get_xaxis().set_ticklabels([])
            ff.set_xlabel('')
        
            
        if len(feat_ylim) == 2:
            ff.set_ylim(feat_ylim)

def first_test(database_dir, tab_name):
    #%%
    
    database_name = os.path.join(database_dir, 'control_experiments_Test_20161027.db')
    feats = get_feats_db(database_name, 
                         filt_path_range = 10, 
                         filt_frac_good = 0.5,
                         tab_name = tab_name)
    #%%
    #feat_str = 'length'
    #feat_ylim = (400, 1600)
    
    feat_str = 'midbody_speed_pos'
    feat_ylim = []
    
    plt.figure()
    plot_boxes(feats, feat_str, 'Strain', 'Picker')
    if feat_ylim:
        plt.ylim(feat_ylim)
    
    plt.figure()
    plot_boxes(feats, feat_str, 'Strain', 'N_Worms')
    if feat_ylim:
        plt.ylim(feat_ylim)
    
    plot_boxes_group(feats, feat_str, 'Strain', 'N_Worms', 'Picker', feat_ylim)

def test_food(database_dir, tab_name):
    #%%
    database_name = os.path.join(database_dir, 'control_experiments_Test_Food.db')
    feats = get_feats_db(database_name, 
                         filt_path_range = 10, 
                         filt_frac_good = 0.5,
                         tab_name = tab_name)
    good = feats['N_Worms'].isin((3,10))
    feats = feats[good]
    #%%
    #feat_str = 'length'
    #feat_ylim = (400, 1600)
    
    feat_str = 'midbody_speed_pos'
    feat_ylim = [0, 500]
    
    plt.figure()
    plot_boxes(feats, feat_str, 'Strain', 'Picker')
    if feat_ylim:
        plt.ylim(feat_ylim)
    
    plt.figure()
    plot_boxes(feats, feat_str, 'Strain', 'N_Worms')
    if feat_ylim:
        plt.ylim(feat_ylim)
    
    plt.figure()
    plot_boxes(feats, feat_str, 'Strain', 'Food_Conc')
    if feat_ylim:
        plt.ylim(feat_ylim)
        
    plot_boxes_group(feats, feat_str, 'Strain', 'N_Worms', 'Picker', feat_ylim)
    
    plot_boxes_group(feats, feat_str, 'Strain', 'Food_Conc', 'N_Worms', feat_ylim)
    
def agar_test(database_dir, tab_name):
    database_name = os.path.join(database_dir, 'control_experiments_Agar_Test.db')
    feats = get_feats_db(database_name, 
                         filt_path_range = 10, 
                         filt_frac_good = 0.5,
                         tab_name = tab_name)
    #%%
    #feat_str = 'length'
    #feat_ylim = (400, 1600)
    
    feat_str = 'midbody_speed_pos'
    feat_ylim = [0, 500]
    
    plt.figure()
    plot_boxes(feats, feat_str, 'Strain', 'Picker')
    if feat_ylim:
        plt.ylim(feat_ylim)
    
    plt.figure()
    plot_boxes(feats, feat_str, 'Strain', 'N_Worms')
    if feat_ylim:
        plt.ylim(feat_ylim)
    
    plt.figure()
    plot_boxes(feats, feat_str, 'Strain', 'Old/New Agar')
    if feat_ylim:
        plt.ylim(feat_ylim)
    
    plot_boxes_group(feats, feat_str, 'Strain', 'Old/New Agar', 'Picker', feat_ylim)   
#%%    
if __name__ == '__main__':
    database_dir = '/Users/ajaver/OneDrive - Imperial College London/compare_strains_DB'
    #first_test(database_dir)
    #test_food(database_dir)
    #agar_test(database_dir)
    
    database_name = os.path.join(database_dir, 'control_experiments_L4_Long_Rec.db')
    feats = get_feats_db(database_name, 
                         filt_path_range = 10, 
                         filt_frac_good = 0.5,
                         tab_name = 'features_P90th_split')

#%%

#database_name = os.path.join(database_dir, 'control_single.db')
#feats = get_feats_db(database_name, tab_name = 'features_means')
#chg = (feats['gene']!=feats['gene'])
#feats.loc[chg, 'gene'] = 'N2'
#feats = feats.sort_values(by='gene')
##%%
#
#plt.figure()
#plt.subplot(2,1,1)
#sns.boxplot(feats['gene'], feats['length'])
#plt.ylim([0, 1600])
#plt.figure()
#plt.subplot(2,1,1)
#sns.boxplot(feats['gene'], feats['midbody_speed_pos'])
#plt.ylim([0, 350])

