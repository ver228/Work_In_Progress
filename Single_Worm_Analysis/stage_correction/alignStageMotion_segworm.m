%function alignStageMotion(masked_image_file,skeletons_file, is_swimming)

main_dir = '/Users/ajaver/Desktop/Videos/single_worm/agar_goa/MaskedVideos/';
results_dir = strrep(main_dir, 'MaskedVideos', 'Results');
feat_dir = strrep(main_dir, 'MaskedVideos', 'Features');

is_swimming = false;



files = dir(main_dir);
for iif = 1:numel(files)
    %
    file = files(iif);
    if isempty(regexp(file.name, '\w*.hdf5', 'ONCE'))
        continue
    end
    fprintf('%i) %s\n', iif, file.name)
    masked_image_file = fullfile(main_dir, file.name);
    skeletons_file = fullfile(results_dir, strrep(file.name, '.hdf5', '_skeletons.hdf5'));
    features_mat = fullfile(feat_dir, strrep(file.name, '.hdf5', '_features.mat'));
    %}
    %{
    masked_image_file = files{iif};
    skeletons_file = strrep(strrep(files{iif}, main_dir, results_dir), '.hdf5', '_skeletons.hdf5');
    features_mat = strrep(strrep(files{iif}, main_dir, feat_dir), '.hdf5', '_features.hdf5');
    %}
    %%
    clear is_stage_move movesI stage_locations
    %% read time stamps. I should put this data into the masked files dir
    video_timestamp_ind = h5read(skeletons_file, '/timestamp/raw');
    video_timestamp_ind = video_timestamp_ind + 1; %correct for python indexing
    
    if any(isnan(video_timestamp_ind))
        disp('The timestamp is corrupt or do not exist')
        continue
    end
    
    video_timestamp_time = h5read(skeletons_file, '/timestamp/time');
    fps = 1/median(diff(video_timestamp_time));
    
    %% Open the information file and read the tracking delay time.
    % (help from segworm findStageMovement)
    % 2. The info file contains the tracking delay. This delay represents the
    % minimum time between stage movements and, conversely, the maximum time it
    % takes for a stage movement to complete. If the delay is too small, the
    % stage movements become chaotic. We load the value for the delay.
    
    xml_info = h5read(masked_image_file, '/xml_info');
    %this is not the cleaneast but matlab does not have a xml parser from
    %text string
    dd = strsplit(xml_info, '<delay>');
    dd = strsplit(dd{2}, '</delay>');
    delay_str = dd{1};
    delay_time = str2double(delay_str) / 1000;
    delay_frames = ceil(delay_time * fps);
    
    %% Read the media times and locations from the log file.
    % (help from segworm findStageMovement)
    % 3. The log file contains the initial stage location at media time 0 as
    % well as the subsequent media times and locations per stage movement. Our
    % algorithm attempts to match the frame differences in the video (see step
    % 1) to the media times in this log file. Therefore, we load these media
    % times and stage locations.
    %from the .log.csv file
    stage_data = h5read(masked_image_file, '/stage_data');
    mediaTimes = stage_data.stage_time';%*60;
    locations = [stage_data.stage_x , stage_data.stage_y];
    
    %% Read the scale conversions, we would need this when we want to convert the pixels into microns
    micronsPerPixelX = 1/h5readatt(masked_image_file, '/mask', 'pixels2microns_x');
    micronsPerPixelY = 1/h5readatt(masked_image_file, '/mask', 'pixels2microns_y');
    
    normScale = sqrt((micronsPerPixelX ^ 2 + micronsPerPixelY ^ 2) / 2);
    micronsPerPixelScale =  normScale * [sign(micronsPerPixelX) sign(micronsPerPixelY)];
    
    % Compute the rotation matrix.
    %rotation = 1;
    angle = atan(micronsPerPixelY / micronsPerPixelX);
    if angle > 0
        angle = pi / 4 - angle;
    else
        angle = pi / 4 + angle;
    end
    cosAngle = cos(angle);
    sinAngle = sin(angle);
    rotation_matrix = [cosAngle, -sinAngle; sinAngle, cosAngle];
    
    %% calculate the variance of the difference between frames
    % Ev's code uses the full vectors without dropping frames
    % 1. video2Diff differentiates a video frame by frame and outputs the
    % differential variance. We load these frame differences.
    frame_diffs_d = getFrameDiffVar(masked_image_file);
    
    %% The shift makes everything a bit more complicated. I have to remove the first frame, before resizing the array considering the dropping frames.
    
    if numel(video_timestamp_ind) > numel(frame_diffs_d) + 1
        %i can tolerate one frame (two with respect to the frame_diff)
        %extra at the end of the timestamp
        video_timestamp_ind = video_timestamp_ind(1:numel(frame_diffs_d)+1);
    end
    
    frame_diffs = nan(1, max(video_timestamp_ind)-1);
    dd = video_timestamp_ind-min(video_timestamp_ind);
    dd = dd(dd>0);
    if numel(frame_diffs_d) ~= numel(dd)
        continue
    end
    frame_diffs(dd) = frame_diffs_d;
    
    %%
    
    try
        clear is_stage_move movesI stage_locations
        [is_stage_move, movesI, stage_locations] = findStageMovement_ver2(frame_diffs, mediaTimes, locations, delay_frames, fps);
        
    catch ME
        fprintf('%i) %s\n', iif, masked_image_file)
        disp(ME)
        
        is_stage_move = ones(numel(frame_diffs)+1, 1);
        stage_locations = [];
        movesI = [];
    end
    %%
    stage_vec = nan(numel(is_stage_move),2);
    if numel(movesI) == 2 && all(movesI==0)
        %there was no movements
        stage_vec(:,1) = stage_locations(1);
        stage_vec(:,2) = stage_locations(2);
        
    else
        %convert output into a vector that can be added to the skeletons file to obtain the real worm displacements
        
        for kk = 1:size(stage_locations,1)
            bot = max(1, movesI(kk,2)+1);
            top = min(numel(is_stage_move), movesI(kk+1,1)-1);
            stage_vec(bot:top, 1) = stage_locations(kk,1);
            stage_vec(bot:top, 2) = stage_locations(kk,2);
        end
    end
    
    %the nan values must match the spected video motions
    assert(all(isnan(stage_vec(:,1)) == is_stage_move))
    
    %prepare vectors to save into the hdf5 file.
    %Go back to the original movie indexing. I do not want to include the missing frames at this point.
    frame_diffs_d = frame_diffs_d';
    is_stage_move_d = int8(is_stage_move(video_timestamp_ind))';
    
    
    %% change into a format that i can add directly to the skeletons in skeletons_file
    stage_vec_d = stage_vec(video_timestamp_ind, :);
    
    
    %stage_vec_d(:,1) = stage_vec_d(:,1)*pixels2microns_y;
    %stage_vec_d(:,2) = stage_vec_d(:,2)*pixels2microns_x;
    stage_vec_d = stage_vec_d';
    
    
    %%
    %
    %{
        load(features_mat)
        seg_motion = info.video.annotations.frames==2;
        plot(worm.posture.skeleton.x(:, 1:15:end), worm.posture.skeleton.y(:, 1:15:end))
        if (all(seg_motion==is_stage_move_d))
            disp('Segworm and this code have the same frame aligment.')
        end
    %}
    %{
        skeletons = h5read(skeletons_file, '/skeleton');
        
        skeletons_mu = nan(size(skeletons));
        
        for kk = 1:size(skeletons_mu,3)
            pixels = skeletons(:, :, kk)';
            origin = stage_vec_d(:,kk);
            % Rotate the pixels.
            pixels = (rotation_matrix * pixels')';

            % Convert the pixels coordinates to micron locations.
            microns(:,1) = origin(1) - pixels(:,1) * micronsPerPixelScale(1);
            microns(:,2) = origin(2) - pixels(:,2) * micronsPerPixelScale(2);
            skeletons_mu(:,:,kk) = microns';
        end
        
        
        skel_x = squeeze(skeletons_mu(1,:,:));
        skel_y = squeeze(skeletons_mu(2,:,:));
        
        figure, hold on
        %plot(worm.posture.skeleton.x(25,:))
        plot(skel_x(25,1:400))
        
        figure
        plot(squeeze(skel_x(25,:)))
        
        figure
        plot(skel_x(:, 1:15:end), skel_y(:, 1:15:end))
        
    %}
    
    %%
    %this removes crap from previous analysis
    %%save stage vector
    fid = H5F.open(skeletons_file,'H5F_ACC_RDWR','H5P_DEFAULT');
    if H5L.exists(fid,'/stage_vec','H5P_DEFAULT')
        H5L.delete(fid,'/stage_vec','H5P_DEFAULT');
    end
    
    if H5L.exists(fid,'/is_stage_move','H5P_DEFAULT')
        H5L.delete(fid,'/is_stage_move','H5P_DEFAULT');
    end
    H5F.close(fid);
    
    
    %% delete data from previous analysis if any
    fid = H5F.open(skeletons_file,'H5F_ACC_RDWR','H5P_DEFAULT');
    if H5L.exists(fid,'/stage_movement','H5P_DEFAULT')
        gid = H5G.open(fid, '/stage_movement');
        if H5L.exists(gid,'stage_vec','H5P_DEFAULT')
            H5L.delete(gid,'stage_vec','H5P_DEFAULT');
        end
        
        if H5L.exists(gid,'is_stage_move','H5P_DEFAULT')
            H5L.delete(gid,'is_stage_move','H5P_DEFAULT');
        end
        
        if H5L.exists(gid,'frame_diff','H5P_DEFAULT')
            H5L.delete(gid,'frame_diff','H5P_DEFAULT');
        end
        H5L.delete(gid,'/stage_movement','H5P_DEFAULT');
    end
    H5F.close(fid);
    
    
    %% save stage vector
    
    h5create(skeletons_file, '/stage_movement/stage_vec', size(stage_vec_d), 'Datatype', 'double', ...
        'Chunksize', size(stage_vec_d), 'Deflate', 5, 'Fletcher32', true, 'Shuffle', true)
    h5write(skeletons_file, '/stage_movement/stage_vec', stage_vec_d);
    
    h5create(skeletons_file, '/stage_movement/is_stage_move', size(is_stage_move_d), 'Datatype', 'int8', ...
        'Chunksize', size(is_stage_move_d), 'Deflate', 5, 'Fletcher32', true, 'Shuffle', true)
    h5write(skeletons_file, '/stage_movement/is_stage_move', is_stage_move_d);
    
    h5create(skeletons_file, '/stage_movement/frame_diffs', size(frame_diffs_d), 'Datatype', 'double', ...
        'Chunksize', size(frame_diffs_d), 'Deflate', 5, 'Fletcher32', true, 'Shuffle', true)
    h5write(skeletons_file, '/stage_movement/frame_diffs', frame_diffs_d);
    
    h5writeatt(skeletons_file, '/stage_movement', 'fps', fps)
    h5writeatt(skeletons_file, '/stage_movement', 'delay_frames', delay_frames)
    h5writeatt(skeletons_file , '/stage_movement',  'microns_per_pixel_scale',  micronsPerPixelScale)
    h5writeatt(skeletons_file , '/stage_movement',  'rotation_matrix',  rotation_matrix)
    
    
    
end

%masked_image_file = '/Users/ajaver/Desktop/Videos/single_worm/agar_goa/MaskedVideos/goa-1 (sa734)I on food L_2010_03_04__10_44_32___8___6.hdf5';
%skeletons_file = '/Users/ajaver/Desktop/Videos/single_worm/agar_goa/Results/goa-1 (sa734)I on food L_2010_03_04__10_44_32___8___6_skeletons.hdf5';

