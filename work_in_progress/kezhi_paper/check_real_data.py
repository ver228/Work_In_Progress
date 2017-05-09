#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  9 11:34:19 2017

@author: ajaver
"""
import glob
import os
import pymysql
import shutil

def _get_basenames(main_dir):
    all_files = glob.glob(os.path.join(main_dir, '**', '*_features.hdf5'), recursive=True)
    all_files = sorted([os.path.basename(x).replace('_features.hdf5', '') for x in all_files])
    with open('file_names.txt', 'w') as fid:
        fid.write('\n'.join(all_files))

def select_real_files(main_dir):
    valid_strains = {
            "N2":"Schafer Lab N2 (Bristol, UK)",
            "trp-4":"trp-4(sy695)I",
            "tbh-1":"tbh-1(n3247)X"
            }
    
    
    results_data = {}
    for key,valid_strain in valid_strains.items():
        sql = '''
        SELECT results_dir, base_name, date
        FROM experiments AS exp
        JOIN exit_flags AS f ON exit_flag_id = f.id
        JOIN strains AS s ON s.id = strain_id
        JOIN results_summary AS r ON exp.id = r.experiment_id 
        JOIN arenas AS a ON a.id = arena_id
        WHERE genotype = "{}"
        AND f.name = "END"
        AND a.name NOT LIKE "%liquid%"
        AND total_time BETWEEN 880 AND 920
        AND n_valid_skeletons/n_timestamps > 0.65
        '''.format(valid_strain)
        
        
    
        conn = pymysql.connect(host='localhost', database='single_worm_db')
        cur = conn.cursor()    
        cur.execute(sql)
        results = cur.fetchall()
        conn.close()
        
        results_data[key] = results
    
    #filter by date
    trp_date = [x[2] for x in results_data["trp-4"]]
    tbh_date = [x[2] for x in results_data["tbh-1"]]
    bot = min(min(trp_date), min(tbh_date))
    top = max(max(trp_date), max(tbh_date))
    valid_N2 = [x for x in results_data["N2"] if x[2]>=bot and x[2]<=top]
    results_data["N2"] = valid_N2
    
    features_data = []
    for key, data in results_data.items():
        for results_dir, base_name, data in data:
            feat_file = os.path.join(results_dir, base_name + '_features.hdf5')
            features_data.append(feat_file)        
    
    return features_data

def copy_files(dst_dir):
    
    #dst_dir = os.path.join(main_dir, 'real_data')
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    
    feat_files = select_real_files(main_dir)
    for feat_file in feat_files:
        print(os.path.basename(feat_file))
        shutil.copy(feat_file, dst_dir)
        



if __name__ == '__main__':
    main_dir = '/Volumes/behavgenom$/Kezhi/ToAvelino/for_paper/real_data'

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