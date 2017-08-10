
"""
@author: ajaver
"""

import tables
import numpy as np
import os
import glob
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

import seaborn as sns
from tierpsy.helper.misc import replace_subdir, remove_ext
from tierpsy.helper.params import read_fps
#from scipy.stats import ttest_ind

from scipy.stats import ranksums, wilcoxon, ttest_ind
import statsmodels.stats.multitest as smm

import matplotlib.pylab as plt

from tierpsy.analysis.feat_create.obtainFeaturesHelper import WormStats

from oig8_pulses import read_input, get_names


wStats = WormStats()
feat_avg_names = []
for feat_name, feat_info in wStats.features_info.iterrows():
    motion_types = ['']
    if feat_info['is_time_series']:
        motion_types += ['_forward', '_paused', '_backward']
    
    for mtype in motion_types:
        sub_name = feat_name + mtype
        if feat_info['is_signed']:
            feat_avg_names.append(sub_name + '_abs')
            #if 'speed' in feat_name:
            #    for atype in ['', '_abs', '_neg', '_pos']:
            #        feat_avg_names.append(sub_name + atype)
            #else:
            #    feat_avg_names.append(sub_name + '_abs')

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



def get_p_values(dat):
    #%%
    feat_x = dat[dat['region']=='Before']
    feat_y = dat[dat['region']=='After']
        
    p_values = []
    for feat in feat_avg_names:
        x = feat_x[feat]
        x = x.dropna()
        y = feat_y[feat].dropna()
        
        if x.size > 0 and y.size > 0:
            _, p = ttest_ind(x, y)
        else:
            p = np.nan
        p_values.append((feat, p))
    
    feats, p_val = zip(*p_values)
    p_values = pd.Series(p_val, index=feats).dropna()
    p_values = p_values.sort_values(ascending=True)
    
    if p_values.size > 0:
        reject, pvals_corrected, alphacSidak, alphacBonf = \
            smm.multipletests(p_values.values, method = 'fdr_tsbky')
            
        pvals_corrected = pd.Series(pvals_corrected, index=p_values.index)
    else:
        pvals_corrected = pd.Series()
    #%%
    return p_values, pvals_corrected
#%%
def get_vid_type(base_name):
    if 'control' in base_name:
        vid_type = 'Control'
    elif 'herm' in base_name:
        vid_type = 'Hermaphrodite'
    elif 'male' in base_name:
        vid_type = 'Male'
    else:
        raise ValueError()
        
    return vid_type
