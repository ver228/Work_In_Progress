# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 16:15:39 2016

@author: worm_rig
"""

import os
import glob
import numpy as np
import pandas as pd


GECKO_DT_FMT = '%d%m%Y_%H%M%S'
def _log_parts(x):
    dd = x.rpartition(':')
    timestamp = pd.to_datetime(dd[0])
    plate_n = int(dd[-1].partition('Plate')[-1].strip())
    return timestamp, plate_n

def _movie_parts(x):
    dir_name, bb = os.path.split(x)
    base_name, ext_name = os.path.splitext(bb)
    rest, _, time_str = base_name.rpartition('_')
    rest, _, date_str = rest.rpartition('_')
    prefix, _, ch_str = rest.rpartition('_')
    
    timestamp = pd.to_datetime(date_str + '_' + time_str, 
                               format=GECKO_DT_FMT)
    ch_n = int(ch_str[2:])
    
    return dir_name, prefix, ext_name, timestamp, ch_n
    
def get_movie_dirs(movies_dir_D):
    dir_parts =  movies_dir_D.split(os.sep)
    movie_dirs = []
    for ii, drive in enumerate(['R:', 'S:', 'T:']):
        dd = [drive] + dir_parts[1:]
        dd[-2] = dd[-2][:-1] + str(ii+1)
        movie_dirs.append(os.sep.join(dd))
    
    assert all(os.path.exists(x) for x in movie_dirs)
    return movie_dirs

    
if __name__ == '__main__':
    f_ext = '*.mjpg'
    log_file = "R:\Videos\Move Three Pos_26-10-2016_21-08-53.log"
    movies_dir_D = r'R:\Videos\test_move_mjpg_1\Set_2'
    
    
    
    with open(log_file, 'r') as fid:
        lines = fid.read().split('\n')
        
    move_times = [_log_parts(x) for x in lines if 'Moving to Plate' in x]
    move_times = pd.DataFrame(move_times, columns=['time', 'stage_pos'])
    
    movie_dirs = get_movie_dirs(movies_dir_D)
    
    for ii, movie_dir in enumerate(movie_dirs):
        fnames = glob.glob(os.path.join(movie_dir, f_ext))
        fparts = [_movie_parts(x) for x in fnames]
        fparts = pd.DataFrame(fparts, columns = ('directory', 'prefix', 'ext', 'time', 'channel'))
        
        for old_fname, (irow, row) in zip(fnames, fparts.iterrows()):
            if row['prefix'][:-1].endswith('_Pos'):
                continue
            
            dt = row['time'] - move_times['time']
            dt = dt[dt >= np.timedelta64(0)]
            stage_pos = move_times.loc[dt.argmin(), 'stage_pos']
            
            new_base = '{}_Pos{}_Ch{}_{}{}'.format(row['prefix'], 
                                                   stage_pos, 
                                                   row['channel']  + ii*2,
                                                   row['time'].strftime(GECKO_DT_FMT),
                                                   row['ext'])
            new_fname = os.path.join(row['directory'], new_base)
            print(os.path.split(old_fname), os.path.split(new_fname))
            os.rename(old_fname, new_fname)


    