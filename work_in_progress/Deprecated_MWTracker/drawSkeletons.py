def imFillHoles(im_th):
    #fill holes from (http://www.learnopencv.com/filling-holes-in-an-image-using-opencv-python-c/)
    # Copy the thresholded image.
    im_floodfill = im_th.copy()
     
    # Mask used to flood filling.
    # Notice the size needs to be 2 pixels than the image.
    h, w = im_th.shape[:2]
    mask = np.zeros((h+2, w+2), im_th.dtype)
     
    # Floodfill from point (0, 0)
    cv2.floodFill(im_floodfill, mask, (0,0), 255);
     
    # Invert floodfilled image
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)
     
    # Combine the two images to get the foreground.
    im_out = im_th | im_floodfill_inv
    return im_out

#drawWormContour and writeIndividualMovies are used to create individual worm movies.
def drawWormContour(worm_img, worm_mask, skeleton, cnt_side1, cnt_side2, \
colorpalette = [(119, 158,27 ), (2, 95, 217), (138, 41, 231)]):
    '''
    Draw the worm contour and skeleton. 
    If the contour is not valid, draw the thresholded mask.
    '''
    
    assert worm_img.dtype == np.uint8
    

    max_int = np.max(worm_img)
    
    #the image is likely to be all zeros
    if max_int==0:
        return cv2.cvtColor(worm_img, cv2.COLOR_GRAY2RGB);

    #rescale the intensity range for visualization purposes.
    intensity_rescale = 255./min(1.1*max_int,255.);
    worm_img = (worm_img*intensity_rescale).astype(np.uint8)
            
    worm_rgb = cv2.cvtColor(worm_img, cv2.COLOR_GRAY2RGB);
    if skeleton.size==0 or np.all(np.isnan(skeleton)):
        worm_rgb[:,:,1][worm_mask!=0] = 204
        worm_rgb[:,:,2][worm_mask!=0] = 102
    else:
        pts = np.round(cnt_side1).astype(np.int32)
        cv2.polylines(worm_rgb, [pts], False, colorpalette[1], thickness=1, lineType = 8)
        pts = np.round(cnt_side2).astype(np.int32)
        cv2.polylines(worm_rgb, [pts], False, colorpalette[2], thickness=1, lineType = 8)
        
        pts = np.round(skeleton).astype(np.int32)
        cv2.polylines(worm_rgb, [pts], False, colorpalette[0], thickness=1, lineType = 8)
        
        #mark the head
        cv2.circle(worm_rgb, tuple(pts[0]), 2, (225,225,225), thickness=-1, lineType = 8)
        cv2.circle(worm_rgb, tuple(pts[0]), 3, (0,0,0), thickness=1, lineType = 8)
    
    return worm_rgb


