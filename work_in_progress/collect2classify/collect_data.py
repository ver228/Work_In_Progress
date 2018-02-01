#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 12:29:49 2018

@author: ajaver
"""
import glob
import os
import tables
import pandas as pd
import numpy as np
from tierpsy.analysis.ske_create.helperIterROI import getROIfromInd, pad_if_necessary

TABLE_FILTERS = tables.Filters(
    complevel=5,
    complib='zlib',
    shuffle=True,
    fletcher32=True)


if __name__ == '__main__':
    root_dir = '/Volumes/behavgenom_archive$/Lidia'
    
    maked_files_dir = os.path.join(root_dir, 'MaskedVideos')
    results_dir = os.path.join(root_dir, 'Results')
    
    #masked_files = glob.glob(os.path.join(maked_files_dir, '**', '*.hdf5',), recursive = True)
    skeletons_files = glob.glob(os.path.join(results_dir, '**', '*_skeletons.hdf5',), recursive = True)
    skeletons_files = sorted(skeletons_files)
    fnames = [(ii, ff) for ii,ff in enumerate(skeletons_files)]
    
    roi_size = 128
    
    save_name = os.path.join(root_dir, 'training_rois.hdf5')
    
    traj_data_dtypes = np.dtype([('experiment_id', np.int32),
                                  ('frame_number', np.int32),
                                  ('worm_index_joined', np.int32),
                                  ('coord_x', np.float32),
                                  ('coord_y', np.float32)
                                  ])
    valid_columns = list(traj_data_dtypes.names)
    
    with tables.File(save_name, 'w') as fid:
        fid.create_earray('/', 
                        'mask',
                        atom = tables.UInt8Atom(),
                        shape = (0, roi_size, roi_size),
                        expectedrows = len(fnames)*100,
                        filters = TABLE_FILTERS
                        )
        fid.create_table('/',
                        "trajectories_data",
                        traj_data_dtypes,
                        "Info from where the images in mask where taken.",
                        filters = TABLE_FILTERS)
    
    fid_tab = tables.File(save_name, 'r+')
    masks = fid_tab.get_node('/mask')
    traj_df = fid_tab.get_node('/trajectories_data')
    
    for experiment_id, skel_file in fnames:
        print(experiment_id, len(fnames))
        mask_file = skel_file.replace(results_dir, maked_files_dir).replace('_skeletons.hdf5', '.hdf5')
        
        with pd.HDFStore(skel_file, 'r') as fid:
            trajectories_data = fid['/trajectories_data']
        
        #reduce the table to only save the minimal information
        trajectories_data['experiment_id'] = np.float32(experiment_id)
        trajectories_data = trajectories_data[valid_columns]
        
        traj_df.append(trajectories_data.to_records(index=False))
        
        sample_data_l = []
        for w, dat in trajectories_data.groupby('worm_index_joined'):
            #I am only getting middle ROI in the trajectory
            ind_m = dat.index[len(dat)//2]
            row = dat.loc[ind_m]        
        
            frame_number = int(row['frame_number'])
            worm_index = int(row['worm_index_joined'])
            
            #slow but simple
            row, worm_roi, roi_corner = getROIfromInd(mask_file, trajectories_data, frame_number, worm_index, roi_size = roi_size)
            worm_roi, roi_corner = pad_if_necessary(worm_roi, roi_corner, roi_size)
            masks.append(worm_roi[None, ...])
            
            sample_data_l.append(row)
        
    sample_data = pd.concat(sample_data_l, axis=1).T
    
    id2fname = {ii:f for ii,f in fnames}
    sample_data['mask_file'] = sample_data['experiment_id'].map(id2fname)
    s_dtype = 'S{}'.format(sample_data['mask_file'].apply(len).max())
    
    r_dtype = []
    for col in sample_data:
        if col == 'mask_file':
            dt = s_dtype
        else:
            dt = sample_data[col].dtype
        r_dtype.append((col, dt))
    sample_data = sample_data.to_records(index=False).astype(r_dtype)
    
    fid_tab.create_table('/',
                    "sample_data",
                    sample_data,
                    filters = TABLE_FILTERS)
    
    
    fid_tab.close()