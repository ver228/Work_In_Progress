# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 22:01:59 2016

@author: ajaver
"""
import os
import matplotlib.pylab as plt
import tables
import numpy as np
import pandas as pd
import shutil

from tierpsy.helper.params import read_fps
from tierpsy.analysis.stage_aligment.findStageMovement import getFrameDiffVar, findStageMovement, shift2video_ref

def test_var_diff(masked_file, skeletons_file):
    #%%
    with tables.File(skeletons_file, 'r') as fid:
        frame_diff_o = fid.get_node('/stage_movement/frame_diffs')[:]
        frame_diff_o = np.squeeze(frame_diff_o)
        video_timestamp_ind = fid.get_node('/timestamp/raw')[:]
    #%%
    
    frame_diffs_d = getFrameDiffVar(masked_file);
    #%%
    # The shift makes everything a bit more complicated. I have to remove the first frame, before resizing the array considering the dropping frames.
    if video_timestamp_ind.size > frame_diffs_d.size + 1:
        #%i can tolerate one frame (two with respect to the frame_diff)
        #%extra at the end of the timestamp
        video_timestamp_ind = video_timestamp_ind[:frame_diffs_d.size + 1];
    
    
    dd = video_timestamp_ind - np.min(video_timestamp_ind)-1; #shift data
    dd = dd[dd>=0];
    if frame_diffs_d.size != dd.size: 
        raise(ValueError('the number of frames and time stamps do not match, nothing to do here'))
        #%%
    frame_diffs = np.full(np.max(dd)+1, np.nan);
    frame_diffs[dd] = frame_diffs_d;
    
    #assert np.max(np.abs(frame_diff_o-frame_diffs)) < 1e-6
    #%%
    return frame_diffs, video_timestamp_ind
#%%
def test_aligment(masked_file, skeletons_file, is_calculate_diff=False):
    #%%
    fps = read_fps(skeletons_file)
    

    with tables.File(masked_file, 'r') as fid:
        xml_info = fid.get_node('/xml_info').read().decode()
    
    with pd.HDFStore(masked_file, 'r') as fid:
        stage_log = fid['/stage_log']
    
    #%%
    with tables.File(skeletons_file, 'r') as fid:
        is_stage_move_o = fid.get_node('/stage_movement/is_stage_move')[:]
        is_stage_move_o = np.squeeze(is_stage_move_o)
        stage_vec_o = fid.get_node('/stage_movement/stage_vec')[:]
        stage_vec_o = np.squeeze(stage_vec_o)
    #%%
    #%this is not the cleaneast but matlab does not have a xml parser from
    #%text string
    delay_str = xml_info.partition('<delay>')[-1].partition('</delay>')[0]
    delay_time = float(delay_str) / 1000;
    delay_frames = np.ceil(delay_time * fps);
    mediaTimes = stage_log['stage_time'].values;
    locations = stage_log[['stage_x', 'stage_y']].values;
    
    if is_calculate_diff:
        frame_diffs, video_timestamp_ind = test_var_diff(masked_file, skeletons_file)
    else:
        
        with tables.File(skeletons_file, 'r') as fid:
            video_timestamp_ind = fid.get_node('/timestamp/raw')[:].astype(np.int)
            frame_diffs_d = fid.get_node('/stage_movement/frame_diffs')[:]
            frame_diffs_d = np.squeeze(frame_diffs_d)
        
        
        # The shift makes everything a bit more complicated. I have to remove the first frame, before resizing the array considering the dropping frames.
        if video_timestamp_ind.size > frame_diffs_d.size + 1:
            video_timestamp_ind = video_timestamp_ind[:frame_diffs_d.size + 1];
        
        dd = video_timestamp_ind - np.min(video_timestamp_ind)-1; #shift data
        dd = dd[dd>=0];
        if frame_diffs_d.size != dd.size: 
            raise(ValueError('the number of frames and time stamps do not match, nothing to do here'))
        
        frame_diffs = np.full(np.max(dd)+1, np.nan);
        frame_diffs[dd] = frame_diffs_d;
    
    #%%
    
    is_stage_move, movesI, stage_locations = \
    findStageMovement(frame_diffs, mediaTimes, locations, delay_frames, fps);
    
    print(locations)
    stage_vec_d, is_stage_move_d = shift2video_ref(is_stage_move, movesI, stage_locations, video_timestamp_ind)
    print(stage_locations)
    
    #dd = np.diff(video_timestamp_ind)
    #print('T2:', np.where(dd!=1), np.unique(dd))
    #for x in movesI: print(x[0] + 1, x[1], x[1]-x[0]-1)
    
    
    return (is_stage_move_d, is_stage_move_o), (stage_vec_o, stage_vec_d)



#%%

import multiprocessing as mp
import pymysql
from contextlib import contextmanager
from functools import partial
import sys

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        
        old_stderr = sys.stderr
        sys.stderr = devnull
        
        try:  
            yield
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
                
def _process_row(row, save_dir):
    fpath = os.path.join(row['results_dir'], row['base_name'])
    
    masked_file = fpath + '.hdf5'
    skeletons_file = fpath + '_skeletons.hdf5'
    
    try:
        with suppress_stdout():
            (is_stage_move_d, is_stage_move_o), (stage_vec_o, stage_vec_d)  = \
            test_aligment(masked_file, skeletons_file, is_calculate_diff = False)   
    except:
        f_crashed = (masked_file, skeletons_file)
        
        return f_crashed, None
        #f_crashed.append((masked_file, skeletons_file))
        #continue
    
    
    #aligment_diff= is_stage_move_o-is_stage_move_d
    #if np.any(np.abs(aligment_diff)>0):
    stage_diff = np.abs(stage_vec_o - stage_vec_d)
    dd = stage_diff[~np.isnan(stage_diff)]==0
    if dd.size > 0 and not np.all(dd): 
        d1 = (masked_file, skeletons_file)
        d2 = (is_stage_move_d, is_stage_move_o, stage_vec_o, stage_vec_d)
        #f_missmatched.append((d1, d2))
        
        f_missmatched = (d1, d2)
        
    
        shutil.copy(skeletons_file, save_dir)
        shutil.copy(masked_file, save_dir)
        return None, f_missmatched
    else:
        return None, None

def main_sql():
    
    save_dir = '/Users/ajaver/OneDrive - Imperial College London/Local_Videos/miss_aligments'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    
    conn = pymysql.connect(host='localhost', database='single_worm_db')
    cur = conn.cursor(pymysql.cursors.DictCursor)
    
    sql = '''
    SELECT *
    FROM experiments_valid
    WHERE exit_flag='END'
    '''
    
    cur.execute(sql)
    f_data = cur.fetchall()
    
    
    
    
    f_crashed, f_missmatched = [], [] 
    
    n_batch = 50
    p = mp.Pool(n_batch)
    for nn in range(0, len(f_data), n_batch):
        DD = list(p.map(partial(_process_row, save_dir=save_dir), f_data[nn:nn+n_batch]))
        
        c,m = zip(*DD)
        f_crashed += [x for x in c if x is not None]
        f_missmatched += [x for x in m if x is not None]
        
        print(nn, len(f_data), len(f_crashed), len(f_missmatched))
    return f_crashed, f_missmatched 

if __name__ == '__main__':
    if False:
        DD = main_sql()
    
    else:
        ignore_f = ['798 JU258 on food L_2010_11_26__16_28_04__14']
        
        #%%
        import glob
        
        save_dir = '/Users/ajaver/OneDrive - Imperial College London/Local_Videos/miss_aligments'
        
        fnames = glob.glob(os.path.join(save_dir, '*_skeletons.hdf5'))
        
        fnames = [x for x in fnames if not any(bad_e in x for bad_e in ignore_f)]
        
        fnames = ['/Volumes/behavgenom_archive$/single_worm/unfinished/WT/PS312/food_mec-10,mec-4-L3/XX/30m_wait/clockwise/197 PS312 3 on mec-10,mec-4-L3 L_2011_07_06__15_33___3___1_skeletons.hdf5']
        #%%
        problem_l = []
        for ifile, skeletons_file in enumerate(fnames):
            masked_file = skeletons_file.replace('_skeletons.hdf5', '.hdf5')
            if not os.path.exists(masked_file):
                continue
            
            try:
                (is_stage_move_d, is_stage_move_o), (stage_vec_o, stage_vec_d)  = \
                test_aligment(masked_file, skeletons_file, is_calculate_diff = False)   
            except ValueError:
                problem_l.append(skeletons_file)
                continue
                
            aligment_diff= is_stage_move_o-is_stage_move_d
            stage_diff = np.abs(stage_vec_o - stage_vec_d)
            dd = stage_diff[~np.isnan(stage_diff)]==0
            if True:#dd.size > 0 and not np.all(dd): 
                #np.sum(aligment_diff!=0) > 3:
                print(np.where(aligment_diff))
                print(np.where(~np.isnan(stage_diff) & (stage_diff!=0)))
                
                plt.figure(figsize = (14, 7))
                plt.subplot(5,1,1)
                plt.plot(is_stage_move_o, 'x')
                plt.plot(is_stage_move_d, '.')
                
                plt.subplot(5,1,2)
                plt.plot(aligment_diff, 'x')
                
                plt.subplot(5,1,3)
                plt.plot(stage_vec_o[:,0], '-')
                plt.plot(stage_vec_d[:,0], '.')
                
                plt.subplot(5,1,4)
                plt.plot(stage_vec_o[:,1], '-')
                plt.plot(stage_vec_d[:,1], '.')
                
                
                plt.subplot(5,1,5)
                plt.plot(stage_diff, 'x')
                
                plt.suptitle(os.path.basename(masked_file))
                
                
                print(masked_file)
                