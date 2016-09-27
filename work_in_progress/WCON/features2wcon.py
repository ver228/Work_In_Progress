# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 20:55:19 2016

@author: ajaver
"""

import tables
import pandas as pd
from collections import OrderedDict
import numpy as np
import json

from MWTracker.featuresAnalysis.obtainFeaturesHelper import WormStatsClass

def getMetaData(features_file):
    with tables.File(features_file, 'r') as fid:
        if not '/experiment_info' in fid:
            experiment_info = {}
        else:
            experiment_info_file = fid.get_node('/experiment_info').read()
            experiment_info_file = json.loads(experiment_info_file.decode('utf-8'))
            if not 'lab' in experiment_info_file:
                #I hard code the lab for the moment since all this data base is for the single worm case, and all the data was taken from the schafer lab.
                #if at certain point we add another lab we need to add an extra table in the main database
                experiment_info_file['lab'] = {'name' : 'William R Schafer', 
                'address':'MRC Laboratory of Molecular Biology, Hills Road, Cambridge, CB2 0QH, UK'}
             
            #rename with valid names
            experiment_info = OrderedDict()
            
            experiment_info['base_name'] = experiment_info_file.pop('base_name')
            experiment_info['who'] = experiment_info_file.pop('experimenter')
            experiment_info['lab'] = experiment_info_file.pop('lab')
            
            experiment_info['timestamp'] = experiment_info_file.pop('date')
            experiment_info['arena'] = experiment_info_file.pop('arena')
            experiment_info['food'] = experiment_info_file.pop('food')
            experiment_info['strain'] = experiment_info_file.pop('strain')
            experiment_info['gene'] = experiment_info_file.pop('gene')
            experiment_info['allele'] = experiment_info_file.pop('allele')
            experiment_info['genotype'] = experiment_info_file.pop('genotype')
            
            experiment_info['sex'] = experiment_info_file.pop('sex')
            experiment_info['stage'] = experiment_info_file.pop('developmental_stage')
            
            if experiment_info['stage'] == "young adult":
                experiment_info['stage'] = 'adult'
            
            experiment_info['ventral_side'] = experiment_info_file.pop('ventral_side')
            
            dd = fid.get_node('/provenance_tracking/FEAT_CREATE').read()
            commit_hash = json.loads(dd.decode('utf-8'))['commit_hash']
            experiment_info['software'] = {'name': 'MWTracker', 'commit_hash':commit_hash}
            
            experiment_info.update(experiment_info_file)
        
        
        
        
        return experiment_info

def _reformatForJson(A):
    A = np.where(np.isnan(A), None, A)
    
    #wcon specification require to return a single number if it is only one element list
    if A.size == 1:
        return A[0]
    else:
        return A.tolist()

def indWormsFeats2Dict(features_file):
    with pd.HDFStore(features_file, 'r') as fid:
        features_timeseries = fid['/features_timeseries']
        feat_time_group_by_worm = features_timeseries.groupby('worm_index');
        
        
    with tables.File(features_file, 'r') as fid:
        #fps used to adjust timestamp to real time
        fps = fid.get_node('/features_timeseries').attrs['fps']
        
        
        #get pointers to some useful data
        skeletons = fid.get_node('/skeletons')
        
        #let's append the data of each individual worm as a element in a list
        all_worms_feats = []
        
        #group by iterator will return sorted worm indexes
        for worm_id, worm_feat_time in feat_time_group_by_worm:
            worm_id = int(worm_id)
            
            #read worm skeletons data
            worm_skel = skeletons[worm_feat_time.index]
            
            #start ordered dictionary with the basic features
            worm_basic = OrderedDict()
            worm_basic['id'] = worm_id
            worm_basic['t'] = _reformatForJson(worm_feat_time['timestamp']/fps)
            worm_basic['x'] = _reformatForJson(worm_skel[:, :, 0])
            worm_basic['y'] = _reformatForJson(worm_skel[:, :, 1])
            
            worm_features = OrderedDict()
            #add time series features
            for col_name, col_dat in worm_feat_time.iteritems():
                if not col_name in ['worm_index', 'timestamp']:
                    worm_features[col_name] = _reformatForJson(col_dat)
            
            worm_path = '/features_events/worm_%i' % worm_id
            worm_node = fid.get_node(worm_path)
            #add event features
            for feature_name in worm_node._v_children:
                feature_path = worm_path + '/' + feature_name
                worm_features[feature_name] = _reformatForJson(fid.get_node(feature_path)[:])
            
            worm_basic['@OMG'] = worm_features
            
            #append features
            all_worms_feats.append(worm_basic)
    
    return all_worms_feats

def getUnits(features_file):
    
    with tables.File(features_file, 'r') as fid:
        micronsPerPixel = fid.get_node('/features_timeseries').attrs['micronsPerPixel']
    
    units = OrderedDict()
    units['t'] = 'seconds'
    if isinstance(micronsPerPixel, (float, np.float64)) and micronsPerPixel == 1:
        units['x'] = 'pixels'
        units['y'] = 'pixels'
    else:
        units['x'] = 'microns'
        units['y'] = 'microns'
    
    ws = WormStatsClass()
    units.update(ws.features_info['units'].to_dict())
    
    return units
    
    
def exportWCON(features_file, JSON_path):
    metadata = getMetaData(features_file)
    data = indWormsFeats2Dict(features_file)
    units = getUnits(features_file)
    
    units = {x:units[x].replace('degrees', '1') for x in units}
    units = {x:units[x].replace('radians', '1') for x in units}
    
    
    as_ordered_dict = OrderedDict()
    
    as_ordered_dict['metadata'] = metadata
    as_ordered_dict['units'] = units
    as_ordered_dict['data'] = data
    
    pretty_print = True
    with open(JSON_path, 'w') as fid:
        json.dump(as_ordered_dict, fid, allow_nan=False,
                      indent=4 if pretty_print else None)

if __name__ == '__main__':
    #features_file = '/Users/ajaver/Desktop/Videos/Avelino_17112015/Results/CSTCTest_Ch1_18112015_075624_features.hdf5'
    features_file = '/Users/ajaver/Desktop/Videos/single_worm/global_sample_v2/300 LSJ1 on food L_2011_03_10__10_52_16___6___1_features.hdf5'
    #features_file = '/Users/ajaver/Desktop/Videos/single_worm/large_sample/N2 on food R_2011_03_24__16_38_20___6___5_features.hdf5'
    
    JSON_path = 'test.json'
    
    exportWCON(features_file, JSON_path)
    #%%
    import wcon
    wc = wcon.WCONWorms()
    wc = wc.load_from_file(JSON_path, validate_against_schema = False)
