#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 15:01:54 2016

@author: ajaver
"""
from MWTracker.batchProcessing.CheckFilesForProcessing import CheckFilesForProcessing
from MWTracker.batchProcessing.helperFunc import getDefaultSequence, walkAndFindValidFiles


mask_dir_root = '/Volumes/behavgenom$/Pratheeban/MaskedVideos'
results_dir_root = '/Volumes/behavgenom$/Pratheeban/Results_reanalyzed'
tmp_dir_root = '~/Tmp'
json_file = ''
analysis_checkpoints = getDefaultSequence('Track', False)

walk_args = {'root_dir':mask_dir_root, 
                 'pattern_include' : '*.hdf5',
                  'pattern_exclude' : ''}

check_args = {'video_dir_root': mask_dir_root,
                  'mask_dir_root': mask_dir_root,
                  'results_dir_root' : results_dir_root,
                  'tmp_dir_root' : tmp_dir_root,
                  'json_file' : json_file,
                  'analysis_checkpoints': analysis_checkpoints,
                  'is_single_worm': False,
                  'no_skel_filter': True,
                  'is_copy_video': False}
                  
valid_files = walkAndFindValidFiles(**walk_args)
files_checker = CheckFilesForProcessing(**check_args)
cmd_list = files_checker.filterFiles(valid_files)

#%%
import h5py

dd = files_checker._printUnmetReq()
invalid_files = dd.replace('COMPRESS :', '').split()

for fname in invalid_files:
    with h5py.File(fname, 'r+') as fid:
        if not '/mask' in fid:
            print('bad: ', fname)
            continue
        elif len(fid['/mask'].attrs.keys()) == 0:
            assert '2015' in fname
            fid['/mask'].attrs['has_finished'] = 1
            print('problem: ', fname)
#%%
import os
import glob

results_dir_root = '/Volumes/behavgenom$/Pratheeban/Results/'
files = glob.glob(os.path.join(results_dir_root, '*', '15_*', '*_skeletons.hdf5'))

for fname in files:
    with h5py.File(fname, 'r+') as fid:
        fid['/skeleton'].attrs['has_finished']=1
