# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 17:43:12 2016

@author: ajaver
"""

import h5py
import matplotlib.pylab as plt

int_file = '/Users/ajaver/Desktop/Videos/headtail/Results/acr-3 (ok2049)X on food L_2010_02_19__10_45_38___7___5_intensities.hdf5'

with h5py.File(int_file, 'r') as fid:
    straighten_worm_intensity_median = fid['/straighten_worm_intensity_median'][:]

plt.figure()
plt.imshow(straighten_worm_intensity_median.T, interpolation='none', cmap='gray')
plt.grid('off')


from MWTracker.intensityAnalysis.checkFinalOrientation import searchIntPeaks


med_int = np.median(straighten_worm_intensity_median, axis=(1,2))
plt.figure()
plt.plot(med_int, linewidth=3)
for kk in range(4): 
    plt.plot(peak_ind[kk][0], med_int[peak_ind[kk][0]], 'go', markersize=10)
    plt.plot(peak_ind[kk][1], med_int[peak_ind[kk][1]], 'sr', markersize=10)
