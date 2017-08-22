# -*- coding: utf-8 -*-
"""
This module defines the NormalizedWorm class

"""
import numpy as np
from helper import DataPartition, nanunwrap

#%%
def _h_orientation_vector(x, axis=None):
    return x[:, 0, :] - x[:, -1, :]

def _h_get_velocity(x, delta_frames, fps):
    delta_time = delta_frames/fps
    v = (x[delta_frames:] - x[:-delta_frames])/delta_time
    return v

#%%
def _h_center_skeleton(skeletons, orientation, coords):
    
    Rsin = np.sin(orientation)[:, None]
    Rcos = np.cos(orientation)[:, None]

    skel_c = skeletons - coords[:, None, :]

    skel_ang = np.zeros_like(skel_c)
    skel_ang[:, :, 0] = skel_c[:, :, 0]*Rcos - skel_c[:, :, 1]*Rsin
    skel_ang[:, :, 1] = skel_c[:, :, 0]*Rsin + skel_c[:, :, 1]*Rcos
    
    return skel_ang

def _h_segment_position(skeletons, partition):
    p_obj = DataPartition([partition], n_segments=skeletons.shape[1])
    coords = p_obj.apply(skeletons, partition, func=np.mean)
    orientation_v = p_obj.apply(skeletons, partition, func=_h_orientation_vector)
    return coords, orientation_v

#%%
def get_midbody_velocity(skeletons, delta_frames, fps, _is_plot = False):
    coords, orientation_v = _h_segment_position(skeletons, partition = 'midbody')
    
    velocity = _h_get_velocity(coords, delta_frames, fps)
    speed = np.linalg.norm(velocity, axis=1)
    #I do not need to normalize the vectors because it will only add a constant factor, 
    #and I am only interested in the sign
    s_sign = np.sign(np.sum(velocity*orientation_v[delta_frames:], axis=1))
    signed_speed = speed *s_sign
    
    #let's change the vector to angles
    orientation = np.arctan2(orientation_v[:, 0], orientation_v[:, 1])
    #wrap the angles so the change is continous no jump between np.pi and -np.pi
    orientation = nanunwrap(orientation) 
    angular_velocity = _h_get_velocity(orientation, delta_frames, fps)
    
    centered_skeleton = _h_center_skeleton(skeletons, orientation, coords)
    
    return signed_speed, angular_velocity, centered_skeleton

#%%
def _h_relative_velocity(segment_coords, delta_frames, fps):
    x = segment_coords[:, 0]
    y = segment_coords[:, 1]
    r = np.sqrt(x**2+y**2)
    theta = nanunwrap(np.arctan2(y,x))
    
    r_radial_velocity = _h_get_velocity(r, delta_frames, fps)
    r_angular_velocity = _h_get_velocity(theta, delta_frames, fps)
    return r_radial_velocity, r_angular_velocity


def get_relative_velocities(centered_skeleton, delta_frames, fps):
    partitions = ['head_tip', 'head', 'neck', 'hips', 'tail', 'tail_tip']
    p_obj = DataPartition(partitions, n_segments=centered_skeleton.shape[1])

    r_radial_velocities = {}
    r_angular_velocities = {}
    for p in partitions:
        segment_coords = p_obj.apply(centered_skeleton, p, func=np.mean)
        r_radial_velocity, r_angular_velocity = _h_relative_velocity(segment_coords, delta_frames, fps)
        r_radial_velocities[p] = r_radial_velocity
        r_angular_velocities[p] = r_angular_velocity
    
    return r_radial_velocities, r_angular_velocities
#%%
import matplotlib.pylab as plt
from matplotlib import animation, patches

def _h_ax_range(skel_a):
    x_range = [np.nanmin(skel_a[...,0]), np.nanmax(skel_a[...,0])]
    y_range = [np.nanmin(skel_a[...,1]), np.nanmax(skel_a[...,1])]
    
    dx, dy = np.diff(x_range), np.diff(y_range)
    if dx > dy:
        y_range[1] = y_range[0] + dx
    else:
        x_range[1] = x_range[0] + dy
    
    return (x_range, y_range)

def animate_velocity(skel_a, ini_arrow, arrow_size, speed_v, ang_v):
    x_range, y_range = _h_ax_range(skel_a)
    fig = plt.figure(figsize = (15, 8))
    ax = plt.subplot(1,2,1)
    ax_speed = plt.subplot(2,2,2)
    ax_ang_speed = plt.subplot(2,2,4)
    ax.set_xlim(*x_range)
    ax.set_ylim(*y_range)
    
    line, = ax.plot([], [], lw=2)
    head_p, = ax.plot([], [], 'o')
    orient_arrow = patches.Arrow(*ini_arrow[0], *arrow_size[0], fc='k', ec='k')
    
    ax_speed.plot(speed_v)
    ax_ang_speed.plot(ang_v)
    
    speed_p, = ax_speed.plot([], 'o') 
    ang_speed_p, = ax_ang_speed.plot([],  'o') 
    
    # animation function. This is called sequentially
    def _animate(i):
        global orient_arrow
        
        x = skel_a[i, :, 0]
        y = skel_a[i, :, 1]
        line.set_data(x, y)
        head_p.set_data(x[0], y[0])
        if ax.patches:
            ax.patches.remove(orient_arrow) 
        orient_arrow = patches.Arrow(*ini_arrow[i], *arrow_size[i], width=50, fc='k', ec='k')
        ax.add_patch(orient_arrow)
        
        speed_p.set_data(i, speed_v[i])
        ang_speed_p.set_data(i, ang_v[i])
        return (line, head_p, orient_arrow, speed_p, ang_speed_p)
    
    # call the animator. blit=True means only re-draw the parts that have changed.
    anim = animation.FuncAnimation(fig, _animate,
                                   frames=skel_a.shape[0], interval=20, blit=True);
    return anim
                            