# -*- coding: utf-8 -*-
"""
Created on Fri May 27 14:01:37 2016

@author: ajaver
"""

import numpy as np
import matplotlib.pylab as plt
import tifffile
import os
import glob

main_dir = '/Users/ajaver/Desktop/OMG2 short - larvae - compression test/'

files = sorted(glob.glob(os.path.join(main_dir, '*.dat')))

#the files name contains the image number as an inverted string 6100000000 -> 0000000016
dat_order = [int(os.path.split(x)[1].partition('spool')[0][::-1]) for x in files]
tot_img_decoded = max(dat_order) + 1

tif_file = main_dir + 'OMG2 short TIFF 16 bit.tiff'
img_tif = tifffile.imread(tif_file)

#I cannot initialize yet since i do not have the image size
all_decoded = np.zeros(0)

files = ['/Users/ajaver/Downloads/0000010000spool.dat']
tot_img_decoded = len(files)
for img_n, fname in enumerate(files):
    bin_dat = np.fromfile(fname, np.uint8)
    
    #It seems that the last 40 bytes of the file are the header (it contains zeros and the size of the image 2080*2156)
    header = bin_dat[-40:].astype(np.uint16)
    header =  np.left_shift(header[1::2], 8) + header[0::2]
    im_size = header[14:16]
    
    if all_decoded.size == 0:
        all_decoded = np.zeros((tot_img_decoded, im_size[1], im_size[0]), np.uint16)
    
    #every 3 bytes will correspond two pixel levels.
    D1 = bin_dat[:-40:3]
    D2 = bin_dat[1:-40:3]
    D3 = bin_dat[2:-40:3]
    
    #and this pixel combination seems to work to recreated the desire intensities
    #1 and 3 represent the higher bits of the pixel intensity, while the second is divided as the lower bits.
    D1s = np.left_shift(D1.astype(np.uint16), 4) + np.bitwise_and(D2,15)
    D3s = np.left_shift(D3.astype(np.uint16), 4) + np.right_shift(D2,4)
    
    #the pixels seemed to be organized in this order
    image_decoded = np.zeros(im_size[::-1], np.uint16)
    image_decoded[::-1, -2::-2] = D3s.reshape((im_size[1], -1))
    image_decoded[::-1, ::-2] = D1s.reshape((im_size[1], -1))
    
    #let's save the decoded image in the correct order from the file name
    all_decoded[dat_order[img_n]] = image_decoded

assert np.all(all_decoded == img_tif)
#%%
if True:
    #plt.figure()
    #plt.imshow(img_tif[img_n], interpolation='none', cmap='gray')
    plt.figure()
    plt.imshow(image_decoded, interpolation='none', cmap='gray')
    
    #%%
    #dd = image_decoded.astype(np.double)-img_tif[1].astype(np.double)
    #print(np.unique(dd))
    
    #if np.any(dd!=0):
    #    plt.figure()
    #    plt.imshow(dd, interpolation='none')
               
#%%
#for i_tif, img_t in enumerate(img_tif):
#    for i_dec, img_d in enumerate(all_decoded):
#        dd = img_d.astype(np.double)-img_t.astype(np.double)
#        if np.all(dd == 0):
#            print(i_tif, i_dec)

