#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 11:05:32 2017

@author: ajaver
"""
import pandas as pd
import pymysql

if __name__ == '__main__':
    conn = pymysql.connect(host='localhost', database='single_worm_db')
    
    sql = '''
    SELECT e.strain, e.date, feat_m.* 
    FROM experiments_valid AS e
    JOIN features_means AS feat_m ON e.id = feat_m.experiment_id
    WHERE total_time < 905
    AND total_time > 295
    AND n_valid_skeletons > 120*fps
    '''
    
    df = pd.read_sql(sql, con=conn)
    
    #%%
    
    from scipy.stats import kruskal
    
    index_feats = ['strain', 'experiment_id', 'worm_index', 'n_frames', 'n_valid_skel', 'first_frame']
    feats2check = [x for x in df.columns if not x in index_feats]
    
    results = []
    for feat in feats2check:
        feat_data = df[['strain', feat]]
        dat = [(s, gg[feat].dropna().values) for s, gg in feat_data.groupby('strain')]
        dat = [(s,x) for s,x in dat if len(x) > 10]
        if dat:
            strain_names, samples = zip(*dat)
            
            #k = f_oneway(*samples)
            k = kruskal(*samples)
            
            results.append((feat, k.pvalue, k.statistic))
            
    #%%
    results_df = pd.DataFrame(results, columns = ['feat', 'pvalue', 'statistics'])
    missing_feats = set(feats2check) - set(results_df['feat'])
    bad_feats = results_df[results_df['pvalue']>1e-5].sort_values('pvalue')
    
    good_feats = results_df[results_df['pvalue']<1e-5]
    
    ## MISSING FEATURES ###
    # **coils** feature is broken
    # **crawling** do not occur when the worm is paused
    # **upsilon** and **omega** cannot be negative
    [x for x in missing_feats if not any(f in x for f in ['crawling_amplitude_paused', 'crawling_frequency_paused', 'coils'])]
    
    # **path_curvature** has a sign that does not depend on the ventral/dorsal orientation, so 
    # only abs/neg/pos give a valid value
    # **orientation** is defined with respect to the field of view, so it is useless (unless there was some sort of chemotaxis)
    # **motion_direciton_paused** does not really change when the worm is paused
    [x for x in bad_feats['feat'] if not any(f in x for f in ['orientation', 'path_curvature'])]
    
    #%%
    from scipy.stats import ranksums
    import statsmodels.stats.multitest as smm
    
    strain_g = df.groupby('strain')
    ctr_data = strain_g.get_group('N2')
    
    r_pvalues = []
    for strain, s_data in strain_g:
        if strain == 'N2':
            continue
        for feat in good_feats['feat']:
            x = ctr_data[feat].dropna().values
            y = s_data[feat].dropna().values
            
            if len(y) < 10:
                continue
            
            k = ranksums(x,y)
            r_pvalues.append((strain, feat, k.pvalue))
            
    r_pvalues = pd.DataFrame(r_pvalues, columns=['strain', 'feat', 'pvalue'])
    pvalues_mat = r_pvalues.pivot(index='feat', columns='strain', values='pvalue')
    
    #%%
    
    
    pvalues_mat_corr = pvalues_mat.copy()
    
    for strain in pvalues_mat:
        dat = pvalues_mat[strain]
        good = ~dat.isnull()
        
        pvals = dat[good].values
        reject, pvals_corrected, alphacSidak, alphacBonf = \
            smm.multipletests(pvals, method = 'fdr_tsbky')
        
        pvalues_mat_corr.loc[good, strain] = pvals_corrected
    
    #%%
    
    number_d = pvalues_mat_corr.apply(lambda x : (x<0.01).sum())
    
    #weird
    number_d[number_d==0]
    
    #TEST USING A WINDOW OF N2
    
    '''
    select s.name, g.name, a.name, description from strains as s join genes AS g on gene_id = g.id join alleles as a on allele_id=a.id  where s.name in ('AQ2153', 'AX1743', 'VC1759', 'VC224');
    '''
    
    
    '''
    select CONCAT(results_dir, '/', base_name, '.hdf5') from experiments_valid where strain in ('AQ2153', 'AX1743', 'VC1759', 'VC224');
    '''