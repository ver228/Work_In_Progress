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
    
    feats2check = ['eigen_projection_2_pos', 'eigen_projection_2_abs',
       'forward_motion_frequency', 'backward_motion_time_ratio',
       'head_motion_direction_neg', 'eigen_projection_3_neg',
       'head_motion_direction_abs', 'paused_motion_time_ratio',
       'head_speed_neg', 'head_tip_speed_neg', 'tail_bend_sd_abs',
       'head_motion_direction_pos', 'tail_tip_speed_neg', 'path_curvature_pos',
       'tail_speed_neg', 'path_curvature_abs', 'backward_motion_frequency',
       'midbody_speed_neg', 'eigen_projection_1_pos', 'path_curvature_neg']
    '''
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
                   'paused_motion_time_ratio',
                   'foraging_amplitude',
                   'foraging_amplitude_abs', 
                   'foraging_amplitude_neg', 
                   'foraging_amplitude_pos', 
                   'foraging_amplitude_forward', 
                   'foraging_amplitude_forward_abs', 
                   'foraging_amplitude_forward_neg', 
                   'foraging_amplitude_forward_pos', 
                   'foraging_amplitude_paused', 
                   'foraging_amplitude_paused_abs', 
                   'foraging_amplitude_paused_neg', 
                   'foraging_amplitude_paused_pos', 
                   'foraging_amplitude_backward', 
                   'foraging_amplitude_backward_abs', 
                   'foraging_amplitude_backward_neg', 
                   'foraging_amplitude_backward_pos', 
                   'foraging_speed', 
                   'foraging_speed_abs', 
                   'foraging_speed_neg', 
                   'foraging_speed_pos', 
                   'foraging_speed_forward', 
                   'foraging_speed_forward_abs', 
                   'foraging_speed_forward_neg', 
                   'foraging_speed_forward_pos', 
                   'foraging_speed_paused', 
                   'foraging_speed_paused_abs', 
                   'foraging_speed_paused_neg', 
                   'foraging_speed_paused_pos', 
                   'foraging_speed_backward', 
                   'foraging_speed_backward_abs', 
                   'foraging_speed_backward_neg', 
                   'foraging_speed_backward_pos'
                   ]
    '''
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
    
    
    pvalues = pd.DataFrame(np.full((len(valid_fields), 3), np.nan),
                           columns = ['trp-4', 'tbh-1', 'CB4856'], index=valid_fields)
    
    
    for strain, dat_strain in strain_group:
        if strain != 'N2':
            for field in valid_fields:
                yy = dat_strain[field].values
                xx = dat_ctrl[field].values
                _, pvalues.loc[field, strain] = ttest_ind(xx,yy)
    #%%
    print('trp-4')
    print(pvalues['trp-4'].sort_values()[:20])
    
    print('tbhc-1')
    print(pvalues['tbh-1'].sort_values()[:20])
    
    print('CB4856')
    print(pvalues['CB4856'].sort_values()[:20])
    #%%
#    data = pd.concat((dat_real, dat_simulation))
#    pdf_file = 'simulation_vs_real_boxplot.pdf'
#    fig_list = plot_feats(data)
#    with PdfPages(pdf_file) as pdf_id:
#        for fig in fig_list:
#            pdf_id.savefig(fig)
#            plt.close(fig)
#    
#    data = pd.concat((dat_train, dat_simulation))
#    pdf_file = 'training_vs_real_boxplot.pdf'
#    fig_list = plot_feats(data)
#    with PdfPages(pdf_file) as pdf_id:
#        for fig in fig_list:
#            pdf_id.savefig(fig)
#            plt.close(fig)
    #%%
    data = pd.concat((dat_train, dat_simulation))
    
    fig1= plt.figure(figsize=(7,5))
    data_strain = data[data['strain'].isin(['N2', 'trp-4'])]
    ax = sns.boxplot(x='strain', 
                y='head_bend_mean_abs', 
                hue ='data_type', 
                data=data_strain) 
    ax.legend_.remove()
    ax.legend(loc='best')
    
    
    
    fig2=plt.figure(figsize=(7,5))
    data_strain =  data[data['strain'].isin(['N2', 'tbh-1'])]
    sns.boxplot(x='strain', 
                y='forward_motion_frequency', 
                hue ='data_type', 
                data=data_strain) 
    ax.legend_.remove()
    ax.legend(loc='best')
    
    pdf_file = 'simulation_vs_train_boxplot.pdf'
    with PdfPages(pdf_file) as pdf_id:
        for fig in [fig1, fig2]:
            pdf_id.savefig(fig)
            plt.close(fig)
    #%%
    data = pd.concat((dat_train, dat_simulation))
    valid_strains = ['N2', 'CB4856']
    pdf_file = 'CB4856_simulation_vs_train_boxplot.pdf'
    with PdfPages(pdf_file) as pdf_id:
        for feat in ['head_speed_pos', 'midbody_speed_pos', 'tail_speed_pos']:
            fig=plt.figure(figsize=(7,5))
            data_strain =  data[data['strain'].isin(valid_strains)]
            sns.boxplot(x='strain', 
                        y=feat, 
                        hue ='data_type', 
                        data=data_strain,
                        order=valid_strains) 
            ax.legend_.remove()
            ax.legend(loc='best')
            pdf_id.savefig(fig)
    

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