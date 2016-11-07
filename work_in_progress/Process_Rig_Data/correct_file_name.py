# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 16:15:39 2016

@author: worm_rig
"""

import os
import glob
import numpy as np
import pandas as pd
from functools import partial

GECKO_DT_FMT = '%d%m%Y_%H%M%S'

def rig_focus_to_microns_per_pixel(focus):
    ''' convert rig focus to micros per pixel'''
    return -0.1937*(focus)+13.4377

def read_rig_csv_db(csv_file):
    db = pd.read_csv(csv_file)
    db['microns_per_pixel']= db['Focus'].apply(rig_focus_to_microns_per_pixel)

    db_ind = {(row['Set_N'],row['Rig_Pos'],row['Camera_N']) : irow 
             for irow, row in db.iterrows()}

    assert db.shape[0] == len(db_ind) #there must be only one combination set_n, pos_n, ch_n
    return db, db_ind

def read_rig_log_file(log_file):
    
    def _log_parts(x):
        dd = x.rpartition(':')
        video_timestamp = pd.to_datetime(dd[0].strip(), format='%d/%m/%Y %H:%M:%S')
        plate_n = int(dd[-1].partition('Plate')[-1].strip())
        return video_timestamp, plate_n
    
    with open(log_file, 'r') as fid:
        lines = fid.read().split('\n')
    move_times = [_log_parts(x) for x in lines if 'Moving to Plate' in x]
    move_times = pd.DataFrame(move_times, columns=['time', 'stage_pos'])
    return move_times

def get_rig_pos(movie_time, rig_move_times, max_delta = pd.to_timedelta('5min')):
    '''get rig position by matching movie time with the stage log'''
    dt = movie_time - rig_move_times['time']
    dt = dt[dt >= np.timedelta64(0)]
    
    if dt.min() < max_delta:
        stage_pos = rig_move_times.loc[dt.argmin(), 'stage_pos']
    else:
        stage_pos = np.nan
        
    return stage_pos
    
def gecko_fnames_to_table(filenames):
    def _gecko_movie_parts(x):
        '''
        Read movie parts as expected from a Gecko file.
        '''
        dir_name, bb = os.path.split(x)
        base_name, ext = os.path.splitext(bb)
        
        parts = base_name.split('_')
        
        try:
            video_timestamp = pd.to_datetime(parts[-2] + '_' + parts[-1], 
                                   format=GECKO_DT_FMT)
            parts = parts[:-2]
        
        except ValueError:
            video_timestamp = pd.NaT
            
     
        def _part_n(start_str, parts_d):
            if parts[-1].startswith(start_str):
                part_n = int(parts_d[-1].replace(start_str, ''))
                parts_d = parts_d[:-1]
            else:
                part_n = -1
            return part_n, parts_d
        
            
        channel, parts = _part_n('Ch', parts)
        stage_pos, parts = _part_n('Pos', parts)
        set_n, parts = _part_n('Set', parts)
        
        prefix = '_'.join(parts)
        
        return dir_name, base_name, ext, prefix, channel, stage_pos, set_n, video_timestamp
        
    fparts = [_gecko_movie_parts(x) for x in filenames]
    fparts_tab = pd.DataFrame(fparts, columns = ('directory', 'base_name', 'ext', 'prefix', 'channel', 'stage_pos', 'set_n', 'video_timestamp'))
    return fparts_tab

    
def get_movie_dirs(movies_dir_D, exp_name):
    movie_dirs = []
    for ii in range(3):
        n_pc = str(ii+1)
        dd = os.path.join(movies_dir_D, 'PC' + n_pc, exp_name + '_' + n_pc)
        movie_dirs.append(dd)
    
    assert all(os.path.exists(x) for x in movie_dirs)
    return movie_dirs
    
def read_extra_data(output_root_d, original_root_d):
    def _move_if_needed(fname, old_location):
        if not os.path.exists(fname):
            fname_original = os.path.join(old_location, os.path.basename(fname))
            assert os.path.exists(fname_original)
            os.rename(fname_original, fname)
    
    #get aux files location
    extra_dir = os.path.join(output_root_d, 'ExtraFiles')
    if not os.path.exists(extra_dir):
        os.mkdirs(extra_dir)
    
    
    log_file = os.path.join(extra_dir, exp_name + '.log')
    csv_file = os.path.join(extra_dir, exp_name + '.csv')
    
    
    #move to the new location if needed
    _move_if_needed(log_file, original_root_d)
    _move_if_needed(csv_file, original_root_d)
    
    #read aux files
    rig_move_times = read_rig_log_file(log_file)
    db, db_ind = read_rig_csv_db(csv_file)
    
    return rig_move_times, db, db_ind
    
#%%
def get_new_names(movie_dir, pc_n, f_ext, db, db_ind, rig_move_times, output_dir, new_prefix_fun):
    fnames = glob.glob(os.path.join(movie_dir, '**', f_ext), recursive=True)
    
    fparts_table = gecko_fnames_to_table(fnames)
    #correct the channel using the pc number
    fparts_table['channel']  += pc_n*2
    #get rig pos from log time
    fparts_table['stage_pos'] = fparts_table['video_timestamp'].apply(partial(get_rig_pos, rig_move_times=rig_move_times))
    
    
    dir_files_to_rename = []
    for old_fname, (irow, row) in zip(fnames, fparts_table.iterrows()):
        try:
            #match movie using set_n, pos_n, ch_n
            db_row = db.loc[db_ind[(row['set_n'], row['stage_pos'], row['channel'])]]
        except KeyError:
            #not match in the csv database
            print('FILE NOT LOCATED IN THE DATABASE: ' +  old_fname)
            continue
            
        new_prefix = new_prefix_fun(db_row)

        new_base = '{}_Set{}_Pos{}_Ch{}_{}{}'.format(new_prefix,
                                               row['set_n'], 
                                               row['stage_pos'], 
                                               row['channel'],
                                               row['video_timestamp'].strftime(GECKO_DT_FMT),
                                               row['ext'])

        new_fname = os.path.join(output_dir, new_base)
        #print(os.path.split(old_fname), os.path.split(new_fname))
        dir_files_to_rename.append((old_fname, new_fname))
    return dir_files_to_rename
    
def get_new_names_pc(original_root, exp_name, output_root, f_ext, new_prefix_fun):
    output_dir = os.path.join(output_root, 'RawVideos',  exp_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    #get data from the extra files
    rig_move_times, db, db_ind = read_extra_data(output_root, original_root)
        
    #create output directory where the files are going to be moved
    
        
    #get de directories for a particular experiment
    movie_dirs = get_movie_dirs(original_root, exp_name)    
    
    #explore each directory and get the expected new name
    get_new_d = partial(get_new_names, 
                        f_ext = f_ext, 
                        db = db, 
                        db_ind = db_ind, 
                        rig_move_times = rig_move_times, 
                        output_dir = output_dir, 
                        new_prefix_fun = new_prefix_fun)
    
    files_to_rename = [get_new_d(movie_dir, pc_n) for pc_n, movie_dir in enumerate(movie_dirs)]
    #flatten list
    files_to_rename = sum(files_to_rename, [])

    return files_to_rename
            

def rename_after_bad_choice(output_root, exp_name, f_ext, new_prefix_fun):
    
    raw_dir = os.path.join(output_root, 'RawVideos',  exp_name)
    results_dir = os.path.join(output_root, 'MaskedVideos',  exp_name)
    mask_dir = os.path.join(output_root, 'Results',  exp_name)
    
    if 'mjpg' in f_ext:
        output_dir = raw_dir
        r_fnames = glob.glob(os.path.join(results_dir, '**', '*.hdf5'), recursive=True)
        m_fnames = glob.glob(os.path.join(mask_dir, '**', '*.hdf5'), recursive=True)
        fnames = r_fnames + m_fnames
    elif 'hdf5' in f_ext:
        output_dir = mask_dir
        fnames = glob.glob(os.path.join(results_dir, '**', '*.hdf5'), recursive=True)
    else:
        raise ValueError('f_ext must be mjpg or hdf5')
    
    
    
    assert os.path.exists(output_dir)
    
    rig_move_times, db, db_ind = read_extra_data(output_root, '')
    
    files2rename = get_new_names(output_dir, 0, f_ext, db, db_ind, rig_move_times, output_dir, new_prefix_fun)
    getbn = lambda x : os.path.splitext(os.path.basename(x))[0]
    old2new = {getbn(x):getbn(y) for x,y in files2rename}
    
    
    dd = [[(x,x.replace(key, old2new[key])) for x in fnames if key in x] for key in old2new]
    dd = sum(dd,[]) #flatten
    
    assert len(dd) == len(fnames)
    files2rename += dd
    return files2rename
    

    
def _switch_pos_ch():
    output_root = "/Volumes/behavgenom_archive$/Avelino/Worm_Rig_Tests/Test_20161027"
    results_dir = os.path.join(output_root, 'MaskedVideos')
    mask_dir = os.path.join(output_root, 'Results')
    r_fnames = glob.glob(os.path.join(results_dir, '**', '*.hdf5'), recursive=True)
    m_fnames = glob.glob(os.path.join(mask_dir, '**', '*.hdf5'), recursive=True)
    fnames = r_fnames + m_fnames
    
    
    
    def correct_name(x):
        prefix, mid, rest = x.partition('_Ch')
        ch_n, mid, rest = rest.partition('_Pos')
        pos_n, mid, rest = rest.partition('_')
        assert ch_n and pos_n
        return '{}_Pos{}_Ch{}_{}'.format(prefix, pos_n, ch_n, rest)
    
    files_to_rename = [(x, correct_name(x)) for x in fnames]
    return files_to_rename

if __name__ == '__main__':
    f_ext = '*.mjpg'
    exp_name = 'FoodDilution_041116'
    
    raw_movies_root = "/Volumes/behavgenom_archive$/RigRawVideos"
    output_root = "/Volumes/behavgenom_archive$/Avelino/Worm_Rig_Tests/Test_Food"
    #output_root = "/Volumes/behavgenom_archive$/Avelino/Worm_Rig_Tests/Test_20161027"
    
    def TEST_FOOD_name_fun(db_row):
        return '{}_N{}_F1-{}'.format(db_row['Strain'], db_row['N_Worms'], db_row['Food_Conc'])
    
    new_prefix_fun = TEST_FOOD_name_fun
    
    #files_to_rename = rename_after_bad_choice(output_root, exp_name, '*.hdf5', new_prefix_fun)
    #[print([y for y in map(os.path.basename, x)]) for x in files_to_rename if x[0]!=x[1]]
    
    files_to_rename = get_new_names_pc(raw_movies_root, 
                                       exp_name, 
                                       output_root, 
                                       f_ext, 
                                       new_prefix_fun)
    #rename files
    for x in files_to_rename:
        os.rename(*x)

    #f_ext = '*.hdf5'
    dd = rename_after_bad_choice(output_root, exp_name, f_ext, new_prefix_fun)
    wrong_naming = [[y for y in map(os.path.basename, x)] for x in dd if x[0]!=x[1]]
    assert(len(wrong_naming) == 0)
    

    
    
    
    
    