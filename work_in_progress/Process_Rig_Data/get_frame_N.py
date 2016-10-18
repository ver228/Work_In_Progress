# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import tables
import time

"C:\Program Files\Anaconda3\Lib\site-packages\tables\scripts"

TABLE_FILTERS = tables.Filters(
        complevel=5,
        complib='zlib',
        shuffle=True,
        fletcher32=True)

volumes = ['R:', 'S:', 'T:'][1:2]
input_subdir = 'Test'
output_dir = 'D:\\Test_14102016\\'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


exp_prefix = 'N2_Adult_Test'

for ivol, vol in enumerate(volumes):
    dat_dir = os.path.join(vol, input_subdir)
    
    for fname in os.listdir(dat_dir):
        fullname = os.path.join(dat_dir, fname)
            
        remain = fname.split('_')[-3:]
        channel_n = int(remain[0][2]) + ivol*2
        timestamp = '_'.join(remain[1:])
        
        newfname = '{}_Ch{}_{}'.format(exp_prefix, channel_n, timestamp)
        newfullname = os.path.join(output_dir, newfname)
        print(newfname)
        
        with tables.File(fullname, 'r') as fid_old, \
            tables.File(newfullname, 'w') as fid_new:
            mask_old = fid_old.get_node('/mask')

            tot_frames, im_height, im_width = mask_old.shape

            mask_new = fid_new.create_carray(
                "/", "mask",
                tables.UInt8Atom(),
                (tot_frames, im_height, im_width),
                chunkshape = (1, im_height, im_width),
                filters=TABLE_FILTERS)
            
            tic = time.time()
            for n in range(tot_frames):
                mask_new[n] = mask_old[n]
                if n % 500 == 0:
                    print(n,tot_frames, time.time() - tic)
                    tic = time.time()
                    
        break
        
