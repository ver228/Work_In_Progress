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
from tierpsy.helper.misc import WLAB, save_modified_table, get_base_name, print_flush
from fix_wrong_merges import ImageRigBuff, get_border_cnt, \
get_traj_limits, fix_wrong_merges


def get_traj_limits_cnts(mask_video, 
                         traj_limits, 
                         buf_size,
                         border_range):
    
    grouped_t0 = traj_limits.groupby('t0')
    grouped_tf = traj_limits.groupby('tf')
    
    uT0 = np.unique(traj_limits['t0'])
    uTf = np.unique(traj_limits['tf'])
    
    initial_cnt = OrderedDict()
    final_cnt = OrderedDict()
    
    
    with tables.File(mask_video, 'r') as fid:
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
                    initial_cnt[int(row['worm_index'])] = \
                    get_border_cnt(img_r, img_c, roi_data, border_range)
                    
            if frame_number in uTf:
                dd = grouped_tf.get_group(frame_number) 
                for ff, row in dd.iterrows():
                    roi_data = (row['xf'], 
                                row['yf'], 
                                row['roi_size'], 
                                row['thf'], 
                                row['af']/2)
                    final_cnt[int(row['worm_index'])] = \
                    get_border_cnt(img_r, img_c, roi_data, border_range)
                    
                    
#                    if ff == 27:
#                        import matplotlib.pylab
#                        cnt, _ = get_border_cnt(img_r, img_c, roi_data, border_range)
#                        plt.figure()
#                        plt.plot(cnt[:, 0], cnt[:, 1])
#                        plt.title(ff)
#                        plt.axis('equal')
                    
        return initial_cnt, final_cnt 
 
def get_possible_connections(traj_limits, max_gap):
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
        current_cnt, is_border = node1_cnts[current_ind]
        
        if current_cnt.size == 0:
            continue
        bot = np.min(current_cnt, axis=0);
        top = np.max(current_cnt, axis=0);
        
        for pii in connect_dict[current_ind]:
            cnt2check, _ = node2_cnts[pii]
            
            if cnt2check.size == 0:
                continue
            bot_p = np.min(cnt2check,axis=0);
            top_p = np.max(cnt2check,axis=0);
            
            bot = np.min((bot, bot_p), axis=0)
            top = np.max((top, top_p), axis=0)
        
        roi_size = top-bot + (1,1)
        roi_size = roi_size[::-1]
    
        mask_curr = np.zeros(roi_size, np.int32)
        worm_cnt = [(current_cnt-bot).astype(np.int32)];
        cv2.drawContours(mask_curr, worm_cnt, 0, 1, -1)
        area_curr = np.sum(mask_curr)    
        
        for pii in connect_dict[current_ind]:
            cnt2check, _ = node2_cnts[pii]
            if cnt2check.size == 0:
                continue
            mask_possible = np.zeros(roi_size, np.int32)
            worm_cnt = [(cnt2check-bot).astype(np.int32)];
            cv2.drawContours(mask_possible, worm_cnt, 0, 1, -1)
            
            area_intersect = np.sum(mask_curr & mask_possible)
        
            intersect_ratio[(current_ind, pii)] = area_intersect/area_curr
        
    return intersect_ratio

def select_near_nodes(connect_dict, 
                      ratio_dict, 
                      time_table, 
                      min_intersect):
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

def create_conn_graph(mask_video, 
                      trajectories_data,
                      buf_size,
                      border_range,
                      max_conn_gap,
                      min_area_intersect):
    #%%
    #Getting the trajectories starting and ending points.
    traj_limits = get_traj_limits(trajectories_data, 
                                  worm_index_type='worm_index_auto', 
                                  win_area = buf_size)
    
    #Extracting worm contours from each point in trajectory limits.
    initial_cnt, final_cnt = get_traj_limits_cnts(mask_video, 
                                                  traj_limits,
                                                  buf_size=buf_size,
                                                  border_range=border_range)
    

    #%%
    #Getting possible connecting point.
    connect_before, connect_after = \
    get_possible_connections(traj_limits, max_gap = max_conn_gap)
    
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
    
    return DG, initial_cnt, final_cnt
#%%
def get_likely_worms(trajectories_data, 
                     min_frac_skel,
                     worm_index_type):
    '''
    I am using the number of good skeletons as a proxy for a trajectory to be a worm.
    It might be better to use a neural network in the future.
    '''
    #maybe i should use a neural network here...
    
    traj_g = trajectories_data.groupby(worm_index_type)
    dat = traj_g.agg({'is_good_skel': np.nansum, 'frame_number': 'count'})
    frac_skeletons = dat['is_good_skel']/dat['frame_number']
    #maybe use movement?
    
    likely_single_worms = set(frac_skeletons[frac_skeletons>min_frac_skel].index)
    
    return likely_single_worms
