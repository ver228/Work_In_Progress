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
import tables
import numpy as np
from collections import OrderedDict
import cv2
import networkx as nx
import warnings
from fix_wrong_merges import ImageRigBuff, get_border_cnt, get_traj_limits, fix_wrong_merges
from tierpsy.helper.misc import WLAB, save_modified_table

def get_traj_limits_cnts(masked_image_file, traj_limits, buf_size = 11):
    grouped_t0 = traj_limits.groupby('t0')
    grouped_tf = traj_limits.groupby('tf')
    
    uT0 = np.unique(traj_limits['t0'])
    uTf = np.unique(traj_limits['tf'])
    
    initial_cnt = OrderedDict()
    final_cnt = OrderedDict()
    
    with tables.File(masked_image_file, 'r') as fid:
        mask_group = fid.get_node('/mask')
        ir = ImageRigBuff(mask_group, buf_size)
        for frame_number in np.unique(np.concatenate((uT0,uTf))):
            #img = mask_group[frame_number]
            
            img_c, img_r = ir.get_buff_reduced(frame_number)

            if frame_number in uT0:
                dd = grouped_t0.get_group(frame_number)
                for ff, row in dd.iterrows():
                    roi_data = (row['x0'], 
                                row['y0'], 
                                row['roi_size'], 
                                row['th0'], 
                                row['a0']/2)
                    worm_cnt = get_border_cnt(img_r, img_c, roi_data)
                    initial_cnt[int(row['worm_index'])] = worm_cnt
            if frame_number in uTf:
                dd = grouped_tf.get_group(frame_number) 
                for ff, row in dd.iterrows():
                    roi_data = (row['xf'], 
                                row['yf'], 
                                row['roi_size'], 
                                row['thf'], 
                                row['af']/2)
                    worm_cnt = get_border_cnt(img_r, img_c, roi_data)
                    final_cnt[int(row['worm_index'])] = worm_cnt
                    
        return initial_cnt, final_cnt 
 
def get_possible_connections(traj_limits, max_gap = 25):
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

def get_intersect_ratio(connect_dict, node1_cnts, node2_cnts):    

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

def select_near_nodes(connect_dict, ratio_dict, time_table, min_intersect = 0.5):
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

