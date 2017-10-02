import cv2
import tables
import numpy as np

from tierpsy.analysis.compress.BackgroundSubtractor import BackgroundSubtractor
from tierpsy.analysis.traj_create.getBlobTrajectories import \
_cnt_to_ROIs, getBufferThresh, getBlobContours, generateImages, generateROIBuff



if __name__ == '__main__':
    #masked_image_file = '/Users/ajaver/OneDrive - Imperial College London/Tests/different_animals/swimming/MaskedVideos/trp-4_N5_F1--_Set1_Pos4_Ch4_07022017_121132.hdf5'
    #masked_image_file = '/Users/ajaver/OneDrive - Imperial College London/Tests/different_animals/swimming/MaskedVideos/unc-9_N5_F1--_Set1_Pos4_Ch6_07022017_121217.hdf5'
    masked_image_file = '/Users/ajaver/OneDrive - Imperial College London/Tests/different_animals/fish/MaskedVideos/c_short_pigmented.hdf5'
    masked_image_file = '/Users/ajaver/OneDrive - Imperial College London/Tests/different_animals/fish/MaskedVideos/a_short.hdf5'
    
    is_light_background = True
    bgnd_params = dict(buff_size = 500, frame_gap = 1, is_light_background=is_light_background)
    
    
    buffer_size = 30
    min_box_width = 25
    strel_size = (5,5)
    worm_bw_thresh_factor = 1
    
    analysis_type = 'WORM'#'WORM'
    
    
    
    generator = generateROIBuff(masked_image_file, buffer_size, bgnd_params)
    
    
    
    output = next(generator)
    
    #%%
    
    ROI_cnts, image_buffer_b, frame_number = output
    import matplotlib.pylab as plt
    
    #plt.figure()
    #plt.imshow(image_buffer_b[0], interpolation='none', cmap='gray')
    
    min_box_width = 25
    for ROI_cnt in ROI_cnts:
        ROI_buffer, _ = _cnt_to_ROIs(ROI_cnt, image_buffer_b, min_box_width)
        thresh_buff = getBufferThresh(ROI_buffer, worm_bw_thresh_factor, not is_light_background, analysis_type)
        print(thresh_buff)
        
        if ROI_buffer is not None:
            curr_ROI = ROI_buffer[0]
            
            ROI_worms, hierarchy = getBlobContours(curr_ROI, 
                                                    thresh_buff, 
                                                    strel_size, 
                                                    not is_light_background,
                                                    analysis_type, 
                                                    -1)
            
            plt.figure()
            plt.imshow(curr_ROI, interpolation='none', cmap='gray')
            
            for cnt in ROI_worms:
                xx = cnt[:,:,0].squeeze()
                yy = cnt[:,:,1].squeeze()
                plt.plot(xx,yy)