#%%
def add_border_egdes(DG_f, initial_cnt, final_cnt):
    '''I am adding possible edges to the border of the video labeled as -100.
    I am doing it after removing the bad nodes because otherwise some of those 
    bad nodes will appear connected to the main network'''
    border_edges = []
    for node in DG_f.nodes():
        if node in initial_cnt:
            _,is_border = initial_cnt[node]
            if is_border:
                border_edges.append((-100, node))
        if node in final_cnt:
            _,is_border = final_cnt[node]
            if is_border:
                border_edges.append((node,-100)) 
    if border_edges:
        DG_f.add_node(-100)
        DG_f.add_edges_from(border_edges)
    return DG_f

def _get_bad_nodes(DG_f, likely_single_worms):
    bad_nodes = []
    for gg in nx.connected_component_subgraphs(DG_f.to_undirected()):
        g_nodes = gg.nodes()
        if not any(x in likely_single_worms for x in g_nodes):
            bad_nodes += g_nodes
    return bad_nodes


def remove_unconnected_nodes(DG, likely_single_worms):
    '''
    I am considering as a bad node, anything that does not connect to a likely worm.
    Again, in the feature I should use a neural network for this.
    '''
    
    bad_particles = _get_bad_nodes(DG, likely_single_worms)
    bad_particles = []

    # This worms are inconsistent (weird).
    #this are likely a worm gets in the way of a bad particle and confouses the algorithm.
    #Maybe i can fix it but for the moment I will just remove the weird nodes
    weird_nodes = []
    for node in likely_single_worms:
        ins = DG.predecessors(node)
        outs = DG.successors(node)
        
        #if len(ins)>1 or len(outs) >1:
        #    warnings.warn('{} {} {} Weird single worm merged/split.'.format(node, ins, outs))
        
        if len(ins) > 1:
            weird_nodes += ins
        elif len(outs) > 1:
            weird_nodes += outs
    
    if weird_nodes:
        weird_nodes = set(weird_nodes) - likely_single_worms
        
    good_nodes = set(DG.nodes()) - set(bad_particles) -set(weird_nodes)
    
    DG_f = DG.subgraph(good_nodes)
    return DG_f

def get_nodes_weights(all_nodes, DG_f, edges_weights, likely_single_worms):
    #intialize node_weights
    node_weights = {x: 0 for x in all_nodes}
    for node in DG_f.nodes():
        if node == -100:
            continue
        
        if node in likely_single_worms:
            # A likely worm must be 1
            node_weights[node] = 1 
            continue
        
        edges_in = [(i,node) for i in DG_f.predecessors(node)]
        edges_out = [(node, i) for i in DG_f.successors(node)]
        
        #remove edges that for some reason were not calculated (likely worng edges)
        edges_in = [x for x in edges_in if x in edges_weights]
        edges_out = [x for x in edges_in if x in edges_weights]
        
        tot_in = sum(edges_weights[e] for e in edges_in)
        is_neg_in = any(edges_weights[e]<0 for e in edges_in)
        tot_out = sum(edges_weights[e] for e in edges_out)
        is_neg_out = any(edges_weights[e]<0 for e in edges_in)
        
        if edges_in and edges_out:
            if tot_in == tot_out and \
            tot_in >= 0 and \
            not (is_neg_in or is_neg_out):
                node_weights[node] = tot_in
            else:
                #there was something funny in the fitting
                node_weights[node] = -min(tot_in, tot_out)
                if node_weights[node] > 0: 
                    #this is in case the fit was actually negative
                    node_weights[node] = -node_weights[node]
        elif edges_in:
            #do not have successors (trajectory end)
            node_weights[node] = tot_in
        elif edges_out:
            #do not have predecessors (trajectory start)
            node_weights[node] = tot_out
        elif node in likely_single_worms:
            node_weights[node] = 1
    return node_weights