#%%
if __name__ == '__main__':
    results_dir = '/Users/ajaver/OneDrive - Imperial College London/optogenetics/Arantza/Results/oig8'

    #mask_dir = '/Volumes/behavgenom_archive$/Avelino/screening/Arantza/MaskedVideos'
    
    expected_pulse_size_s = 5
    
    min_traj_s = 45
    
    fnames = [x for x in os.listdir(results_dir) if x.endswith('.hdf5')]
    base_names = sorted(set(map(remove_ext, fnames)))
    
    all_data = pd.DataFrame()
    for vid_id, base_name in enumerate(sorted(base_names)):
        feat_file, mask_file = get_names(results_dir, base_name)
        
        vid_type = get_vid_type(base_name)
        
        
        feat_file = replace_subdir(remove_ext(mask_file), 'MaskedVideos', 'Results') + '_feat_manual.hdf5'
        
        light_on = read_light_data(mask_file)
        fps = read_fps(mask_file)
        expected_pulse_size = fps*expected_pulse_size_s
        turn_on, turn_off = get_pulses_indexes(light_on, expected_pulse_size)
        
        min_traj = fps*min_traj_s
        with pd.HDFStore(feat_file, 'r') as fid:
            feats = fid['/features_summary/medians_split']
        
        feats = feats[feats['n_frames']>min_traj]
        
        before_ind = feats['first_frame']+feats['n_frames'] < turn_on[0]
        after_ind = feats['first_frame'] > turn_off[0]
        
        index_cols = ['worm_index', 'n_frames', 'n_valid_skel', 'first_frame']
        valid_cols = [x for x in feats.columns if x not in index_cols]
        
        before_feats = feats.loc[before_ind, valid_cols]
        after_feats = feats.loc[after_ind,  valid_cols]
        
        #mm = before_feats.mean(skipna=True)
        #ss = before_feats.std(skipna=True)
        #before_feats = (before_feats-mm)/ss
        #after_feats = (after_feats-mm)/ss
        
        before_feats['region'] = 'Before'
        after_feats['region'] = 'After'
        feat_vid_N = pd.concat([before_feats, after_feats])
        
        
        
        feat_vid_N['video_id'] = vid_id
        feat_vid_N['vid_type'] = vid_type
        
        all_data = pd.concat([all_data , feat_vid_N])
    
    #%%
    
    feat_dats = {}
    tot_rows = 3
    tot_cols = 5
    tot_plots = tot_rows*tot_cols
    
    lab_order = ['Before', 'After']
    valid_feats = {}
    #video_id vid_type
    for vid_type, dat in all_data.groupby('vid_type'):
        #print(os.path.basename(mask_files[vid_type]))
        p_values, pvals_corrected = get_p_values(dat)
        feat_dats[vid_type] = pvals_corrected
        
        
        val = pvals_corrected[pvals_corrected<0.05]
        val_feats = val.index.values
        
        print(vid_type.upper())
        print(val)
        
        
        if val_feats.size == 0:
            continue
        
        valid_feats[vid_type] = val_feats
        with PdfPages(vid_type + '_traj.pdf') as pdf:
            for iplot, feat in enumerate(val_feats):
                
                fig = plt.figure(figsize=(5,5))
                ax1 =sns.boxplot(x="region", 
                                  y=feat,
                                  data=dat, 
                                  order=lab_order,
                                   palette="binary")
                ax2 =sns.stripplot(x="region", 
                                  y=feat,
                                  data=dat, 
                                  order=lab_order,
                                  hue='video_id',
                                  jitter=True)
                ax2.legend_.remove()
                
                plt.title(feat)
                plt.ylabel('')
                plt.xlabel('')
                bot, top = plt.ylim()
                top = 1.1*top
                
                p_str = 'p=%01.4f    pc=%01.4f' % (p_values[feat], pvals_corrected[feat])
                plt.text(0.1, 0.95,p_str, transform=ax2.transAxes)
                plt.ylim((bot, top))
                
                pdf.savefig(fig)
                plt.close()
    #%%
    vid_groups = {}
    for bn in base_names:
        vid_type = get_vid_type(bn)
        if not vid_type in vid_groups:
            vid_groups[vid_type] = []
        vid_groups[vid_type].append(bn)
    #%%
    
    mean_feats = {}
    for vid_type in vid_groups:
        df = pd.DataFrame()
        #feat_m = []
        for base_name in vid_groups[vid_type]:
            feat_ranges, feat_timeseries, fps = \
            read_input(results_dir, base_name, 0, expected_pulse_size_s)
            turn_on, turn_off = feat_ranges['During']
            
            #I get the absolute value of everything because that's what i get for the features
            feat_timeseries = feat_timeseries.abs()
            
            #normalize data by when the lamp was on
            feat_timeseries['timestamp'] -= turn_on
            
            df = pd.concat((df, feat_timeseries))
            
            #get the mean value at a given timestamp
            #dd = feat_timeseries.groupby('timestamp').agg('mean')
            #feat_m.append(dd)
         
        #mean_feats[vid_type] = feat_m
        mean_feats[vid_type] = df.groupby('timestamp').agg('mean')
        
#%% 
    win_size = int(min_traj_s*fps)
    
    from scipy.signal import medfilt, savgol_filter
    def _clean_name(feat):
        post_fix_s1= ['_abs', '_pos', '_neg']
        post_fix_s2 = ['_forward', '_backward', '_paused']
        
        for ss in post_fix_s1:
            if feat.endswith(ss):
                feat = feat.replace(ss, '')
                break
            
        for ss in post_fix_s2:
            if feat.endswith(ss):
                feat = feat.replace(ss, '')
                break
        return feat
        
    #%%
    for vid_type in valid_feats:
        df = mean_feats[vid_type]
        #vid_dfs = mean_feats[vid_type]
        
        feats = valid_feats[vid_type]
        feats = set(map(_clean_name, feats))
        
        
        for feat in feats:
        #for df in vid_dfs:
            yy = df[feat]
            yys = savgol_filter(yy, win_size, 3, mode='nearest')
            yys[:win_size] = np.nan
            yys[-win_size:] = np.nan
            
            xx = df.index
            
            plt.figure(figsize=(12,5))
            plt.plot(xx, yy, '.', color = '0.75')
            plt.plot(xx, yys, 'r')
            plt.plot((0,0), plt.ylim(), 'k:')
            
            plt.title(feat)




