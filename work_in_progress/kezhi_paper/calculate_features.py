#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 14:13:06 2017

@author: ajaver
"""
import glob
import os
import tables
import pandas  as pd
import multiprocessing as mp

import open_worm_analysis_toolbox as mv
from tierpsy.helper.misc import TimeCounter
from tierpsy.analysis.feat_create.obtainFeaturesHelper import WormStats
from tierpsy.analysis.feat_create.obtainFeatures import FUNC_FOR_DIV

def _get_type_str(basename, types_list):
            type_str = ''
            for ss in types_list:
                if ss in basename:
                    type_str = ss
                    break
            return type_str
    
def get_strain(basename):
    strain = _get_type_str(basename, ['N2', 'tbh-1', 'trp-4'])
    if not strain:
        strain = ''
    return strain

def get_data_type(basename):
    simulation_dict = {
            'generated_info.mat':'no_noise', 
            'generated_Lnoise_info.mat':'low_noise', 
            'generated_noise_info.mat':'noise'
            }
    simulation_str = _get_type_str(basename, 
                       ['generated_info.mat', 
                        'generated_Lnoise_info.mat', 
                        'generated_noise_info.mat']
                       )
    
    if simulation_str:
        data_type = simulation_dict[simulation_str]
    else:
        data_type = 'real'
    return data_type

def concat_dataframe(fname, worm_stat):
    bn = os.path.basename(fname)
    strain = get_strain(bn)
    simulation = get_data_type(bn)
    
    all_feats = []
    for stat_type, feats in worm_stat.items():
        feats_d = pd.DataFrame(feats)
        feats_d['strain'] = strain
        feats_d['data_type'] = simulation
        feats_d['stat_type'] = stat_type
        all_feats.append(feats_d)
    
    return pd.concat(all_feats)
    

def calculate_feat_stats_cnt(fname):
    print(os.path.basename(fname))
    
    def _read_points(fid, field):
        dat = fid.get_node(field)[:]
        vec = [x[0] for x in dat]
        return vec
    
    field_names = {
            'skeletons':'/all_skeletons',
            'cnt_dorsal':'/all_non_vulva_contours',
            'cnt_ventral':'/all_vulva_contours'
            }
    
    with tables.File(fname, 'r') as fid:
        data = {key:_read_points(fid, field) for key, field in field_names.items()}
    
    bw = mv.BasicWorm.from_contour_factory(data['cnt_ventral'], data['cnt_dorsal'])
    nw = mv.NormalizedWorm.from_BasicWorm_factory(bw)
    
    #it seems that the skeletons are in micrometers
    bw.video_info.fps = 10 #the simulated data is corrected in time
    
    wf = mv.WormFeatures(nw)
    
    wStats = WormStats()
    
    worm_stat = {}
    for stat, func in FUNC_FOR_DIV.items():
        worm_stat[stat] = wStats.getWormStats(wf, func)
         
    return concat_dataframe(fname, worm_stat)

def exec_parallel(input_data, func):
    print('*******', len(input_data))
    progress_timer = TimeCounter()
    
    n_batch = mp.cpu_count()
    p = mp.Pool(n_batch)
    tot = len(input_data)
    
    #all_files = all_files[slice(0, len(all_files), 10)] #FOR TESTING
    output_data = []
    for ii in range(0, tot, n_batch):
        dat = input_data[ii:ii + n_batch]
        for x in p.map(func, dat):
            output_data.append(x)
        
        print('{} of {}. Total time: {}'.format(min(ii + n_batch, tot), 
                  tot, progress_timer.get_time_str()))
    
    return output_data



if __name__ == '__main__':
    main_dir = '/Volumes/behavgenom$/Kezhi/ToAvelino/for_paper'
    simulation_files = glob.glob(os.path.join(main_dir, '**', '*.mat'), recursive=True)
    simulation_feats =  exec_parallel(simulation_files, calculate_feat_stats_cnt)
    
    simulation_feats = pd.concat(simulation_feats)
    simulation_feats.to_csv('simulation_features.csv')
    #%%
    import seaborn as sns
    feat_f = 'midbody_bend_sd_abs'
    
    data = simulation_feats[['strain', 'data_type', 'stat_type', feat_f]]
    #data[feat_f] /= 3
    sns.factorplot(x="strain", y=feat_f, hue="stat_type",
               col="data_type", data=data, kind='box',
               size=4, aspect=.5);

         
    