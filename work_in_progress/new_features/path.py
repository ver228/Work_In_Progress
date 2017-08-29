#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 15:54:00 2017

@author: ajaver
"""
import numpy as np
from helper import DataPartition

from scipy.interpolate import interp1d
from scipy.signal import savgol_filter

if __name__ == '__main__':
    #data = np.load('worm_example_small_W1.npz')
    data = np.load('worm_example.npz')
    skeletons = data['skeleton']
    ventral_contour = data['ventral_contour']
    dorsal_contour = data['dorsal_contour']
    
    
    
    p_obj = DataPartition(n_segments=skeletons.shape[1])
    
    body_coords = p_obj.apply(skeletons, 'body', func=np.mean)
    
    
    
    
    xx = body_coords[:,0]
    yy = body_coords[:,1]
    tt = np.arange(body_coords.shape[0])
    
    good = ~np.isnan(xx)
    
    x_i = xx[good] 
    y_i = yy[good] 
    t_i = tt[good]
    
    t_i = np.hstack([-1, t_i, body_coords.shape[0]]) 
    x_i = np.hstack([x_i[0], x_i, x_i[-1]]) 
    y_i = np.hstack([y_i[0], y_i, y_i[-1]]) 
    
    fx = interp1d(t_i, x_i)
    fy = interp1d(t_i, y_i)
    
    xx_i = fx(tt)
    yy_i = fy(tt)
    
    # calculate the cumulative length for each segment in the curve
    dx = np.diff(xx_i)
    dy = np.diff(yy_i)
    dr = np.sqrt(dx * dx + dy * dy)
    
    lengths = np.cumsum(dr)
    lengths = np.hstack((0, lengths))
    #%%
    fx = interp1d(lengths, xx_i)
    fy = interp1d(lengths, yy_i)
    ft = interp1d(lengths, tt)
    
    sub_lengths = np.arange(lengths[0], lengths[-1], 50)
    xs = fx(sub_lengths)
    ys = fy(sub_lengths)
    ts = ft(sub_lengths)
    #%% 
    points_window = 5
    curve = np.vstack((xs, ys)).T
    s_center = curve[points_window:-points_window] #center points
    s_left = curve[:-2*points_window] #left side points
    s_right = curve[2*points_window:] #right side points
    
    
    d_left = s_left - s_center 
    d_right = s_center - s_right
    
    #arctan2 expects the y,x angle
    ang_l = np.arctan2(d_left[...,1], d_left[...,0])
    ang_r = np.arctan2(d_right[...,1], d_right[...,0])
    ang = ang_r-ang_l
    ang = np.unwrap(ang);
    
    
    import matplotlib.pylab as plt
    plt.figure()
    plt.plot(ang)
    
    #%%
    
    
    plt.figure()
    plt.plot(xx_i, yy_i)
    plt.plot(xs, ys, '.')
    plt.axis('equal')