if __name__ == '__main__':
    import matplotlib.pylab as plt
    import glob
    import os
    from tierpsy.helper.misc import RESERVED_EXT
    
    max_gap = 25
    min_area_intersect = 0.5
    #mask_dir = '/Volumes/behavgenom_archive$/Avelino/screening/CeNDR/MaskedVideos/CeNDR_Set1_310517/'
    #mask_dir = '/Volumes/behavgenom_archive$/Avelino/screening/CeNDR/MaskedVideos/CeNDR_Set1_160517/'
    #mask_dir = '/Volumes/behavgenom_archive$/Avelino/screening/CeNDR/MaskedVideos/CeNDR_Set1_020617/'
    #mask_dir = '/Volumes/behavgenom_archive$/Avelino/Worm_Rig_Tests/Test_Food/MaskedVideos/FoodDilution_041116'
    #mask_dir = '/Volumes/behavgenom_archive$/Avelino/screening/Development/MaskedVideos/Development_C1_170617/'
    #mask_dir = '/Volumes/behavgenom_archive$/Avelino/screening/Development/MaskedVideos/**/'
    #mask_dir = '/Users/ajaver/OneDrive - Imperial College London/optogenetics/ATR_210417'
    mask_dir = '/Users/ajaver/OneDrive - Imperial College London/optogenetics/Arantza/MaskedVideos/**/'
    
    fnames = glob.glob(os.path.join(mask_dir, '*.hdf5'))
    fnames = [x for x in fnames if not any(x.endswith(ext) for ext in RESERVED_EXT)]
    
    for mask_video in fnames:
        skeletons_file = mask_video.replace('MaskedVideos','Results').replace('.hdf5', '_skeletons.hdf5')
        
        print(os.path.basename(mask_video))
        #%%
        print('Fixing wrong merge events.')
        trajectories_data, splitted_points = \
        fix_wrong_merges(mask_video,
                         skeletons_file, 
                         min_area_limit=50,
                         worm_index_type='worm_index_joined')
        #%%
        #Getting the trajectories starting and ending points.
        traj_limits = get_traj_limits(trajectories_data, 
                                      worm_index_type='worm_index_auto')
        
        #Getting possible connecting point.
        connect_before, connect_after = \
        get_possible_connections(traj_limits, max_gap = 25)
        
        #Extracting worm contours from trajectory limits.
        initial_cnt, final_cnt = get_traj_limits_cnts(mask_video, traj_limits)
    
        
        #Looking for overlaping fraction between contours.
        after_ratio = get_intersect_ratio(connect_after, final_cnt, initial_cnt)
        before_ratio = get_intersect_ratio(connect_before, initial_cnt, final_cnt)
        
        #Getting connections between trajectories.  
        edges_after = select_near_nodes(connect_after, after_ratio, traj_limits['t0'], min_intersect = min_area_intersect)
        edges_before = select_near_nodes(connect_before, before_ratio, -traj_limits['tf'], min_intersect = min_area_intersect)
        #switch so the lower index is first    
        edges_before = [(y,x) for x,y in edges_before]
        
        #get unique nodes
        trajectories_edges = set(edges_after+edges_before)
        
        #print('Removing redundant connections.')
        DG=nx.DiGraph()
        DG.add_nodes_from(traj_limits.index)
        DG.add_edges_from(trajectories_edges)
        
        
        #%%
        min_frac_skel = 0.25
        
        traj_g = trajectories_data.groupby('worm_index_auto')
        dat = traj_g.agg({'is_good_skel': np.nansum, 'frame_number': 'count'})
        frac_skeletons = dat['is_good_skel']/dat['frame_number']
        #maybe use movement?
        
        likely_single_worms = set(frac_skeletons[frac_skeletons>min_frac_skel].index)
        #%%
        bad_particles = []
        for gg in nx.connected_component_subgraphs(DG.to_undirected()):
            g_nodes = gg.nodes()
            if not any(x in likely_single_worms for x in g_nodes):
                bad_particles += g_nodes
        
        good_nodes = set(DG.nodes()) - set(bad_particles)
        DG_f = DG.subgraph(good_nodes)
        
        #%%
        weird_nodes = []
        for node in likely_single_worms:
            ins = DG.predecessors(node)
            outs = DG.successors(node)
            
            if len(ins)>1 or len(outs) >1:
                warnings.warn('{} {} {} Weird single worm merged/split.'.format(node, ins, outs))
            
            if len(ins) > 1:
                weird_nodes += ins
            elif len(outs) > 1:
                weird_nodes += outs
        
        if weird_nodes:
            weird_nodes = set(weird_nodes) - likely_single_worms
            
            print(weird_nodes)
        #%%
        #i need to add a node to the outside of the plate...
        edges_order = {x:i for i,x in enumerate(DG_f.edges())}
        
        #nodes2check = {x:0 for x in good_nodes - set(likely_single_worms)}
        #knonwn_sizes = {x:1 for x in likely_single_worms}
        
        A = []
        B = []
        
        #remaining_nodes = {}
        for node in DG_f.nodes():
            ins = DG_f.predecessors(node)
            outs = DG_f.successors(node)
            
            edges_ins = [(ini, node) for ini in ins]
            edges_outs =  [(node, out) for out in outs]
            
            assert all(x in edges_order for x in edges_ins+edges_outs)
            
            if edges_ins and edges_outs:
                a = np.zeros(len(edges_order))
                for ini in edges_ins:
                    a[edges_order[ini]] = 1
                for out in edges_outs:
                    a[edges_order[out]] = -1
                
                A.append(a)
                B.append(0)
            
            if node in likely_single_worms:
                if edges_ins:
                    a = np.zeros(len(edges_order))
                    for ini in edges_ins:
                        a[edges_order[ini]] = 1
                    A.append(a)
                    B.append(1)
                if edges_outs:
                    a = np.zeros(len(edges_order))
                    for out in edges_outs:
                        a[edges_order[out]] = -1
                    A.append(a)
                    B.append(-1)
                
        #%%
        A = np.array(A)
        B = np.array(B)
        print(np.linalg.lstsq(A,B))
            
            
            
            
        #%%
            
            
#        dd = {}
#        possible_cluster
#        for node in DG.nodes():
#            node_inputs = DG.predecessors(node)
#            node_outpus = DG.successors(node)
#            dd[node] = (len(node_inputs), len(node_outpus))
#            
#            if (any(x in worm_indexes for x in node_inputs) or  \
#                any(x in worm_indexes for x in node_outpus)):
#                possible_cluster.append(node)
#        possible_cluster = set(possible_cluster)
        
        
        #%%
        trajectories_data['auto_label'] = WLAB['U']
        
        good = trajectories_data['worm_index_auto'].isin(likely_single_worms)
        trajectories_data.loc[good, 'auto_label'] = WLAB['WORM']
        
        good = trajectories_data['worm_index_auto'].isin(bad_particles)
        trajectories_data.loc[good, 'auto_label'] = WLAB['BAD']
        
        
        assert (trajectories_data['skeleton_id']==trajectories_data.index).all()
        
        #let's save this data into the skeletons file
        save_modified_table(skeletons_file, trajectories_data, 'trajectories_data')
        
        