import tables
import pandas as pd

from tierpsy.analysis.compress.BackgroundSubtractor import BackgroundSubtractor
from tierpsy.analysis.ske_create.helperIterROI import getAllImgROI
from tierpsy.analysis.traj_create.getBlobTrajectories import _cnt_to_ROIs, getBufferThresh, getBlobContours


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


def generateMoviesROI(masked_file, 
                    trajectories_data,
                    bgnd_params={},
                    roi_size = -1, 
                    progress_prefix = '',
                    progress_refresh_rate_s=20):

    if len(trajectories_data) == 0:
        print_flush(progress_prefix + ' No valid data. Exiting.')
        
    else:
        frames = trajectories_data['frame_number'].unique()
        img_generator = generateImages(masked_image_file, frames=frames, bgnd_params=bgnd_params)
        
        traj_group_by_frame = trajectories_data.groupby('frame_number')
        progress_time = timeCounterStr(progress_prefix)
        with tables.File(masked_file, 'r') as fid:
            try:
                expected_fps = fid.get_node('/', 'mask')._v_attrs['expected_fps']
            except:
                expected_fps = 25
            progress_refresh_rate = expected_fps*progress_refresh_rate_s


        for ii, (current_frame, img) in enumerate(img_generator):
            frame_data = traj_group_by_frame.get_group(current_frame)
            
            #dictionary where keys are the table row and the values the worms ROIs
            yield getAllImgROI(img, frame_data, roi_size)
            
            if current_frame % progress_refresh_rate == 0:
                print_flush(progress_time.getStr(current_frame))
            
        print_flush(progress_time.getStr(current_frame))

if __name__ == '__main__':
    #masked_image_file = '/Users/ajaver/OneDrive - Imperial College London/Tests/different_animals/swimming/MaskedVideos/trp-4_N5_F1--_Set1_Pos4_Ch4_07022017_121132.hdf5'
    #masked_image_file = '/Users/ajaver/OneDrive - Imperial College London/Tests/different_animals/swimming/MaskedVideos/unc-9_N5_F1--_Set1_Pos4_Ch6_07022017_121217.hdf5'
    masked_image_file = '/Users/ajaver/OneDrive - Imperial College London/Tests/different_animals/fish/MaskedVideos/c_short_pigmented.hdf5'
    
    
    skeletons_file = masked_image_file.replace('MaskedVideos', 'Results').replace('.hdf5', '_skeletons.hdf5')
    
    is_light_background = True
    bgnd_params = dict(buff_size = 50, frame_gap = 13, is_light_background=is_light_background)
    
    
    buffer_size = 30
    min_box_width = 25
    strel_size = (5,5)
    worm_bw_thresh_factor = 1.0
    
    analysis_type = 'WORM'#'WORM'
    
    
    with pd.HDFStore(skeletons_file, 'r') as fid:
        trajectories_data = fid['/trajectories_data']
    
    roi_generator = generateMoviesROI(masked_image_file, trajectories_data, bgnd_params)
    
    output = next(roi_generator)
    #%%
    import matplotlib.pylab as plt
    for irow, (worm_roi, roi_corner) in output.items():
        thresh_buff = getBufferThresh(worm_roi, worm_bw_thresh_factor, not is_light_background, analysis_type)
        
        plt.figure()
        plt.imshow(worm_roi, interpolation='none', cmap='gray')
        
    #%%
    
#    ROI_cnts, image_buffer_b, frame_number = output
#    import matplotlib.pylab as plt
#    
#    #plt.figure()
#    #plt.imshow(image_buffer_b[0], interpolation='none', cmap='gray')
#    
#    min_box_width = 25
#    for ROI_cnt in ROI_cnts:
#        ROI_buffer, _ = _cnt_to_ROIs(ROI_cnt, image_buffer_b, min_box_width)
#        thresh_buff = getBufferThresh(ROI_buffer, worm_bw_thresh_factor, not is_light_background, analysis_type)
#        
#        if ROI_buffer is not None:
#            curr_ROI = ROI_buffer[0]
#            
#            ROI_worms, hierarchy = getBlobContours(curr_ROI, 
#                                                    thresh_buff, 
#                                                    strel_size, 
#                                                    not is_light_background,
#                                                    analysis_type, 
#                                                    -1)
#            
#            plt.figure()
#            plt.imshow(curr_ROI, interpolation='none', cmap='gray')
#            
#            for cnt in ROI_worms:
#                xx = cnt[:,:,0].squeeze()
#                yy = cnt[:,:,1].squeeze()
#                plt.plot(xx,yy)