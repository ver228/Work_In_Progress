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
    
    fps = read_fps(skeletons_file)
    

    with tables.File(masked_file, 'r') as fid:
        xml_info = fid.get_node('/xml_info').read().decode()
    
    with pd.HDFStore(masked_file, 'r') as fid:
        stage_log = fid['/stage_log']
    
    with tables.File(skeletons_file, 'r') as fid:
        is_stage_move_o = fid.get_node('/stage_movement/is_stage_move')[:]
        is_stage_move_o = np.squeeze(is_stage_move_o)
        stage_vec_o = fid.get_node('/stage_movement/stage_vec')[:]
        stage_vec_o = np.squeeze(stage_vec_o)
    
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
            frame_diffs = fid.get_node('/stage_movement/frame_diffs')[:]
            frame_diffs = np.squeeze(frame_diffs)
        
    
        # The shift makes everything a bit more complicated. I have to remove the first frame, before resizing the array considering the dropping frames.
        if video_timestamp_ind.size > frame_diffs.size + 1:
            video_timestamp_ind = video_timestamp_ind[:frame_diffs.size + 1];
    
    
    
    is_stage_move, movesI, stage_locations = \
    findStageMovement(frame_diffs, mediaTimes, locations, delay_frames, fps);
    
    stage_vec_d, is_stage_move_d = shift2video_ref(is_stage_move, movesI, stage_locations, video_timestamp_ind)

    return (is_stage_move_d, is_stage_move_o), (stage_vec_o, stage_vec_d)

def fix_timestamps(masked_file, skeletons_file):
    from tierpsy.analysis.compress.extractMetaData import read_and_save_timestamp
    from tierpsy.helper.misc import save_modified_table
    
    timestamp, timestamp_time = read_and_save_timestamp(masked_file, dst_file='')
    if os.path.exists(skeletons_file):
        read_and_save_timestamp(masked_file, dst_file=skeletons_file)
    
    with pd.HDFStore(skeletons_file, 'r') as fid:
        trajectories_data = fid['trajectories_data']
    
    ind = trajectories_data['frame_number'].values.astype(np.int)
    trajectories_data['timestamp_raw'] = timestamp[ind]
    trajectories_data['timestamp_time'] = timestamp_time[ind]
    
    save_modified_table(skeletons_file, trajectories_data, 'trajectories_data')

if __name__ == '__main__':
    import pymysql
    import os
    
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
    
    problematic = []
    
    for irow, row in enumerate(f_data[::-1]):
        print(irow, len(f_data))
        
        fpath = os.path.join(row['results_dir'], row['base_name'])
        
        masked_file = fpath + '.hdf5'
        skeletons_file = fpath + '_skeletons.hdf5'
        #%%
        
        #%%
        
        #masked_file = '/Users/ajaver/Documents/GitHub/tierpsy-tracker/tests/data/SCHAFER_LAB_SINGLE_WORM/MaskedVideos/L4_19C_1_R_2015_06_24__16_40_14__.hdf5'
        #skeletons_file = masked_file.replace('MaskedVideos', 'Results').replace('.hdf5', '_skeletons.hdf5')
        try:
            (is_stage_move_d, is_stage_move_o), (stage_vec_o, stage_vec_d)  = \
            test_aligment(masked_file, skeletons_file, is_calculate_diff = False)   
        except:
            print('BAD', row['base_name'])
            continue
    
        #%%
        aligment_diff= is_stage_move_o-is_stage_move_d
        
        if np.sum(np.abs(aligment_diff))> 3:
            problematic.append((masked_file, skeletons_file))
            print('WEIRD', row['base_name'])
        
            plt.figure()
            plt.subplot(2,1,1)
            plt.plot(is_stage_move_o, 'x')
            plt.plot(is_stage_move_d, '.')
            
            plt.subplot(2,1,2)
            plt.plot(aligment_diff, 'x')
            
            plt.title(row['base_name'])
            
            
            if len(problematic)<100:
                shutil.copy(skeletons_file, save_dir)
                shutil.copy(masked_file, save_dir)
        
        if irow > 2000:
            break
        
    #%%



