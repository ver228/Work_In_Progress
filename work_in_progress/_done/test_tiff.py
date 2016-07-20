# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 14:50:24 2015

@author: ajaver
"""

tiff_file = os.path.splitext(masked_image_file)[0] + '_full.tiff';
reduce_fractor = 8
mask_fid = h5py.File(masked_image_file, "r");

expected_size = int(np.floor(mask_fid["/mask"].shape[0]/float(mask_fid["/full_data"].attrs['save_interval']) + 1));
if expected_size > mask_fid["/full_data"].shape[0]: 
    expected_size = mask_fid["/full_data"].shape[0]
expected_size = 8

im_size = tuple(np.array(mask_fid["/full_data"].shape[1:])/reduce_fractor)

I_worms = np.zeros((expected_size, im_size[0],im_size[1]), dtype = np.uint8)

for frame in range(expected_size):
    I_worms[frame, :,:] = cv2.resize(mask_fid["/full_data"][0,:,:], im_size);

#fi.write_multipage(I_worms, tiff_file, fi.IO_FLAGS.TIFF_LZW)
tifffile.imsave(tiff_file, I_worms)