def fit_edges_weights(DG_f, likely_single_worms):
    '''I am trying to solve the equations system to get each edge weight.
    The sum of the edges weights entering to a node must be equal to
    the sum of the edges leaving.
    I am using numpy least squares to solve the equation.
    '''
    #%%
    known_edges = {}
    for node in likely_single_worms:
        ins = DG_f.predecessors(node)
        outs = DG_f.successors(node)
        
        if len(ins) == 1: 
            known_edges[(ins[0], node)] = 1
            
        if len(outs) == 1:
            known_edges[(node, outs[0])] = 1
            
    #%%
    edges2check = [x for x in DG_f.edges() if not x in known_edges]
    
    #%%
    edges_order = {x:i for i,x in enumerate(edges2check)}
    A = []
    B = []
    for node in DG_f.nodes():
        if node < 0:
            continue
        
        ins = DG_f.predecessors(node)
        outs = DG_f.successors(node)
        
        edges_ins = [(ini, node) for ini in ins]
        edges_outs =  [(node, out) for out in outs]
        
        #assert all(x in edges_order for x in edges_ins+edges_outs)
        
        if edges_ins and edges_outs:
            a = np.zeros(len(edges_order))
            b = 0
            
            for ini in edges_ins:
                if ini in known_edges:
                    b -= known_edges[ini]
                else:
                    a[edges_order[ini]] = 1
            for out in edges_outs:
                if out in known_edges:
                    b += known_edges[out]
                else:
                    a[edges_order[out]] = -1
            
            if not np.all(a==0):
                A.append(a)
                B.append(b)
    
    if len(A) == 0: 
        #continue if no valid edges for fit were found
        edges_weights = known_edges
    else:
        assert len(A) == len(B)
        A = np.array(A)
        B = np.array(B)
        best_fit, residuals, rank, s  = np.linalg.lstsq(A,B)
        #for ii, x in zip(edges_order, best_fit):
        #    print(ii, x)
        #the weights must be integers so I am approximating here
        edges_weights = {x:int(round(best_fit[ii])) for x,ii in edges_order.items() }
    
        for x in known_edges:
            edges_weights[x] = known_edges[x]
    #%%
    return edges_weights

def correct_bad_weights(DG, likely_single_worms, node_weights):
    '''remove the bad nodes, if there is an unconnected set of nodes, 
    if there are subgraphs with no single worms it is very likely 
    they are due to an error'''
    
    
    def _correct_bad_w():
        DG_f2 = DG.copy()
        for node in node_weights:
            if node_weights[node] <= 0 :
                DG_f2.remove_node(node)
        return _get_bad_nodes(DG_f2, likely_single_worms)
    
    for ii in range(5):
        #I repeat it a few times just to be sure...
        bad_particles = _correct_bad_w()
        if not bad_particles:
            break
        for n in bad_particles:
            node_weights[n] = 0
    
    return node_weights
#%%
def merge_redundant_nodes(DG_f):
    
    redundant_nodes = []
    for node in DG_f:
        ins = DG_f.predecessors(node)
        outs = DG_f.successors(node)
        if len(ins) == 1 and len(outs) == 1:
            redundant_nodes.append(node)
    
    
    nodes_merged = {}
    DG_f_merged = DG_f.copy()
    #reduce nodes consider the case of several successive single connections
    reduced_g = DG_f.subgraph(redundant_nodes)
    
    for sub_g in nx.connected_component_subgraphs(reduced_g.to_undirected()):
        
        nodes2check = sub_g.nodes()
        
        root_ini = [n for n in nodes2check 
                    if not DG_f.predecessors(n) in nodes2check]
        assert len(root_ini)==1 
        root_ini = root_ini[0]
        ini_pred = DG_f.predecessors(root_ini)[0]
        if len(DG_f.successors(ini_pred)) == 1:
            root_ini = ini_pred
        
        root_end = [n for n in nodes2check 
                    if not DG_f.successors(n) in nodes2check]
        assert len(root_end)==1 
        root_end = root_end[0]
        
        
        end_succ = DG_f.successors(root_end)[0]
        if len(DG_f.predecessors(end_succ)) == 1:
            root_end = end_succ
        nodes2remove = [x for x in nodes2check 
                        if x != root_ini and x!=root_end]
        
        if nodes2remove:
            for n in nodes2remove:
                nodes_merged[n] = root_ini
            
            DG_f_merged.add_edge(root_ini, root_end)
            DG_f_merged.remove_nodes_from(nodes2remove) 
       
    return DG_f_merged, nodes_merged
#%%
def get_node_weights(trajectories_data,
                     mask_video, 
                     buf_size,
                     border_range,
                     max_conn_gap,
                     min_area_intersect,
                     min_frac_skel
                     ):
    #%%
    DG, initial_cnt, final_cnt = create_conn_graph(mask_video, 
                                                   trajectories_data,
                                                   buf_size,
                                                   border_range,
                                                   max_conn_gap,
                                                   min_area_intersect)
    #%%
    DG_merged = DG
    DG_merged, nodes_merged = merge_redundant_nodes(DG)
    
    assert len(merge_redundant_nodes(DG_merged)[1]) == 0
    #slower but better (it seems that pandas .replace assumes 1 to 1 mapping)
    trajectories_data['worm_index_auto'] = \
    [x if not x in nodes_merged else nodes_merged[x] 
    for x in trajectories_data['worm_index_auto']]
    
    likely_single_worms = get_likely_worms(trajectories_data, 
                                           min_frac_skel = min_frac_skel,
                                           worm_index_type='worm_index_auto')
    print(likely_single_worms, DG_merged.nodes())
    
    assert len(likely_single_worms-set(DG_merged.nodes())) == 0
    #%%
    DG_f = remove_unconnected_nodes(DG_merged, likely_single_worms)
    DG_f = add_border_egdes(DG_f, initial_cnt, final_cnt)
    #%%
    edges_weights = fit_edges_weights(DG_f, likely_single_worms)
    
    
    
    node_weights = get_nodes_weights(DG.nodes(), 
                                     DG_f, 
                                     edges_weights, 
                                     likely_single_worms)
    node_weights = correct_bad_weights(DG, likely_single_worms, node_weights)
    #%%
    return node_weights, DG_merged, trajectories_data


