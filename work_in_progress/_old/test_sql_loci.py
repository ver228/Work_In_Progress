# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 12:20:26 2015

@author: ajaver
"""
import sqlite3
import numpy as np
import matplotlib.pylab as plt

database_name = '/Users/ajaver/Desktop/loci_data.db'

conn = sqlite3.connect(database_name);
cur = conn.cursor()

#%%
cur.execute('''
SELECT v.video_id, count(p.particle_id) FROM particles as p
JOIN videos as v ON v.video_id = p.video_id
GROUP BY v.video_id
''')

aa = cur.fetchall()

particles_per_video = [0]*len(aa)
for vid, N in aa:
    particles_per_video[vid-1] = N


#%%
vid_id = 2#np.argmax(particles_per_video)+1

cur.execute('''
SELECT particle_id
FROM particles
WHERE video_id = %i
''' % vid_id)
particles_id = cur.fetchall()
particles_id = np.asarray(particles_id).squeeze()


#%%
plt.figure()
for p_id in particles_id:
    cur.execute('''
    SELECT video_time, coord_x, coord_y
    FROM coordinates
    WHERE particle_id = %i;
        ''' % p_id)
    
    time, xx, yy = list(zip(*cur.fetchall()))
    plt.plot(xx,yy)
    

#%%
