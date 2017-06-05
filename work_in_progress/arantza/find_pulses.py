
"""
@author: ajaver
"""

import tables
import numpy as np
import os
import glob
import matplotlib.pylab as plt


def read_light_data(mask_file):
    with tables.File(mask_file) as fid:
        mean_intensity = fid.get_node('/mean_intensity')[:]
    
    
    med = np.median(mean_intensity)
    mad = np.median(np.abs(mean_intensity-med))
    #the MAD is releated to sigma by the factor below as explained here:
    #wiki (https://en.wikipedia.org/wiki/Median_absolute_deviation#relation_to_standard_deviation)
    s = mad*1.4826 
    
    #... and since the median should be equal to the mean in a gaussian dist
    # we can use 6 sigma as our threshold
    light_on = mean_intensity >  med + s*6
    
    return light_on

def get_pulses_indexes(light_on, window_size):
    switches = np.diff(light_on.astype(np.int))
    turn_on, = np.where(switches==1)
    turn_off, = np.where(switches==-1)
    
    pulses = dict(
    centre = np.round((turn_on+turn_off)/2),
    before = turn_on - window_size*2,
    after = turn_off + window_size*2,
    )
    return pulses

if __name__ == '__main__':
    
    mask_dir = '/Volumes/behavgenom_archive$/Avelino/screening/Arantza/MaskedVideos'
    
    mask_files = glob.glob(os.path.join(mask_dir, '**', '*.hdf5'), recursive=True)
    
    for mask_file in mask_files:
        light_on = read_light_data(mask_file)
        plt.figure()
        plt.plot(light_on)
    
    
    
#    feat_file = os.path.join(results_dir, base_name + '_features.hdf5')
#    
#    mask_dir = replace_subdir(results_dir, 'Results', 'MaskedVideos')
#    mask_file = os.path.join(mask_dir, base_name +'.hdf5')
    