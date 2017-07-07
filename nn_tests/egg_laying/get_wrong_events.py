#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 17:50:32 2017

@author: ajaver
"""
import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from tierpsy.helper.misc import get_base_name


def plot_probs(eggs, worm_probs, thresh=0.99, plot_log=True):

    def get_possible_eggs(worm_probs, thresh ):
        inds = np.where(worm_probs>thresh)[0]
        inds = inds[np.argsort(worm_probs[inds])][::-1]
        return inds
    
    def _plot_probs(worm_probs, thresh= 0.99, maker='v', col='b'):
        inds = get_possible_eggs(worm_probs, thresh)
        plt.plot(worm_probs, col)
        plt.plot(inds, worm_probs[inds], maker+col)
        
        return inds
    
    
    #eggs, worm_probs_resized, worm_probs_fixed = [results[x] for x in ['eggs', 'worm_probs_resized', 'worm_probs_fixed']]
    
    egg_frames = results.loc[results['true_events']>0, 'true_events'].index
    
    plt.figure()
    _plot_probs(worm_probs, thresh= thresh, maker='o', col='g')
    plt.plot(egg_frames, np.ones(len(egg_frames)), 'xr')
    plt.title('resized')

def createBlocks(flags_vector, min_block_size=0):
    # divide data into groups of continous indexes
    prev_ind = False
    group_ini = []
    group_fin = []
    for ii, flag_ind in enumerate(flags_vector):

        if not prev_ind and flag_ind:
            group_ini.append(ii)
        if prev_ind and not flag_ind:
            # substract one size this is the condition one after the end of the
            # block
            group_fin.append(ii - 1)
        prev_ind = flag_ind
    # append the last index if the group ended in the last index
    if len(group_ini) - len(group_fin) == 1:
        group_fin.append(ii)
    assert len(group_ini) == len(group_fin)

    # change this into a single list of tuples
    groups = list(zip(group_ini, group_fin))

    # remove any group smaller than the min_block_size
    groups = [gg for gg in groups if gg[1] - gg[0] >= min_block_size]
    return groups

if __name__ == '__main__':
    results_dir = '/Users/ajaver/OneDrive - Imperial College London/egg_laying/results'
    thresh = 0.99
    
    fnames = glob.glob(os.path.join(results_dir, '*.csv'))
    
    tot_eggs = 0
    tot_bad_eggs = 0
    tot_bad_pred = 0
    bad_props = []
    bad_egg_files = []
    for ii, fname in enumerate(fnames):
        base_name = get_base_name(fname)
        print(base_name)
        results = pd.read_csv(fname, index_col=0)
        
        pred_inds = np.where(results['egg_prob']>thresh)[0]
        real_inds = np.where(results['true_events']>0)[0]
        
        dist_d = np.abs(pred_inds-real_inds[:, np.newaxis])
        bad = np.min(dist_d, axis=1)>1
        bad_pred = pred_inds[np.any(dist_d>1, axis=0)]
        
        tot_eggs += bad.size
        if np.any(bad):
            n_bad = np.sum(bad)
            tot_bad_eggs += n_bad
            bad_props.append(results.loc[real_inds[bad], 'egg_prob'].values)
            bad_egg_files.append((fname, n_bad))
            
            
            gg = []
            n_groups = 0
            curr = np.nan
            for gi in sorted(bad_pred):
                if np.isnan(curr):
                    gg.append([gi])
                    curr = gi
                    n_groups += 1
                elif gi-curr < 3:
                    gg[n_groups-1].append(gi)
                    curr = gi
                else:
                    curr = np.nan
            tot_bad_pred += n_groups
        
        
        #if ii > 10:
        #    break
        
#        if 'T27E9.9 (ok2371)III on food R_2011_08_11__10_23_19__2' in fname:
#            plot_probs(results['true_events'],
#                       results['egg_prob'], 
#                       thresh=thresh)
#            break