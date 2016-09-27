# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 17:17:43 2016

@author: ajaver
"""
import os
import glob
import numpy as np
import pandas as pd
import tables
import datetime

from sqlalchemy import create_engine
from MWTracker.featuresAnalysis.obtainFeaturesHelper import WormStatsClass


def get_path_df_pratheeban(file_list, main_dir):
        
    #get magnification map
    def _getmag(x):
        try:
            return float(x.partition('x')[-1].partition(' ')[0].partition(',')[0])
        except:
            return np.nan
    magMap = pd.read_csv('experiments_zoom_pratheeban.csv', index_col=0)
    magMap = magMap.applymap(_getmag)
    magMap.index = [pd.to_datetime(x, format='%d-%b-%y').date() for x in magMap.index]
    
    #dictionary that maps magnification into microns/pixel
    PIXELS_PER_MICRON = {1:0.178, 1.25:0.224, 1.6:0.289, 2:0.363, 2.5:0.455}
        
    #split function that will map the info in each file into each rows in the experiments table
    def _split_fname_fun(fname):
        develop, date_str, base_name = fname.replace(main_dir, '').split(os.path.sep)
        
        base_name = base_name.rpartition('_feat')[0]
        
        timestamp_str = base_name.partition('_Ch1_')[-1]
        
        if timestamp_str:
            timestamp = pd.to_datetime(timestamp_str, format='%d%m%Y_%H%M%S')
            time_d = timestamp.time()
        else:
            timestamp = pd.to_datetime('20' + date_str, format='%Y_%m_%d')
            time_d = np.nan
        
        date_d = timestamp.date()
        
        is_manual = '_feat_manual.hdf5' in base_name
        
        
        magnification = magMap.loc[date_d, develop]        
        microns_per_pixel = 1/PIXELS_PER_MICRON[magnification]
        return base_name, date_d, time_d, develop, magnification, microns_per_pixel, is_manual,
    
    colnames = ['base_name', 'date', 'datetime', 'developmental_stage', 
    'magnification', 'microns_per_pixel', 'is_manual']
    
    DD_tup = zip(*map(_split_fname_fun, file_list))
    DD = pd.DataFrame({col:dat for col, dat in zip(colnames, DD_tup)})
    return DD
    
    
def convertUnits(df, micronsPerPixel):
    
    def _removeExtra(x):
        for bad_str in ['_pos', '_neg', '_abs', '_paused', '_foward', '_backward']:
            x = x.replace(bad_str, '')
        return x
    
    dict_units = WormStatsClass().features_info['units'].to_dict()
    
    def _getFactor(x):
        try:
            units = dict_units[_removeExtra(x)]
        except KeyError:
            units = '1'
        if units in ['microns', 'microns/seconds']:
            return micronsPerPixel
        elif units == 'microns^2':
            return micronsPerPixel**2
        elif units == 'radians/microns':
            return 1/micronsPerPixel
        else:
            return 1
    
    for feat in df:
        df[feat] *= _getFactor(feat)
    
    return df
    
class ReadFeaturesHDF5(object):
    def __init__(self):
        self.ws = WormStatsClass()
    
    def get(self, features_file, feat2read = []):
        if not feat2read:
            feat2read = self.ws.feat_timeseries
        feat2read = ['worm_index', 'timestamp'] + feat2read
        with pd.HDFStore(features_file, 'r') as fid:
            features_timeseries = fid['/features_timeseries']
            features_timeseries = features_timeseries[feat2read]

        return features_timeseries
    
    def get_means(self, features_file):
        with pd.HDFStore(features_file, 'r') as fid:
            features_means = fid['/features_means']
        return features_means


#
#plate_mean_features
if __name__ == '__main__':
    main_dir = '/Users/ajaver/Desktop/Videos/pratheeban/Results/'
    
    #feat_list = glob.glob(os.path.join(main_dir, '*/*/*_features.hdf5'))
    #feat_list_manual = glob.glob(os.path.join(main_dir, '*/*/*_feat_manual.hdf5'))
    all_feat_list = glob.glob(os.path.join(main_dir, '*/*/*_feat*.hdf5'))
    
    
    experiments = get_path_df_pratheeban(all_feat_list, main_dir)
    
#    #bad_first_date = datetime.date(2016,4,28)
#    #bad_last_date = datetime.date(2016,6,22)
#    #bad_experiments = (experiments['date'] >= bad_first_date) & \ 
#    #                    (experiments['date']<= bad_last_date)
#    #experiments = experiments[~bad_experiments]
#    
#    #experiments.to_csv('pratheeban_experiments.csv', 
#    #          na_rep='NULL', 
#    #          index=False)
#    
#    disk_engine = create_engine('sqlite:///pratheeban_features.db')
#    experiments.to_sql('experiments', 
#                       disk_engine, 
#                       if_exists='replace', 
#                       index_label = 'plate_id')
#    
#    feat_reader = ReadFeaturesHDF5()
#    for plate_id, plate_row in experiments.iterrows():
#        plate_mean_features = feat_reader.get_means(plate_row['full_name'])
#        plate_mean_features = convertUnits(plate_mean_features, plate_row['microns_per_pixel'])
#        plate_mean_features['plate_id'] = plate_id
#        
#        exists_type = 'replace' if plate_id == 0 else 'append'
#        plate_mean_features.to_sql('features_means', 
#                              disk_engine,
#                              if_exists=exists_type,
#                              index = False)
#        
#        print(plate_row['base_name'])



    
    
    
	


