# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 16:33:34 2015

@author: ajaver
"""

import os
import sys
from math import sqrt

import cv2
import numpy as np
import tables
from scipy.spatial.distance import cdist
import skimage.filters as skf
import skimage.morphology as skm
from sklearn.utils.linear_assignment_ import linear_assignment  # hungarian algorithm

from MWTracker.analysis.compress.extractMetaData import readAndSaveTimestamp
from MWTracker.helper.timeCounterStr import timeCounterStr
from MWTracker.helper.misc import TABLE_FILTERS

class plate_worms_(tables.IsDescription):
    # class for the pytables
    worm_index_blob = tables.Int32Col(pos=0)
    frame_number = tables.Int32Col(pos=1)
    coord_x = tables.Float32Col(pos=2)
    coord_y = tables.Float32Col(pos=3)
    threshold = tables.Int32Col(pos=4)
    area = tables.Float32Col(pos=5)
    bounding_box_xmin = tables.Int32Col(pos=6)
    bounding_box_xmax = tables.Int32Col(pos=7)
    bounding_box_ymin = tables.Int32Col(pos=8)
    bounding_box_ymax = tables.Int32Col(pos=9)

def _getWormsLocations(worm_cnt, ROI_bbox):
    
    area = float(cv2.contourArea(worm_cnt))
    
    worm_bbox = cv2.boundingRect(worm_cnt)
    bounding_box_xmin = ROI_bbox[0] + worm_bbox[0]
    bounding_box_xmax = bounding_box_xmin + worm_bbox[2]
    bounding_box_ymin = ROI_bbox[1] + worm_bbox[1]
    bounding_box_ymax = bounding_box_ymin + worm_bbox[3]

    # save everything into the the proper output format
    bbox =(bounding_box_xmin, 
                bounding_box_xmax,
                bounding_box_ymin,
                bounding_box_ymax)


    (CMx, CMy), (L, W), angle = cv2.minAreaRect(worm_cnt)
    #adjust CM from the ROI reference frame to the image reference
    CMx += ROI_bbox[0]
    CMy += ROI_bbox[1]


    return area, (CMx, CMy), bbox


def _getBWThreshold(pix_valid):

    # calculate otsu_threshold as lower limit. Otsu understimates the threshold.
    try:
        otsu_thresh = skf.threshold_otsu(pix_valid)
    except:
        return np.nan

    # calculate the histogram
    pix_hist = np.bincount(pix_valid)

    # the higher limit is the most frequent value in the distribution
    # (background)
    largest_peak = np.argmax(pix_hist)
    if otsu_thresh < largest_peak and otsu_thresh + 2 < len(pix_hist) - 1:
        # smooth the histogram to find a better threshold
        pix_hist = np.convolve(pix_hist, np.ones(3), 'same')
        cumhist = np.cumsum(pix_hist)

        xx = np.arange(otsu_thresh, cumhist.size)
        try:
            # the threshold is calculated as the first pixel level above the otsu threshold 
            # at which there would be larger increase in the object area.
            hist_ratio = pix_hist[xx] / cumhist[xx]
            thresh = np.where(
                (hist_ratio[3:] - hist_ratio[:-3]) > 0)[0][0] + otsu_thresh
        except IndexError:
            thresh = np.argmin(
                pix_hist[
                    otsu_thresh:largest_peak]) + otsu_thresh
    else:
        # if otsu is larger than the maximum peak keep otsu threshold
        thresh = otsu_thresh

    return thresh

def _getBufferThresh(ROI_buffer, worm_bw_thresh_factor, is_light_background):
    # calculate threshold using the nonzero pixels.  Using the
    # buffer instead of a single image, improves the threshold
    # calculation, since better statistics are recoverd
    pix_valid = ROI_buffer[ROI_buffer != 0]


    if pix_valid.size > 0:
        if is_light_background:
            thresh = _getBWThreshold(pix_valid)
        else:
            #correct for fluorescence images
            MAX_PIX = 255 #for uint8 images
            thresh = _getBWThreshold(MAX_PIX - pix_valid)
            thresh = MAX_PIX - thresh

        thresh *= worm_bw_thresh_factor
    else:
        thresh = np.nan
    
    return thresh


def _removeExtraBlobs(ROI_image):
    #remove blobs specially in the corners that could be part of other ROI
    # get the border of the ROI mask, this will be used to filter for valid
    # worms
    ROI_valid = (ROI_image != 0).astype(np.uint8)
    _, ROI_border_ind, _ = cv2.findContours(
        ROI_valid, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if len(ROI_border_ind) > 1:
        # consider the case where there is more than one contour in the blob
        # i.e. there is a neighboring ROI in the square, just keep the largest area
        ROI_area = [cv2.contourArea(x) for x in ROI_border_ind]
        valid_ind = np.argmax(ROI_area)
        ROI_valid = np.zeros_like(ROI_valid)
        ROI_valid = cv2.drawContours(ROI_valid, ROI_border_ind, valid_ind, 1, -1)
        ROI_image = ROI_image * ROI_valid

    return ROI_image

def _getBlobMask(ROI_image, thresh, is_light_background):
    # get binary image, 
    if is_light_background:
        ## apply a median filter to reduce rough edges / sharpen the boundary btw worm and background
        ROI_image = cv2.medianBlur(ROI_image, 3)
        ROI_mask = ROI_image < thresh
    else:
        # for fluorescent pharynx labeled images, refine the threshold with a local otsu (http://scikit-image.org/docs/dev/auto_examples/plot_local_otsu.html)
        # this compensates for local variations in brightness in high density regions, when many worms are close to each other
        # as a local threshold introcudes artifacts at the edge of the mask, also use a global threshold to cut these out
        local_otsu = skf.rank.otsu(ROI_image, skm.disk(thresh_block_size))
        thresh = min(local_otsu, thresh)

        ROI_mask = ROI_image>=thresh
        # don't use the blurred image for fluorescent pharynx-labeled images

    ROI_mask = (ROI_mask & (ROI_image != 0)).astype(np.uint8)

    return ROI_mask, thresh




def _getWormContours(ROI_image, 
                    threshold, 
                    strel_size=(5, 5), 
                    is_light_background=True, 
                    thresh_block_size=15):

    ROI_image = _removeExtraBlob(ROI_image)
    ROI_mask, thresh = _getBlobMask(ROI_image, thresh, is_light_background)

    # clean it using morphological closing - make this optional by setting strel_size to 0
    if np.all(strel_size):
        strel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, strel_size)
        ROI_mask = cv2.morphologyEx(ROI_mask, cv2.MORPH_CLOSE, strel)

    # get worms, assuming each contour in the ROI is a worm
    [_, ROI_worms, hierarchy] = cv2.findContours(
        ROI_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    return ROI_worms, hierarchy, thresh


def _getWormFeatures2(
        worm_cnt,
        ROI_image,
        ROI_bbox,
        current_frame,
        thresh,
        min_area):
    
    area = float(cv2.contourArea(worm_cnt))
    worm_bbox = cv2.boundingRect(worm_cnt)
    # find use the best rotated bounding box, the fitEllipse function produces bad results quite often
    # this method is better to obtain an estimate of the worm length than
    # eccentricity
    (CMx, CMy), (L, W), angle = cv2.minAreaRect(worm_cnt)
    #adjust CM from the ROI reference frame to the image reference
    CMx += ROI_bbox[0]
    CMy += ROI_bbox[1]

    if L == 0 or W == 0:
        return None #something went wrong abort
    
    if W > L:
        L, W = W, L  # switch if width is larger than length
    quirkiness = sqrt(1 - W**2 / L**2)

    hull = cv2.convexHull(worm_cnt)  # for the solidity
    solidity = area / cv2.contourArea(hull)
    perimeter = float(cv2.arcLength(worm_cnt, True))
    compactness = 4 * np.pi * area / (perimeter**2)

    # calculate the mean intensity of the worm
    worm_mask = np.zeros(ROI_image.shape, dtype=np.uint8)
    cv2.drawContours(worm_mask, [worm_cnt], 0, 255, -1)
    intensity_mean, intensity_std = cv2.meanStdDev(ROI_image, mask=worm_mask)
    intensity_mean = intensity_mean[0,0]
    intensity_std = intensity_std[0,0]

    # calculate hu moments, they are scale and rotation invariant
    hu_moments = cv2.HuMoments(cv2.moments(worm_cnt))

    
    # save everything into the the proper output format
    mask_feat = (CMx,
                CMy,
                area,
                perimeter,
                L,
                W,
                quirkiness,
                compactness,
                angle,
                solidity,
                intensity_mean,
                intensity_std,
                *hu_moments)

    return mask_feat

def _joinConsecutiveFrames(
        index_list_prev,
        coord,
        coord_prev,
        area,
        area_prev,
        tot_worms,
        max_allowed_dist,
        area_ratio_lim):
    # TODO probably it is better to convert the whole getWormTrajectories
    # function into a class for clearity
    if coord_prev.size != 0:
        costMatrix = cdist(coord_prev, coord)  # calculate the cost matrix
        # costMatrix[costMatrix>MA] = 1e10 #eliminate things that are farther
        # use the hungarian algorithm
        assigment = linear_assignment(costMatrix)

        index_list = np.zeros(coord.shape[0], dtype=np.int)

        # Final assigment. Only allow assigments within a maximum allowed
        # distance, and an area ratio
        for row, column in assigment:
            if costMatrix[row, column] < max_allowed_dist:
                area_ratio = area[column] / area_prev[row]

                if area_ratio > area_ratio_lim[
                        0] and area_ratio < area_ratio_lim[1]:
                    index_list[column] = index_list_prev[row]

        # add a new index if no assigment was found
        unmatched = index_list == 0
        vv = np.arange(1, np.sum(unmatched) + 1) + tot_worms
        if vv.size > 0:
            tot_worms = vv[-1]
            index_list[unmatched] = vv
    else:
        # initialize worm indexes
        index_list = tot_worms + np.arange(1, len(area) + 1)
        tot_worms = index_list[-1]

    index_list = tuple(index_list)
    return index_list, tot_worms


def getWormTrajectories(masked_image_file,
                        trajectories_file,
                        min_area=25,
                        min_box_width=5,
                        max_allowed_dist=20,
                        area_ratio_lim=(0.5, 2),
                        buffer_size=25,
                        worm_bw_thresh_factor=1.,
                        strel_size=(5,5),
                        analysis_type="WORM",
                        thresh_block_size=61):
    '''
    #read images from 'masked_image_file', and save the linked trajectories and their features into 'trajectories_file'
    #use the first 'total_frames' number of frames, if it is equal -1, use all the frames in 'masked_image_file'
    min_area -- min area of the segmented worm
    min_box_width -- min size of the bounding box in the ROI of the compressed image
    max_allowed_dist -- maximum allowed distance between to consecutive trajectories
    area_ratio_lim -- allowed range between the area ratio of consecutive frames
    worm_bw_thresh_factor -- The calculated threshold will be multiplied by this factor. Desperate attempt to solve for the swimming case.
    '''

    
    # intialize variables
    base_name = masked_image_file.rpartition('.')[0].rpartition(os.sep)[-1]
    progressTime = timeCounterStr(base_name + ' Calculating trajectories.')
    

    with tables.File(masked_image_file, 'r') as mask_fid, \
            tables.open_file(trajectories_file, mode='w') as traj_fid:
        
        mask_dataset = mask_fid.get_node("/mask")
        
        plate_worms = traj_fid.create_table('/',
                                            "plate_worms",
                                            plate_worms_,
                                            "Worm feature List",
                                            filters = TABLE_FILTERS)

        
        #find if it is a mask from fluorescence and save it in the new group
        is_light_background = 1 if not 'is_light_background' in mask_dataset._v_attrs \
                            else mask_dataset._v_attrs['is_light_background']
        plate_worms._v_attrs['is_light_background'] = is_light_background

        
        # initialized variables
        tot_worms = 0
        buff_last_coord, buff_last_index, buff_last_area = (np.empty([0]),) * 3

        for frame_number in range(0, mask_dataset.shape[0], buffer_size):

            # load image buffer
            ini = frame_number
            fin = (frame_number+buffer_size)
            image_buffer = mask_dataset[ini:fin, :, :]

            # z projection and select pixels as connected regions that were selected as worms at
            # least once in the masks
            main_mask = np.any(image_buffer, axis=0)

            # change from bool to uint since same datatype is required in
            # opencv
            main_mask = main_mask.astype(np.uint8)

            #calculate the contours, only keep the external contours (no holes) and 
            _, ROI_cnts, hierarchy = cv2.findContours(main_mask, 
                                                      cv2.RETR_EXTERNAL, 
                                                      cv2.CHAIN_APPROX_NONE)

            # examinate each region of interest
            for ROI_cnt in ROI_cnts:
                ROI_bbox = cv2.boundingRect(ROI_cnt)
                # bounding box too small to be a worm - ROI_bbox[2] and [3] are width and height
                if ROI_bbox[2] > min_box_width and ROI_bbox[3] > min_box_width:
                    # select ROI for all buffer slides 
                    ini_x = ROI_bbox[1]
                    fin_x = ini_x + ROI_bbox[3]
                    ini_y = ROI_bbox[0]
                    fin_y = ROI_bbox[2]
                    ROI_buffer = image_buffer[:, ini_x:fin_x, ini_y:fin_y]

                    # caculate threshold
                    if analysis_type == "WORM":
                        # caculate threshold using the values in the buffer this improve quality since there is more data.
                        thresh_buff = _getWormThreshold(pix_valid, worm_bw_thresh_factor, is_light_background)
                    elif analysis_type == "ZEBRAFISH":
                        # Override threshold
                        thresh_buff = 255
                    
                    for buff_ind in range(image_buffer.shape[0]):
                        curr_ROI = ROI_buffer[buff_ind, :, :]

                        # get the contour of possible worms
                        ROI_worms, hierarchy, thresh = _getWormContours(curr_ROI, 
                                                                        thresh_buff, 
                                                                        strel_size, 
                                                                        is_light_background, 
                                                                        thresh_block_size)
                        current_frame = frame_number + buff_ind
                
                        frame_features = []
                        for worm_ind, worm_cnt in enumerate(ROI_worms):
                            # ignore contours from holes. This shouldn't occur with the flag RETR_EXTERNAL
                            if hierarchy[0][worm_ind][3] != -1:
                                continue

                            # obtain features for each worm
                            area, CM, blob_bbox = _getWormsLocations(worm_cnt,
                                                                ROI_buffer[buff_ind, :, :],
                                                                ROI_bbox,
                                                                thresh,
                                                                min_area)
                            if area >= min_area:
                                # append data to pytables
                                row = (-1, current_frame, *CM, thresh, area, *blob_bbox)
                                plate_worms.append(row)     
           
            if frame_number % 1000 == 0:
                traj_fid.flush()

            if frame_number % 500 == 0:
                # calculate the progress and put it in a string
                progress_str = progressTime.getStr(frame_number)
                print(base_name + ' ' + progress_str)
                sys.stdout.flush()
        # flush any remaining and create indexes
        plate_worms.flush()
        plate_worms.cols.frame_number.create_csindex()  # make searches faster
        plate_worms.cols.worm_index_blob.create_csindex()
        plate_worms.flush()

    readAndSaveTimestamp(masked_image_file, trajectories_file)
    with tables.open_file(trajectories_file, mode='r+') as traj_fid:
        # flag used to determine if the function finished correctly
        traj_fid.get_node('/plate_worms')._v_attrs['has_finished'] = 1

    print(base_name + ' ' + progress_str)
    sys.stdout.flush()
