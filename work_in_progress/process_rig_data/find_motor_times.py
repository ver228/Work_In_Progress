#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 15:37:43 2016

@author: ajaver
"""

import os

from plot_db import plot_db
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns
import pandas as pd

if __name__ == '__main__':
    database_dir = '/Users/ajaver/OneDrive - Imperial College London/compare_strains_DB'
    tab_name = 'features_medians_split'
    filt_path_range = 0
    filt_frac_good = 0
        
    #database_name = 'control_experiments_Agar_Test.db'
    database_name = 'control_experiments_Test_Food.db'
    db_path = os.path.join(database_dir, database_name)
    db_obj = plot_db(db_path, filt_path_range, filt_frac_good, tab_name)
    #%%
    #experiments = db_obj.experiments
    #'length'
    #'midbody_speed_pos'
    bn_fun = lambda x : '_'.join(x.split('_')[:-2])
    db_obj.feats['base_name_d'] = db_obj.feats['base_name'].apply(bn_fun)
    db_obj.feats['start_min'] = db_obj.feats['first_frame']/25/60 + db_obj.feats["delta_time_min"]
    
    #%%
    #db_obj.feats['midbody_speed_pos_log'] = np.log10(db_obj.feats['midbody_speed_pos'])
    #%%
    #midbody_speed_pos #length
#    
#    g = sns.lmplot(x="start_min", 
#               y="midbody_speed_pos", 
#               col="exp_name", 
#               hue="Strain", 
#               data=db_obj.feats,
#               col_wrap=2, 
#               size=3)   
#    g.set(yscale="log")
#    g.set(ylim=(500, 2000))
#    g.set(xlim=(-5, 625))
    #%%
    
    #%%
#    feat_name = "length"#"midbody_speed_pos"
#    for exp_name, exp_feats in db_obj.feats.groupby('exp_name'):
#        g = sns.lmplot(x="start_min", 
#               y=feat_name, 
#               col="Strain", 
#               data=exp_feats,
#               #hue='N_Worms',
#               hue= 'Old/New Agar',
#               col_wrap=2, 
#               size=3)
#        g.set(ylim=(500, 1800))
#        g.set(xlim=(-5, 625))
    #%%
#    feat_name = "length"#"midbody_speed_pos"
#    for exp_name, exp_feats in db_obj.feats.groupby('exp_name'):
#        for strain, strain_feats in db_obj.feats.groupby('Strain'):
#            plt.figure()
#            
#            for vid_name, vid_feats in strain_feats.groupby('base_name_d'):
#                if len(exp_feats['base_name'].unique()) == 1:
#                    continue
#                
#                g = sns.regplot(x="start_min", 
#                       y=feat_name, 
#                       data=vid_feats)
#                #g.set_title(vid_name)
#            
#            g.set(ylim=(500, 1800))
#            g.set(xlim=(-5, 625))
#            plt.title(strain)
#        break

    #%%
    
    
    #%%
    feat_name = "length"#"midbody_speed_pos"
    for exp_name, exp_feats in db_obj.feats.groupby('exp_name'):
        print(exp_name)
        #if exp_name != 'Agar_Screening_181116': #'Agar_Screening_181116'
        #    continue
        
        for strain, strain_feats in db_obj.feats.groupby('Strain'):
            g = sns.lmplot(x="start_min", 
               y=feat_name, 
               col='sample_id',
               data=strain_feats,
               col_wrap=5, 
               size=3)
            g.set(ylim=(500, 1800))
            g.set(xlim=(-5, 625))
        break
    
    
    
    #%%
    import patsy
    import statsmodels.api as sm
    
    f = 'length ~ start_min'
    ols_fits = {}
    for sample_id, strain_feats in db_obj.feats.groupby('sample_id'):
        y,X = patsy.dmatrices(f, strain_feats, return_type='dataframe')
        ols_fits[sample_id] = sm.OLS(y,X).fit()
    #%%
    sample_dat = db_obj.experiments.drop_duplicates('sample_id')
    sample_dat.index = sample_dat['sample_id']
    
    sample_id,dat = zip(*((sample_id, (dat.params['Intercept'], dat.params['start_min'])) 
                                for sample_id, dat in ols_fits.items()))
    fit_df = pd.DataFrame(np.array(dat), sample_id, ['Intercept', 'start_min'])
    
    sample_dat = sample_dat.join(fit_df)
    
    #%%
    hue_feat = 'exp_name'#'N_Worms'#'Food_Conc'#'Old/New Agar'
    g = sns.FacetGrid(sample_dat, col="Strain", hue=hue_feat, col_wrap=2)
    g.map(plt.scatter, 'sample_id', 'start_min')
    g.add_legend();
    
    g = sns.FacetGrid(sample_dat, col="Strain", hue=hue_feat, col_wrap=2)
    g.map(plt.scatter, 'sample_id', 'Intercept')
    g.add_legend();
    #%%
    x_feat = 'n_valid_skel' #'start_min' #'first_frame'#'n_frames' #
    #y_feat = "midbody_speed_abs" 
    y_feat = "length"#
    
    for strain, strain_feats in db_obj.feats.groupby('Strain'):
        g = sns.FacetGrid(strain_feats, col_wrap=4, col="sample_id")
        g.map(plt.scatter, x_feat, y_feat)
        plt.subplots_adjust(top=0.9)
        g.fig.suptitle(strain)
    
    #%%
    #feat_name = "length"#"midbody_speed_pos"
    #g = sns.FacetGrid(db_obj.feats, row="Strain")
    #g.map(sns.coefplot, formula='length~start_min', groupby='sample_id')
    #%%
#    for exp_name, exp_feats in db_obj.feats.groupby('exp_name'):
#        print(exp_name)
#        #if exp_name != 'Agar_Screening_181116': #'Agar_Screening_181116'
#        #    continue
#        #plt.figure()
#        for ii, (strain, strain_feats) in enumerate(db_obj.feats.groupby('Strain')):
#            #plt.subplot(2,2, ii+1) 
#            g = sns.coefplot('length~start_min', strain_feats, groupby='sample_id')
#            plt.title(strain)
#            
#        break
    
    #%%
#               col_wrap=2, 
#
#        g.set(ylim=(500, 1800))
#        g.set(xlim=(-5, 625))
#        plt.title(strain)
        #break
    #%%
#    for exp_name, dat in experiments.groupby('exp_name'):
#        print('***************')
#        print(exp_name)
#        for bn in dat['base_name_d'].unique():
#            print(bn)