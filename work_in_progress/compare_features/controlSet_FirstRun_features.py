# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 17:17:43 2016

@author: ajaver
"""
import os
import glob
import pandas as pd
from sqlalchemy import create_engine
from MWTracker.featuresAnalysis.obtainFeaturesHelper import WormStatsClass


GECKO_DT_FMT = '%d%m%Y_%H%M%S'
def focus2microns_per_pixel(focus):
    return -0.1937*(focus)+13.4377

def _db_ind(db):
    return {(row['Set_N'],row['Rig_Pos'],row['Camera_N']) : irow 
             for irow, row in db.iterrows()}    

def _rowdict(full_name, csv_db_ind, csv_db):
    rest, fname = os.path.split(full_name);
    exp_dir = os.path.split(rest)[1]
    
    dd = fname.split('_')
    time_str = dd[-2]
    date_str = dd[-3]
    pos_n = int([x[3:] for x in dd if x.startswith('Pos')][0])
    ch_n = int([x[2:] for x in dd if x.startswith('Ch')][0])
    set_n = int([x[3:] for x in dd if x.startswith('Set')][0])
    
    irow = csv_db_ind[exp_dir][(set_n, pos_n, ch_n)]
    row = csv_db[exp_dir].loc[irow]
    rowdict = row.to_dict()
    rowdict['microns_per_pixel'] = focus2microns_per_pixel(rowdict['Focus'])
    rowdict['base_name'] = '_'.join(dd[:-1])
    rowdict['full_name'] = full_name
    rowdict['video_timestamp'] = pd.to_datetime(date_str + '_' + time_str, format=GECKO_DT_FMT)
    return rowdict

def get_path_df_control(csv_dir, main_dir):
    csv_files = glob.glob(os.path.join(csv_dir, '*.csv'))
    csv_db = {os.path.basename(x)[:-4] : pd.read_csv(x) for x in csv_files}
    
    
    csv_db_ind = {x:_db_ind(csv_db[x]) for x in csv_db}
    
    
    
    fnames = glob.glob(os.path.join(main_dir, '**/*_features.hdf5'), recursive=True)
    
    experiments = pd.DataFrame(_rowdict(x,csv_db_ind, csv_db) for x in fnames)
    return experiments


    
def convertUnits(df, microns_per_pixel):
    
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
            return microns_per_pixel
        elif units == 'microns^2':
            return microns_per_pixel**2
        elif units == 'radians/microns':
            return 1/microns_per_pixel
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
    
    def get_means(self, features_file, group_str = 'feat_means'):
        with pd.HDFStore(features_file, 'r') as fid:
            features_means = fid['/' + group_str]
        return features_means

def saveIntoDB(database_name, experiments):
    
    assert all(x in experiments for x in ['full_name', 'microns_per_pixel'])
    
    disk_engine = create_engine('sqlite:///' + database_name)
    experiments.to_sql('experiments', 
                       disk_engine, 
                       if_exists='replace', 
                       index_label = 'video_id')
    
    feat_reader = ReadFeaturesHDF5()
    for video_id, plate_row in experiments.iterrows():
        if not os.path.exists(plate_row['full_name']):
                continue
            
        for feat_str in ['features_means', 'features_means_split']:
            plate_mean_features = feat_reader.get_means(plate_row['full_name'], feat_str)
            plate_mean_features = convertUnits(plate_mean_features, plate_row['microns_per_pixel'])
            plate_mean_features['video_id'] = video_id
    
            exists_type = 'replace' if video_id == 0 else 'append'
            plate_mean_features.to_sql(feat_str, 
                                  disk_engine,
                                  if_exists=exists_type,
                                  index = False)
            
        print(plate_row['base_name'])
    
#plate_mean_features
if __name__ == '__main__':
    csv_dir = '/Volumes/behavgenom_archive$/Avelino/Worm_Rig_Tests/Test_20161027/Experiments_CSV'
    main_dir = '/Volumes/behavgenom_archive$/Avelino/Worm_Rig_Tests/Test_20161027/Results'
    
    database_dir = '/Users/ajaver/OneDrive - Imperial College London/compare_strains_DB'
    database_name = os.path.join(database_dir, 'control_experiments_firstRun.db')
    
    experiments = get_path_df_control(csv_dir, main_dir)
    saveIntoDB(database_name, experiments)
    

    
    