def writeIndividualMovies(masked_image_file, skeletons_file, video_save_dir, 
                          fps=25, bad_seg_thresh = 0.5, save_bad_worms = False):    
    
    '''
        Create individual worms videos.
        
        masked_image_file - hdf5 with the masked videos.
        skeleton_file - file with skeletons and trajectory data previously created by trajectories2Skeletons
        video_save_dir - directory where individual videos are saved
        roi_size - region of interest size.
        fps - frames per second in the individual video.
        bad_seg_thresh - min the fraction of skeletonized frames in the whole trajectory, allowed before being rejected (bad_worm).
        save_bad_worms - (bool flag) if True videos from bad worms are created.
    '''
    
    #extract the base name from the masked_image_file. This is used in the progress status.
    base_name = masked_image_file.rpartition('.')[0].rpartition(os.sep)[-1]
    
    #remove previous data if exists
    if os.path.exists(video_save_dir):
        shutil.rmtree(video_save_dir)
    os.makedirs(video_save_dir)
    if save_bad_worms:
        bad_videos_dir = video_save_dir + 'bad_worms' + os.sep;
        os.mkdir(bad_videos_dir)
    
    #data to extract the ROI
    with pd.HDFStore(skeletons_file, 'r') as ske_file_id:
        trajectories_df = ske_file_id['/trajectories_data']
        skeleton_fracc = trajectories_df[['worm_index_joined', 'has_skeleton']].groupby('worm_index_joined').agg('mean')
        skeleton_fracc = skeleton_fracc['has_skeleton']
        valid_worm_index = skeleton_fracc[skeleton_fracc>=bad_seg_thresh].index
        if not save_bad_worms:
            #remove the bad worms, we do not care about them
            trajectories_df = trajectories_df[trajectories_df['worm_index_joined'].isin(valid_worm_index)]

    with tables.File(skeletons_file, "r") as ske_file_id, tables.File(masked_image_file, 'r') as mask_fid:
        #pointers to masked images dataset
        mask_dataset = mask_fid.get_node("/mask")

        #pointers to skeletons, and contours
        skel_array = ske_file_id.get_node('/skeleton')
        cnt1_array = ske_file_id.get_node('/contour_side1')
        cnt2_array = ske_file_id.get_node('/contour_side2')

        #get first and last frame for each worm
        worms_frame_range = trajectories_df.groupby('worm_index_joined').agg({'frame_number': [min, max]})['frame_number']
        
        video_list = {}
        progressTime = timeCounterStr('Creating individual worm videos.');
        for frame, frame_data in trajectories_df.groupby('frame_number'):
            assert isinstance(frame, (np.int64, int))

            img = mask_dataset[frame,:,:]
            for skeleton_id, row_data in frame_data.iterrows():
                worm_index = row_data['worm_index_joined']
                assert not np.isnan(row_data['coord_x']) and not np.isnan(row_data['coord_y'])

                worm_img, roi_corner = getWormROI(img, row_data['coord_x'], row_data['coord_y'], row_data['roi_size'])

                skeleton = skel_array[skeleton_id,:,:]-roi_corner
                cnt_side1 = cnt1_array[skeleton_id,:,:]-roi_corner
                cnt_side2 = cnt2_array[skeleton_id,:,:]-roi_corner
                
                if not row_data['has_skeleton']:
                    #if it does not have an skeleton get a the thresholded mask
                    worm_mask = _getWormMask(worm_img, row_data['threshold'])
                else:
                    worm_mask = np.zeros(0)
                
                if (worms_frame_range['min'][worm_index] == frame) or (not worm_index in video_list):
                    #if it is the first frame of a worm trajectory initialize a VideoWriter object
                    
                    movie_save_name = video_save_dir + ('worm_%i.avi' % worm_index)
                    if save_bad_worms and not worm_index in valid_worm_index:
                        #if we want to save the 'bad worms', save them in a different directory
                        movie_save_name = bad_videos_dir + ('worm_%i.avi' % worm_index)
                    else:
                        movie_save_name = video_save_dir + ('worm_%i.avi' % worm_index)
                    
                    video_list[worm_index] = cv2.VideoWriter(movie_save_name, \
                    cv2.VideoWriter_fourcc('M','J','P','G'), fps, (row_data['roi_size'], row_data['roi_size']), isColor=True)
                
                #draw contour/mask
                worm_rgb = drawWormContour(worm_img, worm_mask, skeleton, cnt_side1, cnt_side2)
                assert (worm_rgb.shape[0] == worm_img.shape[0]) and (worm_rgb.shape[1] == worm_img.shape[1]) 

                #write video frame
                video_list[worm_index].write(worm_rgb)
            
                #release VideoWriter object if it is the last frame of the trajectory
                if (worms_frame_range['max'][worm_index] == frame):
                    video_list[worm_index].release();
                    video_list.pop(worm_index, None)
            
            #update progress bar
            if frame % 500 == 0:
                progress_str = progressTime.getStr(frame)
                print(base_name + ' ' + progress_str);
                sys.stdout.flush()