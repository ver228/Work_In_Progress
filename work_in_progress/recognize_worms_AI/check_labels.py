#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 16:40:14 2016

@author: ajaver
"""

import tables
import numpy as np
import pandas as pd
import pickle
import gzip
#from sklearn import cross_validation

all_samples_file = '/Users/ajaver/OneDrive - Imperial College London/training_data/worm_ROI_samplesI.hdf5'


with pd.HDFStore(all_samples_file) as fid:
    sample_data = fid['/sample_data']

valid_data = sample_data.loc[sample_data['label_id']>0]
print(valid_data['label_id'].value_counts())

label_id = valid_data['label_id'].values
is_worms = valid_data['label_id'].isin([2,3,4]).values.astype(np.uint8)



with tables.File(all_samples_file, 'r') as fid:
    d = (40, 120)
    
    masks = fid.get_node('/', 'mask')[valid_data.index, d[0]:d[1], d[0]:d[1]]
    full_data = fid.get_node('/', 'full_data')[valid_data.index, d[0]:d[1], d[0]:d[1]]
#%%
new_dim = (masks.shape[0], masks.shape[1]*masks.shape[2])

masks = masks.reshape(new_dim)
full_data = full_data.reshape(new_dim)
    
#%%
tot_samples = full_data.shape[0]

all_ind = np.random.permutation(tot_samples)



test_size = 1000
val_size = 1000

test_ind = all_ind[:test_size]
val_ind = all_ind[test_size:(val_size+test_size)]
train_ind = all_ind[(val_size+test_size):]


sample_data = [(masks[x], is_worms[x]) for x in [train_ind, val_ind, test_ind]]


with gzip.open( "sample.pkl.gz", "wb" ) as fid:
    pickle.dump( sample_data,  fid)
#%%
with gzip.open( "sample.npz.gz", "wb" ) as fid:
    pickle.dump( sum(map(list, sample_data), []),  fid)


    


#%%
#import matplotlib.pylab as plt
#
#import numpy as np
#
#for ii in np.where(~is_worms)[0][100:110]:
#    plt.figure()
#    plt.imshow(masks[ii])