#%%
if __name__ == '__main__':
    import matplotlib.pylab as plt
    import glob
    import os
    from tierpsy.helper.misc import RESERVED_EXT
    
    
    
    min_area_limit = 50
            
    args_graph = dict(
            max_conn_gap = 25,
            min_area_intersect = 0.5,
            buf_size = 11,
            border_range = 10,
            min_frac_skel = 0.3
            )
            
    #mask_dir = '/Volumes/behavgenom_archive$/Avelino/screening/CeNDR/MaskedVideos/CeNDR_Set1_310517/'
    #mask_dir = '/Volumes/behavgenom_archive$/Avelino/screening/CeNDR/MaskedVideos/CeNDR_Set1_160517/'
    #mask_dir = '/Volumes/behavgenom_archive$/Avelino/screening/CeNDR/MaskedVideos/CeNDR_Set1_020617/'
    #mask_dir = '/Volumes/behavgenom_archive$/Avelino/Worm_Rig_Tests/Test_Food/MaskedVideos/FoodDilution_041116'
    #mask_dir = '/Volumes/behavgenom_archive$/Avelino/screening/Development/MaskedVideos/Development_C1_170617/'
    #mask_dir = '/Volumes/behavgenom_archive$/Avelino/screening/Development/MaskedVideos/**/'
    #mask_dir = '/Users/ajaver/OneDrive - Imperial College London/optogenetics/ATR_210417'
    #mask_dir = '/Users/ajaver/OneDrive - Imperial College London/optogenetics/Arantza/MaskedVideos/**/'
    mask_dir = '/Users/ajaver/OneDrive - Imperial College London/aggregation/'
    
    
    fnames = glob.glob(os.path.join(mask_dir, '*.hdf5'))
    #fnames = glob.glob(os.path.join(mask_dir, 'oig-8_ChR2_ATR_herms_3_Ch1_11052017_170502.hdf5'))
    fnames = [x for x in fnames if not any(x.endswith(ext) for ext in RESERVED_EXT)]
    
    for ivid, mask_video in enumerate(fnames):
        
        skeletons_file = mask_video.replace('MaskedVideos','Results').replace('.hdf5', '_skeletons.hdf5')
        if not os.path.exists(skeletons_file):
            continue
        
        base_name = get_base_name(mask_video)
        print('{} of {} {}'.format(ivid+1, len(fnames), base_name))
        
        #%%
        
        trajectories_data, splitted_points = \
        fix_wrong_merges(mask_video,
                         skeletons_file, 
                         min_area_limit
                         )
        #%%
        print_flush('{} Creating trajectories graph network.'.format(base_name))
        node_weights, DG, trajectories_data = \
        get_node_weights(trajectories_data,
                        mask_video,
                        **args_graph)
        trajectories_data['cluster_size'] = trajectories_data['worm_index_auto'].map(node_weights)
        
        #if np.any(trajectories_data['cluster_size']<0):
        #    print(node_weights)
        
        def _label(x):
            if x == 0:
                return WLAB['BAD']
            elif x == 1:
                return WLAB['WORM']
            elif x > 1:
                return WLAB['WORMS']
            else:
                return WLAB['U']
        trajectories_data['auto_label'] = trajectories_data['cluster_size'].map(_label)
        
        
        assert (trajectories_data['skeleton_id']==trajectories_data.index).all()
        
        #let's save this data into the skeletons file
        save_modified_table(skeletons_file, trajectories_data, 'trajectories_data')
        
        #save the graph tree information
        with tables.File(skeletons_file, 'r+') as fid:
            if '/trajectories_graph' in fid:
                fid.remove_node('/trajectories_graph', recursive=True)
            fid.create_group('/', 'trajectories_graph')
            fid.create_array('/trajectories_graph', 'nodes', DG.nodes())
            fid.create_array('/trajectories_graph', 'edges', np.array(DG.edges()))
        
#%%
max_conn_gap = 25
min_area_intersect = 0.5
buf_size = 11
border_range = 10
min_frac_skel = 0.3
 