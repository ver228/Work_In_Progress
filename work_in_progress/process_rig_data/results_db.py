#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 08:19:55 2016

@author: ajaver
"""

import os
import pandas as pd
import matplotlib.pylab as plt

from plot_db import get_feats_db, plot_boxes, plot_boxes_group

from plot_db import plot_db


DATABASE_DIR = '/Users/ajaver/OneDrive - Imperial College London/compare_strains_DB'

def first_test(tab_name, filt_path_range, filt_frac_good):
    #%%
    database_name = 'control_experiments_Test_20161027.db'
    db_path = os.path.join(DATABASE_DIR, database_name)
    db_obj = plot_db(db_path, filt_path_range, filt_frac_good, tab_name)
    
    db_obj.plot(['length',  'Strain', 'Picker'])
    db_obj.plot(['midbody_speed_pos',  'Strain', 'Picker'])
    db_obj.plot(['midbody_speed_pos', 'N_Worms', 'Picker'])
    

def food_test(tab_name, filt_path_range, filt_frac_good):
    #%%
    database_name = 'control_experiments_Test_Food.db'
    db_path = os.path.join(DATABASE_DIR, database_name)
    db_obj = plot_db(db_path, filt_path_range, filt_frac_good, tab_name)
    db_obj.plot(['length',  'Strain', 'Picker'])
    db_obj.plot(['midbody_speed_pos',  'Strain', 'Food_Conc'], [])
    db_obj.plot(['midbody_speed_pos',  'Strain', 'Food_Conc'], [0, 500])

    
    #%%
def agar_test(tab_name, filt_path_range, filt_frac_good):
    #%%
    database_name = 'control_experiments_Agar_Test.db'
    db_path = os.path.join(DATABASE_DIR, database_name)
    db_obj = plot_db(db_path, filt_path_range, filt_frac_good, tab_name)
    
    #% Agar_Screening_181116 seems to be wrongly labeled
    db_obj.plot(['midbody_speed_pos',  'Strain', 'Old/New Agar', 'exp_name'], [])
    db_obj.plot(['length',  'Strain', 'Old/New Agar', 'exp_name'], [])
#%%    
def main1():
    database_dir = '/Users/ajaver/OneDrive - Imperial College London/compare_strains_DB'
    #first_test(database_dir)
    #test_food(database_dir)
    #agar_test(database_dir)
    
    database_name = os.path.join(database_dir, 'control_experiments_single_worm_protocol.db')
    feats = get_feats_db(database_name, 
                         filt_path_range = 10, 
                         filt_frac_good = 0.5,
                         tab_name = 'features_means_split')
    
    #%%
    feats['Pick_type'] = feats['Pick_type'].str.lower()
    feat_str = 'length'
    feat_ylim = []#[0, 500]
    
    plt.figure()
    plot_boxes(feats, feat_str, 'Strain', 'Picker')
    if feat_ylim:
        plt.ylim(feat_ylim)
    
    plt.figure()
    plot_boxes(feats, feat_str, 'Strain', 'Pick_type')
    if feat_ylim:
        plt.ylim(feat_ylim)
    
    plt.figure()
    plot_boxes(feats, feat_str, 'Strain', 'date')
    if feat_ylim:
        plt.ylim(feat_ylim)
    #%%
    plot_boxes_group(feats, feat_str, 'Strain', 'date', 'Pick_type')
    #%%
    feat_str = 'midbody_speed_pos'
    feat_ylim = [0, 350]
    plot_boxes_group(feats, feat_str, 'Pick_type', 'Strain', 'date', feat_ylim)
    plot_boxes_group(feats, feat_str, 'Picker', 'Strain', 'date', feat_ylim)
#%%
    plot_boxes_group(feats, feat_str, 'N_Worms', 'Strain', 'date', feat_ylim)
    #%%
    
#%%
    from datetime import datetime
    plt.figure()
    feat_str = 'midbody_speed_pos'
    good = feats['date'] == datetime(2016, 11, 25).date()
    plot_boxes(feats[good], feat_str, 'Pick_type', 'Strain')
    
    #%%
    database_name = os.path.join(database_dir, 'control_single.db')
    feats_single = get_feats_db(database_name, tab_name = 'features_means')
    chg = (feats_single['gene']!=feats_single['gene'])
    feats_single.loc[chg, 'gene'] = 'N2'
    feats_single = feats_single.sort_values(by='gene', ascending=False)
    feats_single = feats_single.rename(columns={'gene':'Strain'})
    
    feats['setup'] = 'W-3 24/11'
    feats_single['setup'] = 'old'
    
    feat_m = pd.concat((feats, feats_single))
    
    good = feat_m['Strain'] != 'HW'
    good = good & (feat_m['date'] == datetime(2016, 11, 24).date())
    good = good & (feat_m['N_Worms'] == 3)
    good = good | (feat_m['setup'] == 'old')
    
    feat_m = feat_m[good]
    #%%
    plt.figure()
    plot_boxes(feat_m, feat_str, 'Strain', 'setup')
    plt.ylim([0, 350])
    #%%
    plt.figure()
    plot_boxes(feat_m, 'length', 'Strain', 'setup')
    #plt.ylim([0, 350])
    #%%
    feats_agar_test = agar_test(database_dir, tab_name = 'features_means_split')
    #%%
    good = feats_agar_test['N_Worms'].isin([3, 10])
    feats = feats_agar_test[good]
    feat_str = 'midbody_speed_pos'
    feat_ylim = [0, 350]
    
    plt.figure()
    plot_boxes(feats, feat_str, 'Picker', 'Strain')
    if feat_ylim:
        plt.ylim(feat_ylim)
    #%%
    plt.figure()
    plot_boxes(feats, feat_str, 'N_Worms', 'Strain')
    if feat_ylim:
        plt.ylim(feat_ylim)
    #%%
    plt.figure()
    plot_boxes(feats, feat_str, 'Old/New Agar', 'Strain')
    if feat_ylim:
        plt.ylim(feat_ylim)
    #%%
    feat_str = 'length'
    plot_boxes_group(feats_agar_test, feat_str, 'Old/New Agar', 'Strain', 'date')   
    plot_boxes_group(feats_agar_test, feat_str, 'Strain', 'N_Worms', 'date')   

#%%
def main2():
    database_dir = '/Users/ajaver/OneDrive - Imperial College London/compare_strains_DB'
    tab_name = 'features_medians'
    filt_path_range = 0
    filt_frac_good = 0
        
    database_name = 'control_experiments_Test_20161027.db'
    
    feats = get_feats_db(os.path.join(database_dir, database_name), 
                         filt_path_range, 
                         filt_frac_good,
                         tab_name)
    
    #%%
    sorted_lengths = feats.length.sort_values()
    largest_row = sorted_lengths.index[0]
    directory = feats.loc[largest_row, 'directory']
    base_name = feats.loc[largest_row, 'base_name']
    
    #%%
    #%%
    feat_str = 'length'
    feat_ylim = (400, 1600)
    
    import seaborn as sns
    sns.boxplot(feats['Strain'], feats[feat_str])
    #%%
    
    #feat_str = 'midbody_speed_pos'
    #feat_ylim = []
    
#    plt.figure()
#    plot_boxes(feats, feat_str, 'Strain', 'Picker')
#    if feat_ylim:
#        plt.ylim(feat_ylim)
#    
#    plt.figure()
#    plot_boxes(feats, feat_str, 'Strain', 'N_Worms')
#    if feat_ylim:
#        plt.ylim(feat_ylim)
#    
#    plot_boxes_group(feats, feat_str, 'Strain', 'N_Worms', 'Picker', feat_ylim)



if __name__ == '__main__':
    #%%
    
    tab_name = 'features_medians_split'
    filt_path_range = 0
    filt_frac_good = 0
    
    #%%
    #first_test(tab_name, filt_path_range, filt_frac_good)
    food_test(tab_name, filt_path_range, filt_frac_good)
    #agar_test(tab_name, filt_path_range, filt_frac_good)
    
    #%%
    database_name = 'control_experiments_short_movies.db'
    db_path = os.path.join(DATABASE_DIR, database_name)
    db_obj = plot_db(db_path, filt_path_range, filt_frac_good, tab_name)
    #%%
    valid_rows = ~db_obj.feats['Vortex'].isnull()#db_obj.feats['exp_name'] == 'single_picking_011216'
    feat_str = ['midbody_speed_pos',  'Strain', 'Vortex', 'exp_name']
    db_obj.plot(feat_str, valid_rows=valid_rows)
    #%%
    valid_rows = db_obj.feats['exp_name'].str.contains('double')
    valid_rows &= ~db_obj.feats['exp_name'].str.contains('after')
    valid_rows &= db_obj.feats['Vortex'] != 1
    
    feat_str = ['midbody_speed_pos',  'Food_Conc', 'Strain', 'exp_name']
    db_obj.plot(feat_str, valid_rows=valid_rows)
    
    