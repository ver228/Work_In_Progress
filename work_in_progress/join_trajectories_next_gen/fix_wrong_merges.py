#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 13:47:05 2017

@author: ajaver
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 17:46:36 2016

@author: ajaver
"""
import pandas as pd
import tables
import numpy as np
from collections import OrderedDict
import cv2

from tierpsy.analysis.ske_create.getSkeletonsTables import getWormMask
from tierpsy.analysis.ske_create.helperIterROI import getWormROI

class ImageRigBuff:
    #ring buffer class to avoid having to read the same image several times
    def __init__(self, mask_group, buf_size):
        
        self.buf_size = buf_size
        
        self.ind = 0
        self.current_time = 0
        self.win_size = buf_size//2
        self.last_frame = mask_group.shape[0]
        self.mask_group = mask_group
        
        #start the buffer
        self.I_buff = mask_group[:buf_size]
        
    def get_buffer(self, next_frame):
        bot = max(next_frame-self.win_size, self.current_time+self.win_size+1)        
        top = min(self.last_frame, next_frame + self.win_size)
        self.current_time = next_frame
        self.ind_center =  self.current_time - bot
        
        
        Idum = self.mask_group[bot:top+1]
        
        #print('A', bot, top, Idum.shape)
                
        for ii in range(Idum.shape[0]):
            self.I_buff[self.ind] = Idum[ii]
            self.ind += 1
            if self.ind >= self.buf_size:
                self.ind = 0
        
        return self.I_buff
    
    def get_buff_reduced(self, next_frame):
        img = self.get_buffer(next_frame).copy()
        img_c = img[self.ind_center]
        
        img[img==0] = 255
        img_r = np.min(img, axis=0)
        img_r[img_r==255] = 0
        
        return img_c, img_r
    

def get_traj_limits(trajectories_data, 
                    worm_index_type='worm_index_joined', 
                    win_area = 10):
    traj_limits = OrderedDict()
    
    assert worm_index_type in trajectories_data
    grouped_trajectories = trajectories_data.groupby(worm_index_type)
    
    tot_worms = len(grouped_trajectories)
    
        
    
    traj_limits = np.recarray(tot_worms, [('worm_index',np.int), ('t0',np.int), ('tf',np.int), \
    ('x0',np.float), ('xf',np.float), ('y0',np.float), ('yf',np.float), \
    ('a0',np.float), ('af',np.float),  ('th0',np.float), ('thf',np.float), \
    ('roi_size',np.int)])
    
    fields_needed = ['coord_x', 'coord_y', 'roi_size', 'frame_number', 'threshold']
    for index_n, (worm_index, trajectories_worm) in enumerate(grouped_trajectories):
        good = trajectories_worm['area'] != 0
        dd = trajectories_worm.loc[good, 'frame_number']
        row0 = dd.argmin();
        rowf = dd.argmax();
        
        worm_areas = trajectories_worm['area'].values;
        
        a0 = np.median(worm_areas[:win_area])
        
        af = np.median(worm_areas[-win_area:])
        
        dd = trajectories_worm.loc[[row0, rowf], fields_needed]
        
        t0, tf = dd['frame_number'].values
                
        roi_size = dd['roi_size'].values[0]

        x0, xf = dd['coord_x'].values
        y0, yf = dd['coord_y'].values
        
        th0, th1 = dd['threshold'].values     
        
        traj_limits[index_n] = (worm_index, t0, tf, x0,xf, y0,yf, a0, af, th0, th1, roi_size)
        #if worm_index == 50: break;
    traj_limits = pd.DataFrame(traj_limits, index=traj_limits['worm_index'])
    return traj_limits 


def get_break_points(trajectories_data, min_area_limit=0.5, worm_index_type='worm_index_joined'):
    trajgrouped = trajectories_data.groupby('frame_number')    
    traj_limits = get_traj_limits(trajectories_data, worm_index_type=worm_index_type) 
    
    
    break_points = []
    #check if the trajectories end or the begining intersect the middle of other trajectories    
    #for ind_check, row2check in traj_limits.loc[436:437].iterrows():
    for ind_check, row2check in traj_limits.iterrows():
        
        R_search = row2check['roi_size']**2
        
        #we only check one frame before the begining of the traj 
        #and one frame after the end.
        t_prev = row2check['t0']-1 
        t_next = row2check['tf']+1
        
        try:      
            
            dat_prev = trajgrouped.get_group(t_prev);
            
            #only cosider points that are in the middle of another trajectory (do not use start or ending points)
            possible_ind = dat_prev[worm_index_type].values                
            traj_tt = traj_limits.loc[possible_ind,  'tf']
                            
            dat_prev = dat_prev[(traj_tt != t_prev).values]# & (traj_tt['tf'] != t_next)).values]
            
            delX = row2check['x0'] - dat_prev['coord_x']
            delY = row2check['y0'] - dat_prev['coord_y']
            R = delX*delX + delY*delY
            dat_prev = dat_prev[R <= R_search]
            for _, rr in dat_prev.iterrows():
                assert t_prev == rr['frame_number'] == row2check['t0']-1
                            
                ind_split = int(rr[worm_index_type])
                dat_split = (rr['coord_x'], rr['coord_y'], rr['roi_size'], rr['threshold'], min_area_limit)#rr['area']/2)
                dat_check = (row2check['x0'], row2check['y0'], row2check['roi_size'], row2check['th0'], min_area_limit)#row2check['a0']/2)
                break_points.append(((int(ind_split), int(t_prev), dat_split), \
                                    (int(ind_check), int(row2check['t0']), dat_check)))      
        except KeyError:
             pass
        
        try:    
            
            dat_next = trajgrouped.get_group(t_next);
            
            #only cosider points that are in the middle of another trajectory (do not use start or ending points)
            possible_ind = dat_next[worm_index_type].values                
            traj_tt = traj_limits.loc[possible_ind,  't0']
            dat_next = dat_next[(traj_tt != t_next).values]# & (traj_tt['tf'] != t_next)).values]
            
            delX = row2check['xf'] - dat_next['coord_x']
            delY = row2check['yf'] - dat_next['coord_y']
            R = delX*delX + delY*delY
            dat_next = dat_next[R <= R_search]
            
            for _, rr in dat_next.iterrows():
                assert t_next == rr['frame_number'] == row2check['tf']+1
                            
                ind_split = int(rr[worm_index_type])
                dat_split = (rr['coord_x'], rr['coord_y'], rr['roi_size'], rr['threshold'], min_area_limit)#rr['area']/2)
                dat_check = (row2check['xf'], row2check['yf'], row2check['roi_size'], row2check['thf'], min_area_limit)#row2check['af']/2)
                break_points.append(((int(ind_split), int(t_next), dat_split), \
                                    (int(ind_check), int(row2check['tf']), dat_check)))            
        except KeyError:
             pass

    
    return break_points



def get_border_cnt(img_r, img_c, roi_dat, border_range=2):

    im_size = img_r.shape
    def _is_border(cnt):
        IM_LIMX = im_size[0] - border_range - 1
        IM_LIMY = im_size[1] - border_range - 1 
        if len(cnt)== 0:
            return False
        else:
            return np.any(cnt <= border_range) | \
            np.any(cnt[:, 0] >=  IM_LIMY) | \
            np.any(cnt[:, 1] >= IM_LIMX)

    
    def _get_roi_cnts(img, x, y, roi_size, thresh, max_area):
        worm_img, roi_corner = getWormROI(img, x, y, roi_size)
        worm_mask, worm_cnt, _ = getWormMask(worm_img, 
                                             thresh, 
                                             min_blob_area=max_area,
                                             strel_size=5)
        if worm_cnt.size > 0:
            worm_cnt += roi_corner   
        return worm_cnt 
      
    worm_cnt_c = _get_roi_cnts(img_c, *roi_dat)
    if _is_border(worm_cnt_c):
        worm_cnt = worm_cnt_c
    else:
        worm_cnt = _get_roi_cnts(img_r, *roi_dat)
    
    return worm_cnt  



def get_area_overlaps(mask_video, break_points, buf_size = 11):
    #%%
    indexInFrame = {} 
    roi_data = {}
    for dd in break_points:
        for ind, t, dat in dd:
            if not t in indexInFrame:
                indexInFrame[t] = []
            indexInFrame[t].append(ind)
            roi_data[ind,t] = dat

    
    worm_cnt = OrderedDict() 
    with tables.File(mask_video, 'r') as fid:
        mask_group = fid.get_node('/mask')
        ir = ImageRigBuff(mask_group, buf_size=buf_size)
        
        for t in sorted(indexInFrame):
            
            img_c, img_r = ir.get_buff_reduced(t)

            for ind in indexInFrame[t]:
                worm_cnt[ind, t] = get_border_cnt(img_r, img_c, roi_data[ind, t])
                
                #if ind == 34:
                #    plt.figure()
                #    plt.imshow(img, cmap='gray')
    #%%
    area_overlap = {}
    #kernel = np.ones((3,3), np.int32)
    for (ind_split, t_split, dat_split), (ind_check, t_check, dat_check) in break_points:
        key_tuple = (ind_split, t_split, ind_check, t_check)
        cnt_split = worm_cnt[ind_split, t_split]
        cnt_check = worm_cnt[ind_check, t_check]
        
        if len(cnt_check) == 0: 
            area_overlap[key_tuple] = -2 #'bad_check'
        elif len(cnt_split) == 0: 
            area_overlap[key_tuple] = -1 #'bad_split'
        elif not key_tuple in area_overlap:
            bot = np.minimum(np.amin(cnt_split,0), np.amin(cnt_check, 0))
            top = np.maximum(np.amax(cnt_split,0), np.amax(cnt_check, 0))
            
            roi_size = top - bot + (1,1)
            roi_size = roi_size[::-1]
            
            mask_split = np.zeros(roi_size, np.int32)
            cnt_split = [(cnt_split-bot).astype(np.int32)];
            cv2.drawContours(mask_split, cnt_split, 0, 1, -1)
            
            mask_check = np.zeros(roi_size, np.int32)
            cnt_check = [(cnt_check-bot).astype(np.int32)];
            cv2.drawContours(mask_check, cnt_check, 0, 1, -1)
            
            area_intersect = np.sum(mask_check & mask_split)
            area_check = np.sum(mask_check)
            
            
            #try:
            #    if ind_split == 34 or ind_check == 34:
            #        plt.figure()
            #        plt.plot(cnt_split[0][:, 0], cnt_split[0][:, 1])
            #        plt.plot(cnt_check[0][:, 0], cnt_check[0][:, 1])
            #        plt.title((ind_split, t_split, ind_check, t_check))
            #except:
            #    import pdb
            #    pdb.set_trace()
            
            
            area_overlap[key_tuple] = area_intersect/area_check
            #%%
    return area_overlap

def get_points2split(trajectories_data, 
                     mask_video, 
                     worm_index_type='worm_index_joined',
                     min_area_ratio=0.5,
                     buf_size = 11):
    
    
    #%%
    break_points = get_break_points(trajectories_data, worm_index_type=worm_index_type)
    area_overlap = get_area_overlaps(mask_video, break_points, buf_size=buf_size)
    
    points2split = {}
    for x in area_overlap:
        if area_overlap[x]>min_area_ratio:
            if not x[0] in points2split: 
                points2split[x[0]] = []
            t_split = max(x[1],x[3]);
            if not t_split in points2split[x[0]]:
                points2split[x[0]].append(t_split)
    #%%
    return points2split

def split_trajectories(mask_video, trajectories_data, worm_index_type='worm_index_joined'):
    #%%
    last_index = trajectories_data[worm_index_type].max()
    traj_grouped_ind = trajectories_data.groupby(worm_index_type)
    
    points2split = get_points2split(trajectories_data, 
                                    mask_video,
                                    worm_index_type)
    #%%
    worm_index_new = trajectories_data[worm_index_type].copy()
    for worm_ind in points2split:
        
        worm_dat = traj_grouped_ind.get_group(worm_ind)
        
        frames = worm_dat['frame_number']           
        last_index += 1
        new_index = pd.Series(last_index, index=frames.index)            
        for t_split in sorted(points2split[worm_ind]):
            last_index += 1
            new_index[frames>=t_split] += 1
            
        assert len(np.unique(new_index)) == len(points2split[worm_ind])+1
        assert np.all(trajectories_data.loc[new_index.index, worm_index_type] == worm_ind)
        
        worm_index_new[new_index.index] = new_index
    #%%
    return worm_index_new, points2split
#%% remove small sporious trajectories
def filter_table_by_area(trajectories_data, 
                         min_area_limit = 50, 
                         n_sigma = 6,
                         worm_index_type='worm_index_joined'):
    area_med = trajectories_data['area'].median()
    area_mad = (trajectories_data['area']-area_med).abs().median();
    
    min_area = max(min_area_limit, area_med-n_sigma*area_mad)
    
    median_area = trajectories_data.groupby(worm_index_type).agg({'area':'median'})
    is_small =  (median_area<min_area).values
    small_index = median_area[is_small].index.tolist()
    
    
    bad = trajectories_data[worm_index_type].isin(small_index)
    trajectories_data_f = trajectories_data[~bad]    
    return trajectories_data_f


def fix_wrong_merges(mask_video, skeletons_file, min_area_limit=50, worm_index_type='worm_index_joined'):
    #%%
    #get the trajectories table
    with pd.HDFStore(skeletons_file, 'r') as fid:
        trajectories_data = fid['/trajectories_data']
    trajectories_data_f = filter_table_by_area(trajectories_data, min_area_limit)
    worm_index_new, points2split = split_trajectories(mask_video, 
                                        trajectories_data_f, 
                                        worm_index_type)
    
    trajectories_data['worm_index_auto'] =  np.int32(-1) #like that it force the unassigned indexes to be empty
    trajectories_data.loc[worm_index_new.index, 'worm_index_auto'] = worm_index_new.values
    #%%
    return trajectories_data, points2split
        


if __name__ == '__main__':
    #import matplotlib.pylab as plt
    import glob
    import os
    
    from tierpsy.helper.misc import remove_ext, RESERVED_EXT
    #mask_dir = '/Volumes/behavgenom_archive$/Avelino/screening/CeNDR/MaskedVideos/CeNDR_Set1_310517/'
    #mask_dir = '/Volumes/behavgenom_archive$/Avelino/screening/CeNDR/MaskedVideos/CeNDR_Set1_160517/'
    #mask_dir = '/Volumes/behavgenom_archive$/Avelino/screening/CeNDR/MaskedVideos/CeNDR_Set1_020617/'
    #mask_dir = '/Volumes/behavgenom_archive$/Avelino/Worm_Rig_Tests/Test_Food/MaskedVideos/FoodDilution_041116'
    #mask_dir = '/Volumes/behavgenom_archive$/Avelino/screening/Development/MaskedVideos/Development_C1_170617/'
    #mask_dir = '/Volumes/behavgenom_archive$/Avelino/screening/Development/MaskedVideos/**/'
    mask_dir = '/Users/ajaver/OneDrive - Imperial College London/optogenetics/ATR_210417'
    #mask_dir = '/Users/ajaver/OneDrive - Imperial College London/optogenetics/Arantza/MaskedVideos/**/'
    
    fnames = glob.glob(os.path.join(mask_dir, '*.hdf5'))
    fnames = [x for x in fnames if not any(x.endswith(ext) for ext in RESERVED_EXT)]
    for mask_video in fnames[1:2]:
        base_name = os.path.basename(mask_video)
        print(base_name)
        skeletons_file = mask_video.replace('MaskedVideos','Results')
        skeletons_file = remove_ext(mask_video) + '_skeletons.hdf5'
        
        trajectories_data, splitted_points = \
        fix_wrong_merges(mask_video,
                         skeletons_file, 
                         min_area_limit=50,
                         worm_index_type='worm_index_joined')
        
        dd = trajectories_data.loc[trajectories_data['skeleton_id']!=trajectories_data.index, 'skeleton_id']
        if len(dd) > 0:
            print(base_name, dd.shape)
        break
        