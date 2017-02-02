#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 15:06:53 2017

@author: ajaver
"""
import matplotlib.pylab as plt
import cv2
import numpy as np
import os
import glob

def find_plates(image, n_plates):
    plate_image_ratio = 1/np.sqrt(n_plates);
    maxRadius = int((np.min(image.shape)*plate_image_ratio)//2)
    dp, min_dist, param1, param2 = 8, maxRadius//3, 200, 500
    

    
    circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, dp, min_dist, 
                               param1=param1, 
                               param2=param2, 
                               minRadius=maxRadius//2, 
                               maxRadius=maxRadius)
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        circles = np.squeeze(circles, axis=0)
        circles = circles[:n_plates, ]
    return circles, maxRadius

if __name__ == '__main__':
    video_dir = '/Users/ajaver/OneDrive - Imperial College London/Tests/different_animals/worm_motel/'
    n_plates = 4
    
    #video_dir = '/Users/ajaver/OneDrive - Imperial College London/Tests/different_animals/'
    n_plates = 1
    
    
    fnames = glob.glob(os.path.join(video_dir, '**'), recursive=True)
    
    #fnames = glob.glob('/Volumes/behavgenom_archive$/RigRawVideos/**', recursive=True)
    fnames = glob.glob('/Volumes/behavgenom_archive$/Tests/Data/**', recursive=True)
    
    
    fnames = [x for x in fnames if any(x.endswith(ext) for ext in ['.avi', '.mjpg'])]
    
    for video_file in fnames:
        vid = cv2.VideoCapture(video_file)
        if not vid.isOpened():
            continue
        
        ret, image = vid.read()
        if image.ndim == 3:
            image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        circles, maxRadius = find_plates(image, n_plates)
        
#        blur_size = maxRadius//20
#        if blur_size%2 == 0:
#            blur_size += 1
#        img_blurred = cv2.medianBlur(image,blur_size)
        
        fig,ax = plt.subplots(1)
        ax.set_aspect('equal')
        plt.imshow(image, cmap='gray', interpolation='none')
        if circles is not None:
            for x, y, r in circles:
                circ = cir = plt.Circle((x, y), r, edgecolor='r', facecolor='none')
                ax.add_patch(circ)
