import cv2
import tables
import numpy as np

from tierpsy.analysis.compress.BackgroundSubtractor import BackgroundSubtractor
from tierpsy.analysis.traj_create.getBlobTrajectories import _cnt_to_ROIs, getBufferThresh, getBlobContours
from tierpsy.analysis.ske_create.helperIterROI import getAllImgROI

from tierpsy.helper.timeCounterStr import timeCounterStr
from tierpsy.helper.misc import print_flush

def generateImages(masked_image_file, frames=[], bgnd_params = {}):
    
    if len(bgnd_params)==0:
        bgnd_subtractor = None
    else:
        bgnd_subtractor = BackgroundSubtractor(masked_image_file, **bgnd_params)
    
    with tables.File(masked_image_file, 'r') as mask_fid:
        mask_dataset = mask_fid.get_node("/mask")
        
        if len(frames) == 0:
            frames = range(mask_dataset.shape[0])
        
        for frame_number in frames:
            image = mask_dataset[frame_number]
            
            if bgnd_subtractor is not None:
                image_b  = bgnd_subtractor.apply(image, last_frame=frame_number)
                #image_buffer_b = 255 - image_buffer_b
                image_b[image==0] = 0
                image = image_b
            
            yield frame_number, image



def generateROIBuff(masked_image_file, buffer_size, img_generator):
    
    with tables.File(masked_image_file, 'r') as mask_fid:
        tot_frames, im_h, im_w = mask_fid.get_node("/mask").shape
        
    
    for frame_number, image in img_generator:
        if frame_number % buffer_size == 0:
            if frame_number + buffer_size > tot_frames:
                buffer_size = tot_frames-frame_number #change this value, otherwise the buffer will not get full
            image_buffer = np.zeros((buffer_size, im_h, im_w), np.uint8)
            ini_frame = frame_number            
        
        
        image_buffer[frame_number-ini_frame] = image
        
        #compress if it is the last frame in the buffer
        if (frame_number-1) % buffer_size == 0 or (frame_number+1 == tot_frames):
            # z projection and select pixels as connected regions that were selected as worms at
            # least once in the masks
            main_mask = np.any(image_buffer, axis=0)
    
            # change from bool to uint since same datatype is required in
            # opencv
            main_mask = main_mask.astype(np.uint8)
    
            #calculate the contours, only keep the external contours (no holes) and 
            _, ROI_cnts, _ = cv2.findContours(main_mask, 
                                                cv2.RETR_EXTERNAL, 
                                                cv2.CHAIN_APPROX_NONE)
    
            yield ROI_cnts, image_buffer, frame_number

def generateMoviesROI(masked_file, 
                    trajectories_data,
                    roi_size = -1, 
                    progress_prefix = '',
                    progress_refresh_rate_s=20):

    if len(trajectories_data) == 0:
        print_flush(progress_prefix + ' No valid data. Exiting.')
        
    else:
        traj_group_by_frame = trajectories_data.groupby('frame_number')
        
        progress_time = timeCounterStr(progress_prefix)
        
        
        with tables.File(masked_file, 'r') as fid:

            try:
                expected_fps = fid.get_node('/', 'mask')._v_attrs['expected_fps']
            except:
                expected_fps = 25
            progress_refresh_rate = expected_fps*progress_refresh_rate_s


            img_data = fid.get_node('/mask')
            for ii, (current_frame, frame_data) in enumerate(traj_group_by_frame):
                img = img_data[current_frame]
                
                #dictionary where keys are the table row and the values the worms ROIs
                yield getAllImgROI(img, frame_data, roi_size)
                
                if current_frame % progress_refresh_rate == 0:
                    print_flush(progress_time.getStr(current_frame))
                
            print_flush(progress_time.getStr(current_frame))

if __name__ == '__main__':
    masked_image_file = '/Users/ajaver/OneDrive - Imperial College London/Tests/different_animals/swimming/MaskedVideos/trp-4_N5_F1--_Set1_Pos4_Ch4_07022017_121132.hdf5'
    #masked_image_file = '/Users/ajaver/OneDrive - Imperial College London/Tests/different_animals/swimming/MaskedVideos/unc-9_N5_F1--_Set1_Pos4_Ch6_07022017_121217.hdf5'
    #masked_image_file = '/Users/ajaver/OneDrive - Imperial College London/Tests/different_animals/fish/MaskedVideos/c_short_pigmented.hdf5'
    
    
    is_light_background = True
    bgnd_params = dict(buff_size = 50, frame_gap = 13, is_light_background=is_light_background)
    
    
    buffer_size = 30
    min_box_width = 25
    strel_size = (5,5)
    worm_bw_thresh_factor = 1.0
    
    analysis_type = 'WORM'#'WORM'
    
    
    img_generator = generateImages(masked_image_file, bgnd_params)
    generator = generateROIBuff(masked_image_file, buffer_size, img_generator)
    
    
    
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