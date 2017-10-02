import numpy as np
import cv2
import os
import matplotlib.pylab as plt


#video_file = '/Users/ajaver/OneDrive - Imperial College London/Tests/different_animals/fish/a_short.avi'
#video_file = '/Users/ajaver/OneDrive - Imperial College London/Tests/different_animals/worm_motel/Position5_Ch2_12012017_100957_s.mjpg'
#video_file = '/Users/ajaver/OneDrive - Imperial College London/Tests/different_animals/worm_motel/Position6_Ch1_12012017_102810_s.mjpg'
#video_file = '/Users/ajaver/OneDrive - Imperial College London/Tests/different_animals/worm_motel/Position6_Ch2_12012017_102810_s.mjpg'
#video_file = '/Users/ajaver/OneDrive - Imperial College London/Tests/different_animals/maggots/hodor_ko_l3_control_siamac_all.mjpg'
#video_file = '/Users/ajaver/OneDrive - Imperial College London/Tests/different_animals/swimming/unc-9_N5_F1--_Set1_Pos4_Ch6_07022017_121217.mjpg'
video_file = '/Users/ajaver/OneDrive - Imperial College London/Tests/different_animals/maggots/MaskedVideos/w1118_l3_control_siamak_all.hdf5'

b_subtractor = BackgroundSubstractor(video_file)
vid = selectVideoReader(video_file)
while(1):
    ret, image = vid.read()
    if ret == 0:
        break
    if image.ndim == 3:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    fgmask = b_subtractor.appy(image)

    scale = tuple(x//2 for x in fgmask.shape[:2][::-1])
    fgmask = cv2.resize(fgmask, scale)

    top=np.max(fgmask)
    bot=np.min(fgmask)
    norm_image = (fgmask-bot)/(top-bot)

    norm_image = norm_image.T
    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    cv2.imshow('frame',norm_image)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
vid.release()
cv2.destroyAllWindows()

#fgbg = cv2.bgsegm.createBackgroundSubtractorMOG(backgroundRatio=0.9)
#
#tot_frames_init = 100
#n_step = 9
#ret = 1
#
#vid = selectVideoReader(video_file)
#frame_n = 0
#while ret>0 and (frame_n < (tot_frames_init*n_step)):
#	ret, frame = vid.read()
#	frame_n += 1
#	if (frame_n % n_step) == 0:
#		fgbg.apply(frame)
#		print(frame_n)
#
#vid.release()
#
#
#vid = selectVideoReader(video_file)
#while(1):
#	ret, frame = vid.read()
#	fgmask = fgbg.apply(frame)
#	scale = tuple(x//2 for x in fgmask.shape[:2])
#	fgmask = cv2.resize(fgmask, scale)
#	cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
#	cv2.imshow('frame',fgmask)
#	k = cv2.waitKey(30) & 0xff
#	if k == 27:
#		break
#vid.release()
#cv2.destroyAllWindows()