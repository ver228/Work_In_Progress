#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 10:44:56 2017

@author: ajaver
"""

import tables
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import os
import seaborn as sns
import statsmodels.stats.multitest as smm
from scipy.stats import ttest_ind
from collections import OrderedDict
from matplotlib.backends.backend_pdf import PdfPages

from tierpsy.helper.misc import replace_subdir, remove_ext
from tierpsy.helper.params import read_fps


REGIONS = ['Before_All', 'Before', 'During', 'After', 'After_All']


signed_ventral_feats = ['head_bend_mean', 'neck_bend_mean', 
                'midbody_bend_mean', 'hips_bend_mean', 
                'tail_bend_mean', 'head_bend_sd', 'neck_bend_sd', 
                'midbody_bend_sd', 'hips_bend_sd', 'tail_bend_sd', 
                'tail_to_head_orientation', 'head_orientation', 
                'tail_orientation', 'eigen_projection_1', 
                'eigen_projection_2', 'eigen_projection_3', 
                'eigen_projection_4', 'eigen_projection_5', 
                'eigen_projection_6', 'head_tip_motion_direction', 
                'head_motion_direction', 'midbody_motion_direction', 
                'tail_motion_direction', 'tail_tip_motion_direction', 
                'foraging_amplitude', 'foraging_speed', 
                'head_crawling_amplitude', 'midbody_crawling_amplitude', 
                'tail_crawling_amplitude', 'head_crawling_frequency', 
                'midbody_crawling_frequency', 'tail_crawling_frequency', 
                'path_curvature']

def get_regions(light_on, expected_pulse_size, base_window):
    turn_on, turn_off = get_pulses_indexes(light_on, expected_pulse_size)
    assert turn_on.size == 1 and turn_off.size == 1
    turn_on = turn_on[0]
    turn_off = turn_off[0]
    
    ranges_f = [
            (0, turn_on),
            (turn_on-base_window, turn_on),
            (turn_on, turn_off),
            (turn_off, turn_off+base_window),
            (turn_off, light_on.size-1)
            ]
    
    
    feat_ranges = {lab:rr for lab, rr in zip(REGIONS, ranges_f)}
    return feat_ranges


def read_light_data(mask_file):
    with tables.File(mask_file) as fid:
        mean_intensity = fid.get_node('/mean_intensity')[:]
    
    
    med = np.median(mean_intensity)
    mad = np.median(np.abs(mean_intensity-med))
    #the MAD is releated to sigma by the factor below as explained here:
    #wiki (https://en.wikipedia.org/wiki/Median_absolute_deviation#relation_to_standard_deviation)
    s = mad*1.4826 
    
    #... and since the median should be equal to the mean in a gaussian dist
    # we can use 6 sigma as our threshold
    light_on = mean_intensity >  med + s*6
    
    return light_on

def get_pulses_indexes(light_on, window_size):
    switches = np.diff(light_on.astype(np.int))
    turn_on, = np.where(switches==1)
    turn_off, = np.where(switches==-1)
    
    assert turn_on.size == turn_off.size
    
    delP = turn_off - turn_on
    
    good = delP>window_size/2
    
    
    return turn_on[good], turn_off[good]



def get_names(results_dir, base_name):
    feat_file = os.path.join(results_dir, base_name + '_feat_manual.hdf5')
    
    mask_dir = replace_subdir(results_dir, 'Results', 'MaskedVideos')
    if not os.path.exists(mask_dir):
        mask_dir = results_dir
    
    mask_file = os.path.join(mask_dir, base_name +'.hdf5')
    
    return feat_file, mask_file

def get_exp_group(base_name):
    for vt in ['control', 'herm', 'male']:
        if vt in base_name:
            return vt
    raise ValueError()

def plot_region(feat_dat):
    fig = plt.figure()
    lab_order = REGIONS
    sns.boxplot(x="region", 
                     y="val",
                     data=feat_dat, 
                     order=lab_order,
                     palette="binary")
    
    ax2 =sns.stripplot(x="region", 
                      y="val",
                      data=feat_dat, 
                      order=lab_order,
                      hue='base_name',
                      jitter=True)
    plt.ylabel('')
    plt.xlabel('')
    ax2.legend_.remove()
    return fig
    
def read_input(results_dir, base_name, base_window_s, expected_pulse_size_s):
    feat_file, mask_file = get_names(results_dir, base_name)
    fps = read_fps(feat_file)
    expected_pulse_size = fps*expected_pulse_size_s
    base_window = fps*base_window_s
    
    
    
    light_on = read_light_data(mask_file)
    feat_ranges = get_regions(light_on, expected_pulse_size, base_window)
    
    #read features
    with pd.HDFStore(feat_file, 'r') as fid:
        feat_timeseries = fid['/features_timeseries']
    feat_timeseries['timestamp'] = feat_timeseries['timestamp'].astype(np.int)
    
    for feat in signed_ventral_feats:
        feat_timeseries[feat] = feat_timeseries[feat].abs()
    
    
    return feat_ranges, feat_timeseries, fps
#%%
def plot_timeseries(xx, yy, vlines, str_t):
    fig = plt.figure(figsize=(12,5))
    plt.plot(xx,yy)
    yl = plt.ylim()
    plt.plot((vlines[2], vlines[2]), yl, 'r:')
    plt.plot((vlines[3], vlines[3]), yl , 'r:')
    
    plt.plot((vlines[1], vlines[1]), yl, 'k:')
    plt.plot((vlines[4], vlines[4]), yl , 'k:')
    plt.xlim((vlines[0], vlines[-1]))
    plt.ylabel(feat)
    
    plt.xlabel('Time (s)')
    plt.title(str_t)
    return fig

def get_data_for_plot(valid_feats, results_dir, base_name, base_window_s, expected_pulse_size_s):
    
    feat_ranges, feat_timeseries, fps = \
    read_input(results_dir, base_name, base_window_s, expected_pulse_size_s)
    
    turn_on, turn_off =  feat_ranges['During']
    
    feat_ind_gg = feat_timeseries.groupby('worm_index')
    traj_ranges = feat_ind_gg.agg({'timestamp':['min', 'max']})
    traj_ranges = traj_ranges['timestamp']
    
    good = (traj_ranges['min']<turn_on) & (traj_ranges['max']>turn_off)
    valid_ind = traj_ranges[good] .index.values
    
    feat_plots = {x:[] for x in valid_feats}
    for ind in valid_ind:
        feats_dat = feat_ind_gg.get_group(ind)
        for feat in valid_feats:
            str_t = '{} : {}'.format(int(ind), base_name)
            
            yy = feats_dat[feat].values
            tt = feats_dat['timestamp'].values
            xx = tt/fps
            
            xP2, xP3 = [x/fps for x in feat_ranges['During']]
            xP1 = feat_ranges['Before'][0]/fps
            xP4 = feat_ranges['After'][1]/fps
            
            dd = base_window_s/4
            xP0 = xP1 - dd
            xP5 = xP4 + dd
            
            vlines = [xP0, xP1, xP2, xP3, xP4, xP5]
            
            
            
            feat_plots[feat].append((xx, yy, vlines, str_t))
    
    return feat_plots

#%%    
if __name__ == '__main__':
    
    #results_dir = '/Volumes/behavgenom_archive$/Avelino/screening/David_Miller/Results/ATR_210417/'
    results_dir = '/Users/ajaver/OneDrive - Imperial College London/optogenetics/Arantza/Results/oig8'
    
    expected_pulse_size_s = 2
    base_window_s = 120
    
    pval_th = 0.05
    
    
    fnames = [x for x in os.listdir(results_dir) if x.endswith('.hdf5')]
    base_names = set(map(remove_ext, fnames))
    
    results = []
    all_data = {} 
    for base_name in sorted(base_names):
        print(base_name)
        
        exp_group = get_exp_group(base_name)
        if not exp_group in all_data:
            all_data[exp_group] = []
        all_data[exp_group].append(base_name)
        
        #read inputs
        feat_ranges, feat_timeseries, _ = \
        read_input(results_dir, base_name, base_window_s, expected_pulse_size_s)
        
        #get regions
        index_cols = ['worm_index', 'timestamp', 'skeleton_id', 'motion_modes']
        valid_cols = [x for x in feat_timeseries.columns if not x in index_cols]
        for region, (ini, fin) in feat_ranges.items():
            good = (feat_timeseries['timestamp']>ini) & (feat_timeseries['timestamp']<fin)
            feats = feat_timeseries.loc[good, valid_cols]
            
            feats_q = feats.quantile([0.1, 0.5, 0.9])
            
            for feat, dat_q in feats_q.items():
                for q, val in dat_q.items():
                    feat_q = '{}_{}'.format(feat, int(round(q*100)))
                    
                    results.append((exp_group, base_name, region, feat_q, val))
            
    #%%
    results = pd.DataFrame(results, columns=['exp_group', 'base_name', 'region', 'feat_q', 'val'])
    #%%
    dd = [('BA-AA', ('Before_All', 'After_All')),
            ('B-A', ('Before', 'After')),
            ('B-D', ('Before', 'During')),
            ('D-A', ('During', 'After'))
            ]
    comparisons = OrderedDict()
    for key, rr in dd:
        comparisons[key] = rr
    #%%
    pvalues = {}
    pvalues_corr = {}
    significant_feats = {}
    for exp_group, feat_exp in results.groupby('exp_group'):
        #calculate p values using ttest
        exp_pvals = []
        for feat_q, feat_dat in feat_exp.groupby('feat_q'):
            region_gg = feat_dat.groupby('region')
            
            pv = []
            for lab, (s1, s2) in comparisons.items():
                x = region_gg.get_group(s1)['val']
                y = region_gg.get_group(s2)['val']
                _, p = ttest_ind(x, y)
                pv.append(p)
            exp_pvals.append((feat_q, pv))
        
        feats, pvals  = zip(*exp_pvals)
        exp_pvals_df = pd.DataFrame(np.array(pvals), feats, columns=comparisons.keys())
        
        #correct for multiple hypothesis comparisons
        
        p_corr_df = exp_pvals_df.copy() # I only copy to avoid having to worry about initializations
        p_corr_df = p_corr_df.dropna()
        for col in p_corr_df:
            reject, pvals_corrected, alphacSidak, alphacBonf = \
                smm.multipletests(p_corr_df[col].values, method = 'fdr_tsbky')
            p_corr_df[col] = pvals_corrected
        
        #%%
#        for feat, dat in p_corr_df.iterrows():
#            reject, pvals_corrected, alphacSidak, alphacBonf = \
#                smm.multipletests(dat.values, method = 'fdr_tsbky')
#            p_corr_df.loc[feat] = pvals_corrected
        #%%
        
        #find features where at least one pval is above 0.1
        dd = p_corr_df.min(axis=1)
        valid_feats = dd[dd<pval_th].index.values
        valid_feats = sorted(valid_feats, key=lambda x:dd[x])
        
        #store results
        pvalues[exp_group] = exp_pvals_df
        pvalues_corr[exp_group] = p_corr_df
        
        significant_feats[exp_group] = valid_feats
#%% 
    tlabel = {'control':'Males Control', 'herm':'Hermaphrodites', 'male':'Males'}
    for exp_group, feat_exp in results.groupby('exp_group'):
        p_corr_df = pvalues_corr[exp_group]
        
         
        exp_name = tlabel[exp_group]
        
        
        if len(significant_feats[exp_group]) == 0:
            #do not create an empty file if there are not valid feats
            continue
        
        with PdfPages(exp_name + '.pdf') as pdf:
            feat_gg = feat_exp.groupby('feat_q')
            for feat in significant_feats[exp_group]:
                feat_dat = feat_gg.get_group(feat)
                
                fig = plot_region(feat_dat)
                dd = []
                for k,x in p_corr_df.loc[feat].items():
                    pp = '{} : {:.3f}'.format(k,x)
                    if x < pval_th:
                        pp += '*'
                    dd.append(pp)
                p_str = ' | '.join(dd)
                
                bot, top = plt.ylim()
                top = 1.1*top
                plt.ylim((bot, top))
                plt.text(0.1, 0.95,p_str, transform=fig.gca().transAxes)
                
                str_t = '{} | {} {}th'.format(exp_name, feat[:-3], feat[-2:])
                
                plt.title(str_t)
                
                pdf.savefig(fig)
                
                plt.close(fig)
    #%%
    
    for exp_group in significant_feats:
        if len(significant_feats[exp_group]) == 0:
            #do not create an empty file if there are not valid feats
            continue
        
        valid_feats = significant_feats[exp_group]
        valid_feats = sorted(set([x[:-3] for x in valid_feats]))
        
        plot_dat = {x:[] for x in valid_feats}
        for base_name in all_data[exp_group]:
        
            plot_dat_bn = get_data_for_plot(valid_feats, 
                                         results_dir, 
                                         base_name, 
                                         base_window_s, 
                                         expected_pulse_size_s)
            for x in plot_dat_bn:
                plot_dat[x] += plot_dat_bn[x]
        
        
        #%%
        exp_name = tlabel[exp_group]
        for feat in plot_dat:
            fname_pdf = '{} {}.pdf'.format(exp_name, feat)
            with PdfPages(fname_pdf) as pdf:
                for dat in plot_dat[feat]:
                    fig = plot_timeseries(*dat)
                    pdf.savefig(fig)
                    plt.close(fig)
#%%
    for x in valid_cols:
        print(x)

#%%

