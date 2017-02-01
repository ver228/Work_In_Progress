#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 15:06:53 2017

@author: ajaver
"""
import matplotlib.pylab as plt
import cv2
import numpy as np

#video_file = '/Users/ajaver/OneDrive - Imperial College London/Tests/different_animals/fish/b_short.avi'
video_file = '/Users/ajaver/OneDrive - Imperial College London/Tests/different_animals/magots/hodor_ko_l3_control_siamac_1.mjpg'
n_plates = 1


video_file = '/Users/ajaver/OneDrive - Imperial College London/Tests/different_animals/worm_motel/Position5_Ch2_12012017_100957_s.mjpg'
n_plates = 4


vid = cv2.VideoCapture(video_file)
ret, image = vid.read()
if image.ndim == 3:
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
img = cv2.medianBlur(image,51)
#%%

plate_image_ratio = 1/np.sqrt(n_plates);
maxRadius = int((np.min(img.shape)*plate_image_ratio)//2)
dp, min_dist, param1, param2 = 8, maxRadius//3, 200, 500

circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, dp, min_dist, 
                           param1=param1, 
                           param2=param2, 
                           minRadius=maxRadius//2, 
                           maxRadius=maxRadius)

circles = np.uint16(np.around(circles))
circles = np.squeeze(circles, axis=0)
circles = circles[:n_plates, ]

#%%


fig,ax = plt.subplots(1)
ax.set_aspect('equal')
plt.imshow(img, cmap='gray', interpolation='none')

for x, y, r in circles:
    circ = cir = plt.Circle((x, y), r, edgecolor='r', facecolor='none')
    ax.add_patch(circ)

#%%
