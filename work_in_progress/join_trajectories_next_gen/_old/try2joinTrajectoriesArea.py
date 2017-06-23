# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 17:46:36 2016

@author: ajaver
"""
import pandas as pd
import os
import tables
import numpy as np
import matplotlib.pylab as plt
from collections import OrderedDict

import networkx as nx

import cv2
from scipy.signal import savgol_filter
from scipy.signal import medfilt

import sys
sys.path.append('/Users/ajaver/Documents/GitHub/Multiworm_Tracking')

from tierpsy.analysis.ske_filt.getFilteredSkels import saveModifiedTrajData
from tierpsy.analysis.ske_create.getSkeletonsTables import getWormMask, binaryMask2Contour
from tierpsy.analysis.ske_create.helperIterROI import getWormROI
from tierpsy.helper.misc import WLAB

#%%
def getStartEndTraj(trajectories_data):
    traj_limits = OrderedDict()
    
    assert 'worm_index_auto' in trajectories_data
    grouped_trajectories = trajectories_data.groupby('worm_index_auto')
    
    tot_worms = len(grouped_trajectories)
    
    win_area = 10    
    
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
#%%
def getIndCnt(img, x, y, roi_size, thresh, max_area):
    worm_img, roi_corner = getWormROI(img, x, y, roi_size)
    worm_mask, worm_cnt, _ = getWormMask(worm_img, thresh)
    if worm_cnt.size > 0:
        worm_cnt += roi_corner   
    return worm_cnt                 
                 

def extractWormContours(masked_image_file, traj_limits):
    grouped_t0 = traj_limits.groupby('t0')
    grouped_tf = traj_limits.groupby('tf')
    
    uT0 = np.unique(traj_limits['t0'])
    uTf = np.unique(traj_limits['tf'])
    
    initial_cnt = OrderedDict()
    final_cnt = OrderedDict()
    
    with tables.File(masked_image_file, 'r') as fid:
        mask_group = fid.get_node('/mask')

        for frame_number in np.unique(np.concatenate((uT0,uTf))):
            img = mask_group[frame_number]
            
            
            if frame_number in uT0:
                dd = grouped_t0.get_group(frame_number)
                for ff, row in dd.iterrows():
                    worm_cnt = getIndCnt(img, row['x0'], row['y0'], 
                                         row['roi_size'], row['th0'], row['a0']/2)
                    initial_cnt[int(row['worm_index'])] = worm_cnt
            if frame_number in uTf:
                dd = grouped_tf.get_group(frame_number) 
                for ff, row in dd.iterrows():
                    worm_cnt = getIndCnt(img, row['xf'], row['yf'], 
                                         row['roi_size'], row['thf'], row['af']/2)
                    final_cnt[int(row['worm_index'])] = worm_cnt
                    
        return initial_cnt, final_cnt 
#%% 
def getPossibleConnections(traj_limits, max_gap = 25):
    connect_before = OrderedDict()
    connect_after = OrderedDict()
    
    for worm_index in traj_limits.index:
        curr_data = traj_limits.loc[worm_index]
        other_data = traj_limits[traj_limits.index != worm_index].copy()
        
        other_data['gap'] = curr_data['t0'] - other_data['tf']
        good = (other_data['gap']> 0) & (other_data['gap']<= max_gap)
        before_data = other_data[good].copy()
    
        other_data['gap'] = other_data['t0'] - curr_data['tf']
        good = (other_data['gap']> 0) & (other_data['gap']<= max_gap)
        after_data =  other_data[good].copy()
        
        Rlim = curr_data['roi_size']**2
        
        delXb = curr_data['x0'] - before_data['xf']
        delYb = curr_data['y0'] - before_data['yf']
        before_data['R2'] = delXb*delXb + delYb*delYb
        before_data = before_data[before_data['R2']<=Rlim]
        
        #before_data['AR'] =  curr_data['a0']/before_data['af']
        before_data = before_data[(curr_data['a0']!=0) & (before_data['af']!=0)]
        
        delXa = curr_data['xf'] - after_data['x0']
        delYa = curr_data['yf'] - after_data['y0']
        after_data['R2'] = delXa*delXa + delYa*delYa
        after_data = after_data[after_data['R2']<=Rlim]
        
        #after_data['AR'] =  curr_data['af']/after_data['a0']
        after_data = after_data[(curr_data['af']!=0) & (after_data['a0']!=0)]
        
        assert worm_index == curr_data['worm_index']
        if len(before_data) > 0:        
            connect_before[worm_index] = list(before_data.index.values)
        
        if len(after_data) > 0:        
            connect_after[worm_index] = list(after_data.index.values)
            
    return connect_before, connect_after



def getAreaIntersecRatio(connect_dict, node1_cnts, node2_cnts):    

    intersect_ratio = {}
    for current_ind in connect_dict:
        current_cnt = node1_cnts[current_ind]
        if current_cnt.size == 0:
            continue
        bot = np.min(current_cnt, axis=0);
        top = np.max(current_cnt, axis=0);
        
        for pii in connect_dict[current_ind]:
            if node2_cnts[pii].size == 0:
                continue
            bot_p = np.min(node2_cnts[pii],axis=0);
            top_p = np.max(node2_cnts[pii],axis=0);
            
            bot = np.min((bot, bot_p), axis=0)
            top = np.max((top, top_p), axis=0)
        
        roi_size = top-bot + (1,1)
        roi_size = roi_size[::-1]
    
        mask_curr = np.zeros(roi_size, np.int32)
        worm_cnt = [(current_cnt-bot).astype(np.int32)];
        cv2.drawContours(mask_curr, worm_cnt, 0, 1, -1)
        area_curr = np.sum(mask_curr)    
        
        for pii in connect_dict[current_ind]:
            if node2_cnts[pii].size == 0:
                continue
            mask_possible = np.zeros(roi_size, np.int32)
            worm_cnt = [(node2_cnts[pii]-bot).astype(np.int32)];
            cv2.drawContours(mask_possible, worm_cnt, 0, 1, -1)
            
            area_intersect = np.sum(mask_curr & mask_possible)
        
            intersect_ratio[(current_ind, pii)] = area_intersect/area_curr
        
    return intersect_ratio

def selectNearNodes(connect_dict, ratio_dict, time_table, min_intersect = 0.5):
    posible_nodes = []
    for node1 in connect_dict:
        node2_dat = []
        for node2 in connect_dict[node1]:
            if (node1, node2) in ratio_dict:
                node2_t0 = time_table[node2]
                ratio12 = ratio_dict[(node1, node2)]
                node2_dat.append((node2, node2_t0,ratio12))
        
        node2_dat = [x for x in node2_dat if x[2] > min_intersect]
        if len(node2_dat)==0: 
            continue

        node2_dat = min(node2_dat, key=lambda a:a[1])
        
        posible_nodes.append((node1, node2_dat[0]))
    return posible_nodes

def transitiveReduction(g):
    ''' from http://stackoverflow.com/questions/17078696/im-trying-to-perform-the-transitive-reduction-of-directed-graph-in-python'''
    for n1 in g.nodes_iter():
        if g.has_edge(n1, n1):
            g.remove_edge(n1, n1)
        for n2 in g.successors(n1):
            for n3 in g.successors(n2):
                for n4 in nx.dfs_preorder_nodes(g, n3):
                    if g.has_edge(n1, n4):
                        g.remove_edge(n1, n4) 

def cleanRedundantNodes(DG):
    transitiveReduction(DG)
    same_nodes = []
    for ind1 in DG.nodes():
        next_nodes = DG.successors(ind1)
        if len(next_nodes) == 1:
            pp = DG.predecessors(next_nodes[0]);
            if len(pp) == 1 and pp[0] == ind1:
                same_nodes.append((ind1, next_nodes[0]))
    
    G_redundant = nx.Graph()
    G_redundant.add_nodes_from(set([i for sub in same_nodes for i in sub]))
    G_redundant.add_edges_from(same_nodes)
    
    index2rename = {}
    for subgraph in nx.connected_component_subgraphs(G_redundant):
        nodes2remove = sorted(subgraph.nodes())
        edges2remove = subgraph.edges()
        first_node = nodes2remove[0]
        last_node = nodes2remove[-1]
        
        assert len(subgraph.neighbors(first_node)) == 1
        assert len(subgraph.neighbors(last_node)) == 1
        
        nodes2remove = nodes2remove[1:]        
        
        index2rename[first_node] = nodes2remove
        
        edges2add = []
        for ind2 in DG.successors(last_node):
                edges2add.append((first_node,ind2))
        
        DG.add_edges_from(edges2add)
        DG.remove_edges_from(edges2remove)
        DG.remove_nodes_from(nodes2remove)
    
    return DG, index2rename

def getTrajGraph(trajectories_data, masked_image_file, max_gap = 25, min_area_intersect = 0.5):
    print('Getting the trajectories starting and ending points.')
    traj_limits = getStartEndTraj(trajectories_data) 
    
    print('Getting possible connecting point.')
    connect_before, connect_after = getPossibleConnections(traj_limits, max_gap = max_gap)
    
    print('Extracting worm contours from trajectory limits.')
    initial_cnt, final_cnt = extractWormContours(masked_image_file, traj_limits)

    print('Looking for overlaping fraction between contours.')
    after_ratio = getAreaIntersecRatio(connect_after, final_cnt, initial_cnt)
    before_ratio = getAreaIntersecRatio(connect_before, initial_cnt, final_cnt)
    #maybe a graph reduction algorithm would work better...
    
    print('Getting connections between trajectories.')    
    edges_after = selectNearNodes(connect_after, after_ratio, traj_limits['t0'], min_intersect = min_area_intersect)
    edges_before = selectNearNodes(connect_before, before_ratio, -traj_limits['tf'], min_intersect = min_area_intersect)
    #switch so the lower index is first    
    edges_before = [(y,x) for x,y in edges_before]
    
    #get unique nodes
    trajectories_edges = set(edges_after+edges_before)
        
    print('Removing redundant connections.')
    DG=nx.DiGraph()
    DG.add_nodes_from(traj_limits.index)
    DG.add_edges_from(trajectories_edges)
    DG, index2rename = cleanRedundantNodes(DG)
    
    for new_index in index2rename:
        for ind in index2rename[new_index]:
            row2chg = trajectories_data.worm_index_auto.isin(index2rename[new_index])
            trajectories_data.loc[row2chg, 'worm_index_auto'] = new_index
    return DG, trajectories_data, traj_limits
    
def getRealWormsIndexes(trajectories_data, n_min_skel = 5, min_frac_skel = 0.25):
    
    N = trajectories_data.groupby('worm_index_auto').agg({'is_good_skel': ['sum', 'count']})
    frac_skel = N['is_good_skel']['sum']/N['is_good_skel']['count']
    good = (N['is_good_skel']['count'] > 5) & (frac_skel> min_frac_skel)
    worm_indexes = set(N[good].index.tolist())    
    return worm_indexes

def getPossibleClusters(DG, worm_indexes):
    
    possible_cluster = []
    for node in DG.nodes():
        node_inputs = DG.predecessors(node)
        node_outpus = DG.successors(node)
        
        if (any(x in worm_indexes for x in node_inputs) or  \
            any(x in worm_indexes for x in node_outpus)):
            possible_cluster.append(node)
    possible_cluster = set(possible_cluster)
    
    return possible_cluster
    
if __name__ == '__main__':
    #base directory
    #masked_image_file = '/Users/ajaver/Desktop/Videos/Avelino_17112015/MaskedVideos/CSTCTest_Ch5_17112015_205616.hdf5'
    #masked_image_file = '/Users/ajaver/Desktop/Videos/Avelino_17112015/MaskedVideos/CSTCTest_Ch1_17112015_205616.hdf5'
    #masked_image_file = '/Users/ajaver/Desktop/Videos/Avelino_17112015/MaskedVideos/CSTCTest_Ch1_18112015_075624.hdf5'
    #masked_image_file = '/Users/ajaver/Desktop/Videos/04-03-11/MaskedVideos/575 JU440 swimming_2011_03_04__13_16_37__8.hdf5'    
    #masked_image_file = '/Users/ajaver/Desktop/Videos/04-03-11/MaskedVideos/575 JU440 on food Rz_2011_03_04__12_55_53__7.hdf5'    
    
    #skeletons_file = masked_image_file.replace('MaskedVideos', 'Results')[:-5] + '_skeletons.hdf5'
    
#    masked_image_file = '/Users/ajaver/OneDrive - Imperial College London/tests/test_5/CSTCTest_Ch1_18112015_075624.hdf5'
#    dd = os.path.dirname(masked_image_file)
#    ff = os.path.basename(masked_image_file).replace('.hdf5', '_skeletons.hdf5')
#    skeletons_file = os.path.join(dd, 'Results',ff )
#   
    masked_image_file = '/Users/ajaver/OneDrive - Imperial College London/tests/join/N2_worm10_F1-3_Set1_Pos4_Ch2_26012017_143133.hdf5'
    skeletons_file = masked_image_file.replace('MaskedVideos', 'Results')[:-5] + '_skeletons.hdf5'
    
 
    #get the trajectories table
    with pd.HDFStore(skeletons_file, 'r') as fid:
        trajectories_data = fid['/trajectories_data']
        trajectories_data['worm_index_auto'] = trajectories_data['worm_index_joined'] 
    
    DG, trajectories_data, traj_limits = getTrajGraph(trajectories_data, masked_image_file, \
                                             max_gap = 25, min_area_intersect = 0.5)
    

#%%
    worm_indexes = getRealWormsIndexes(trajectories_data, n_min_skel = 5, min_frac_skel = 0.25)
    possible_cluster = getPossibleClusters(DG, worm_indexes)
    #%%
    
    candidate2split = possible_cluster & worm_indexes
    
    trajdata2split = trajectories_data[trajectories_data['worm_index_auto'].isin(candidate2split)]
    worm_traj_limits = traj_limits[traj_limits['worm_index'].isin(worm_indexes)]
    
    
    first_frame = trajdata2split['frame_number'].min()
    last_frame = trajdata2split['frame_number'].max()
    
    trajgrouped = trajdata2split.groupby('frame_number')    
    
    valid_frames = trajdata2split['frame_number'].unique()
    break_points = []
    

    for ind_check, row in worm_traj_limits.iterrows():
        
        t_prev = row['t0']-1
        t_next = row['tf']+1
        
        Rlim = row['roi_size']**2
        
        if t_prev in valid_frames:
            dat_prev = trajgrouped.get_group(t_prev);
            
            delX = row['x0'] - dat_prev['coord_x']
            delY = row['y0'] - dat_prev['coord_y']
            R = delX*delX + delY*delY
            dat_prev = dat_prev[R <= Rlim]
            
            if len(dat_prev)>0:
                for _, rr in dat_prev.iterrows():
                    ind_split = int(rr['worm_index_auto'])
                    dat_split = (rr['coord_x'], rr['coord_y'], rr['roi_size'], rr['threshold'], rr['area']/2)
                    dat_check = (row['x0'], row['y0'], row['roi_size'], row['th0'], row['a0']/2)
                    
                    assert t_prev == rr['frame_number']
                    assert t_prev + 1 == row['t0']
                    
                    break_points.append((ind_split, t_prev, dat_split, ind_check, t_prev+1, dat_check))
        
                        
        if t_next in valid_frames:
            dat_next = trajgrouped.get_group(t_next);
            
            delX = row['xf'] - dat_next['coord_x']
            delY = row['yf'] - dat_next['coord_y']
            R = delX*delX + delY*delY
            dat_next = dat_next[R <= Rlim]
            
            if len(dat_next)>0:
                for _, rr in dat_next.iterrows():
                    ind_split = int(rr['worm_index_auto'])
                    dat_split = (rr['coord_x'], rr['coord_y'], rr['roi_size'], rr['threshold'], rr['area']/2)
                    dat_check = (row['xf'], row['yf'], row['roi_size'], row['thf'], row['af']/2)
                    
                    assert t_next == rr['frame_number']
                    assert t_next - 1 == row['tf']
                    
                    break_points.append((ind_split, t_next, dat_split, ind_check, t_next-1, dat_check))
        #if 949
        
    #only search possible break points that occur in the middle of a trajectory
    traj2split_limits = trajdata2split.groupby('worm_index_auto').aggregate({'frame_number':[np.min, np.max]})
    traj2split_limits = {x:(row['frame_number']['amin'], row['frame_number']['amax']) 
                        for x, row in traj2split_limits.iterrows()}
    break_points = [x for x in break_points if not x[1] in traj2split_limits[x[0]]]      
    
    #WHAT    
    #%%
    #break_points = [(1, 21184.0, (1097.2508544921875, 1517.0625, 131.0, 69.0, 744.5), 415, 21183.0, (1059.6776123046875, 1485.4439697265625, 73.0, 69.0, 378.5))]    
    
    points2split = []
    with tables.File(masked_image_file, 'r') as fid:
        mask_group = fid.get_node('/mask')

        for ind_split, t_split, dat_split, ind_check, t_check, dat_check in break_points:
            img_split = mask_group[int(t_split),:,:]
            cnt_split = getIndCnt(img_split, *dat_split)
            
            img_check = mask_group[int(t_check),:,:]
            cnt_check = getIndCnt(img_check, *dat_check)
            
            if len(cnt_check) == 0 or len(cnt_split) == 0:
                continue
            
            bot = np.minimum(np.amin(cnt_split,0), np.amin(cnt_check, 0))
            top = np.maximum(np.amax(cnt_split,0), np.amax(cnt_check, 0))
            
            roi_size = roi_size = top-bot + (1,1)
            roi_size = roi_size[::-1]
            
            mask_split = np.zeros(roi_size, np.int32)
            cnt_split = [(cnt_split-bot).astype(np.int32)];
            cv2.drawContours(mask_split, cnt_split, 0, 1, -1)
            
            mask_check = np.zeros(roi_size, np.int32)
            cnt_check = [(cnt_check-bot).astype(np.int32)];
            cv2.drawContours(mask_check, cnt_check, 0, 1, -1)
            
            area_intersect = np.sum(mask_check & mask_split)
            area_check = np.sum(mask_check)
            
            if area_intersect/area_check > 0.5:
                points2split.append((ind_split, t_split, t_check))
    #%%    
    last_index = trajectories_data['worm_index_auto'].max()
    
    for worm_ind, split_t1, slit_t2 in points2split:
        new_ind1 = last_index+1
        new_ind2 = last_index+2
        last_index =  new_ind2
        
        good = trajectories_data['worm_index_auto'] == worm_ind
        frames = trajectories_data.loc[good, 'frame_number']
        frames = frames.sort_values(inplace=False)
        
        assert abs(split_t1-slit_t2) == 1
        
        #select the split point depending if it was after or before the point. 
        #Probably there is a cleaner way to do this (and explain it)
        good = frames >= split_t1 if split_t1 > slit_t2 else frames <= split_t1
        
        index1 = frames[good].index
        index2 = frames[~good].index
        trajectories_data.ix[index1, 'worm_index_auto'] = new_ind1
        trajectories_data.ix[index2, 'worm_index_auto'] = new_ind2
    
    #%%
    #rename indexes so we use smaller numbers
    
    #create a dictionary to map from old to new indexes  
    dd = trajectories_data.groupby('worm_index_auto').agg({'frame_number':'min'})
    dd = dd.to_records()
    dd.sort(order=['frame_number', 'worm_index_auto'])
    new_ind_dict = {x:ii+1 for ii,x in enumerate(dd['worm_index_auto'])}
    
    #replace the data from the new indexes (pandas replace do not work because the dict and keys values must be different)
    worm_index_auto = trajectories_data['worm_index_auto'].values
    worm_index_auto = [new_ind_dict[x] for x in worm_index_auto]
    trajectories_data['worm_index_auto'] = worm_index_auto

    #%%
    #recalculate the trajectories graph. This is slower but easier than having to make the corrections manually.
    DG, trajectories_data, traj_limits = getTrajGraph(trajectories_data, masked_image_file, \
                                             max_gap = 25, min_area_intersect = 0.5)
    
    
    worm_indexes = getRealWormsIndexes(trajectories_data, n_min_skel = 5, min_frac_skel = 0.25)
    possible_cluster = getPossibleClusters(DG, worm_indexes)
    
    
    #%%    
    good_worms = worm_indexes - possible_cluster
    good_clusters = possible_cluster - worm_indexes

    bad_index = []
    for subgraph in nx.connected_component_subgraphs(DG.to_undirected()):
        subgraph_nodes = subgraph.nodes()
        if not any(x in worm_indexes for x in subgraph_nodes):
            bad_index += subgraph_nodes
    
    
    #%%
    trajectories_data['auto_label'] = WLAB['U']
    
    good = trajectories_data.worm_index_auto.isin(good_worms)
    trajectories_data.loc[good, 'auto_label'] = WLAB['WORM']
    
    good = trajectories_data.worm_index_auto.isin(good_clusters)
    trajectories_data.loc[good, 'auto_label'] = WLAB['WORMS']
    
    good = trajectories_data.worm_index_auto.isin(bad_index)
    trajectories_data.loc[good, 'auto_label'] = WLAB['BAD']

    #let's save this data into the skeletons file
    saveModifiedTrajData(skeletons_file, trajectories_data)
    