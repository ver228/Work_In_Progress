#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  9 11:34:19 2017

@author: ajaver
"""
import seaborn as sns
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
import matplotlib.pylab as plt
from matplotlib.backends.backend_pdf import PdfPages

def plot_feats(data):
    #plt.figure(figsize=(15,4))
    fig_list = []
    feats2check = ['head_bend_sd_abs',
                   'neck_bend_sd_abs', 
                   'midbody_bend_sd_abs',
                   'hips_bend_sd_abs',
                   'tail_bend_sd_abs',
                   'head_bend_mean_abs',
                   'neck_bend_mean_abs', 
                   'midbody_bend_mean_abs',
                   'hips_bend_mean_abs',
                   'tail_bend_mean_abs',
                   'head_bend_mean_forward_abs',
                   'neck_bend_mean_forward_abs', 
                   'midbody_bend_mean_forward_abs',
                   'hips_bend_mean_forward_abs',
                   'tail_bend_mean_forward_abs',
                   'head_bend_mean_backward_abs',
                   'neck_bend_mean_backward_abs',
                   'midbody_bend_mean_backward_abs',
                   'hips_bend_mean_backward_abs',
                   'tail_bend_mean_backward_abs',
                   'head_bend_mean_paused_abs',
                   'neck_bend_mean_paused_abs',
                   'midbody_bend_mean_paused_abs',
                   'hips_bend_mean_paused_abs',
                   'tail_bend_mean_paused_abs',
                   'eigen_projection_1_abs',
                   'eigen_projection_2_abs', 
                   'eigen_projection_3_abs',
                   'eigen_projection_4_abs',
                   'eigen_projection_5_abs',
                   'eigen_projection_6_abs',
                   'midbody_speed', 
                   'midbody_speed_abs', 
                   'midbody_speed_neg', 
                   'midbody_speed_pos',
                   'forward_motion_time_ratio',
                   'backward_motion_time_ratio',
                   'paused_motion_time_ratio'
                   ]
    
    for ii, feat_f in enumerate(feats2check):
        fig = plt.figure()
        sns.boxplot(x='strain', y=feat_f, hue ='data_type', data=data)  
        fig_list.append(fig)
    return fig_list

if __name__ == '__main__':
    fields2ignore = ['worm_index', 'n_frames', 'n_valid_skel', 'first_frame',
                     'strain', 'data_type', 'stat_type']
    
    #%%
    dat_simulation = pd.read_csv('simulation_features.csv')
    good = (dat_simulation['stat_type'] == 'means') & \
           (dat_simulation['data_type'] == 'noise')
    dat_simulation = dat_simulation[good]
    dat_simulation['data_type'] = 'simulation'
    #%%
    dat_train = pd.read_csv('train_features.csv')
    dat_train['data_type'] = 'train'
    good = (dat_train['stat_type'] == 'means') & \
           (~dat_train['strain'].isnull())
    dat_train = dat_train[good]
    
    #%%
    dat_real = pd.read_csv('real_features.csv')
    good = (dat_real['stat_type'] == 'means') & \
           (~dat_real['strain'].isnull())
           
    dat_real = dat_real[good]
    
    # randomly select 10 files for each strain
    strain_group = dat_real.groupby('strain')
    dat_real = []
    np.random.seed(101)
    for strain, strain_dat in strain_group:
        dat_real.append(strain_dat.sample(10))
        
    dat_real = pd.concat(dat_real)
    
    #%%
    strain_group = dat_real.groupby('strain')
    dat_ctrl = strain_group.get_group('N2')
    valid_fields = [x for x in dat_ctrl.columns if x not in fields2ignore]
    valid_fields = [x for x in valid_fields if not any(ff in x for ff in \
                                                       ['_backward', '_forward', '_paused'])]
    
    valid_fields = [x for x in valid_fields if not '_bend_' in x or '_abs' in x]
    
    pvalues = pd.DataFrame(np.full((len(valid_fields), 2), np.nan),
                           columns = ['trp-4', 'tbh-1'], index=valid_fields)
    
    
    for strain, dat_strain in strain_group:
        if strain != 'N2':
            for field in valid_fields:
                yy = dat_strain[field].values
                xx = dat_ctrl[field].values
                _, pvalues.loc[field, strain] = ttest_ind(xx,yy)
    #%%
    print('trp-4')
    print(pvalues['trp-4'].sort_values()[:20])
    
    print('tbh-1')
    print(pvalues['tbh-1'].sort_values()[:20])
    
    #%%
    data = pd.concat((dat_real, dat_simulation))
    pdf_file = 'simulation_vs_real_boxplot.pdf'
    fig_list = plot_feats(data)
    with PdfPages(pdf_file) as pdf_id:
        for fig in fig_list:
            pdf_id.savefig(fig)
            plt.close(fig)
    
    data = pd.concat((dat_train, dat_simulation))
    pdf_file = 'training_vs_real_boxplot.pdf'
    fig_list = plot_feats(data)
    with PdfPages(pdf_file) as pdf_id:
        for fig in fig_list:
            pdf_id.savefig(fig)
            plt.close(fig)
    
    #%%
#    good = (all_feats['stat_type'] == 'means') & \
#           (all_feats['data_type'].isin(['real','low_noise']))
#    dat = all_feats[good]
#    
#    for feat_f in ['midbody_speed', 'length', 'midbody_bend_sd_abs']:
#        plt.figure()
#        sns.boxplot(x='strain', hue='data_type', y=feat_f, data=dat)
#    #%%

    #%%
    
    
    
    #all_files = glob.glob(os.path.join(main_dir, '*.hdf5'))
#    all_files = select_files(main_dir)
#    print(len(all_files))
#    
#    all_feats = pd.concat(all_feats)
#    #%%
#    import seaborn as sns
#    
#    feat_f = 'midbody_bend_sd_abs'
#    data = all_feats[['strain', 'simulation', 'stat_type', feat_f]]
#    sns.boxplot(x='strain', y=feat_f, hue='stat_type', data=data)
#    #sns.stripplot(x="strain", y=feat_f, hue='stat_type', data=data, jitter=True);