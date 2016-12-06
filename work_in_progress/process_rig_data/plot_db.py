#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 08:19:55 2016

@author: ajaver
"""

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
    
    if 'video_timestamp' in feats:
        feats['video_timestamp'] = pd.to_datetime(feats['video_timestamp'])
        feats['date'] = feats['video_timestamp'].dt.date
    
    if 'worm_index' in feats:
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
def plot_boxes(feats, feat_str, main_div, sub_div = None):
    #violinplot
    
    if sub_div is None:
        ff = sns.boxplot(feats[main_div], feats[feat_str])
    else:
        ff = sns.boxplot(feats[main_div], feats[feat_str], hue=feats[sub_div])
    #ff = sns.violinplot(feats[main_div], feats[feat_str], hue=feats[sub_div])
    ff.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    return ff

def plot_boxes_group(feats, feat_str, main_div, sub_div, group_div, feat_ylim=[]):
    plt.figure()
    
    groups = feats.groupby(group_div)
    tot_g = len(groups)
    for ii, (picker, feats_p) in enumerate(groups):
        feats_p = feats_p.sort_values(by=[main_div,  sub_div], ascending=False)
        
        plt.subplot(tot_g,1, ii + 1)
        ff = plot_boxes(feats_p, feat_str, main_div, sub_div)
        
        plt.title(picker)
        if ii < len(groups)-1:
            ff.get_xaxis().set_ticklabels([])
            ff.set_xlabel('')
        
            
        if len(feat_ylim) == 2:
            ff.set_ylim(feat_ylim)

            
class plot_db(object):
    def __init__(self, db_path, filt_path_range, filt_frac_good, tab_name):
        
        self.db_path = db_path
        self.filt_path_range = filt_path_range
        self.filt_frac_good = filt_frac_good
        self.tab_name = tab_name
        
        self.feats = get_feats_db(db_path, 
                         filt_path_range, 
                         filt_frac_good,
                         tab_name)
    
    def plot(self, feat_div, feat_ylim = [], valid_rows = None):
        
        if valid_rows is None:
            feats_f = self.feats
        else:
            feats_f = self.feats.loc[valid_rows]
        
        
        n_feat_div = len(feat_div)
        
        if n_feat_div <= 3:
            plt.figure()
            plot_boxes(feats_f, *feat_div)
            if feat_ylim:
                plt.ylim(feat_ylim)
        
        elif n_feat_div == 4:
            plot_boxes_group(feats_f, *feat_div, feat_ylim)   
        

if __name__ == '__main__':
    import os
    
    database_dir = '/Users/ajaver/OneDrive - Imperial College London/compare_strains_DB'
    tab_name = 'features_medians'
    filt_path_range = 0
    filt_frac_good = 0
        
    database_name = 'control_experiments_Test_20161027.db'
    db_path = os.path.join(database_dir, database_name)
    
    
    db_obj = plot_db(db_path, filt_path_range, filt_frac_good, tab_name)
    #%%
    db_obj.plot(['length',  'Strain', 'N_Worms', 'Picker'])
    db_obj.plot(['midbody_width',  'Strain', 'N_Worms', 'Picker'])
    #%%
    db_obj.plot(['midbody_speed_pos',  'Strain', 'N_Worms', 'Picker'])
    