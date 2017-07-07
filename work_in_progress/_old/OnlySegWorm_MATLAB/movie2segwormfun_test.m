%function movie2segwormfun(data, masked_image_file, save_file)

%program constants
RESAMPLE_SIZE = 50;
MASK_CHUNK_SIZE = [2048 2048 1]; %it mabye good to extract this info from h5info
BUFF_SIZE = 1000; %buffer size, used to not write too much on the hdf5
MAX_DT_ALLOWED = 5; 

ROI_SIZE = 130; %region to be analyzed
window_lims = [-ROI_SIZE/2 ROI_SIZE/2];


%Delete previous file if exist.
if exist(save_file, 'file')
    delete(save_file)
end

%create datasets to be saved in the hdf5, 
h5create(save_file, '/segworm_results/plate_worms_id', Inf, 'Deflate', 1, 'Shuffle', true, 'Chunksize', 100)
h5create(save_file, '/segworm_results/worm_index_joined', Inf, 'Deflate', 1, 'Shuffle', true, 'Chunksize', 100)
h5create(save_file, '/segworm_results/frame_number', Inf, 'Deflate', 1, 'Shuffle', true, 'Chunksize', 100)
h5create(save_file, '/segworm_results/skeleton', [RESAMPLE_SIZE, 2, Inf], 'Deflate', 1, 'Shuffle', true, 'Chunksize', [RESAMPLE_SIZE,2,1])
h5create(save_file, '/segworm_results/contour_ventral', [RESAMPLE_SIZE, 2, Inf], 'Deflate', 1, 'Shuffle', true, 'Chunksize', [RESAMPLE_SIZE,2,1])
h5create(save_file, '/segworm_results/contour_dorsal', [RESAMPLE_SIZE, 2, Inf], 'Deflate', 1, 'Shuffle', true, 'Chunksize', [RESAMPLE_SIZE,2,1])

%%
%sort data by time, it is easier to open frames like that
[~,sortbytime] = sort(data.('frame_number'));
for ff = fieldnames(data)'
    data.(ff{1}) = data.(ff{1})(sortbytime);
end

%% 
%initialize buffer
data2write = [];
for ff = {'plate_worms_id', 'worm_index_joined', 'frame_number'}
    data2write.(ff{1}) = zeros(1,BUFF_SIZE);
end
for ff = {'skeleton', 'contour_ventral', 'contour_dorsal'}
    data2write.(ff{1}) = zeros(RESAMPLE_SIZE,2,BUFF_SIZE);
end

%initialize some variables
current_frame = 0;
tot_segworm_rows = 0;
prev_worms = cell(1,max(data.worm_index_joined));


ind = find(data.('worm_index_joined') == 595)';
%main loop
%%
tic
for plate_worms_row = 1000:1020%numel(data.('frame_number'))
    %read a new image if we change current frame
    %if data.('worm_index_joined')(plate_worms_row) == 24
        
    %end
    if data.('frame_number')(plate_worms_row) ~= current_frame
        current_frame = data.('frame_number')(plate_worms_row);
        I = h5read(masked_image_file, '/mask', [1,1,current_frame], MASK_CHUNK_SIZE)';
        
        if mod(current_frame,25) == 0
            disp(current_frame)
            toc
            tic
        end
    end
    worm_index = data.('worm_index_joined')(plate_worms_row);
    
    %select region of interest, maybe is better to use a tighter bounding box
    range_x = round(data.('coord_x')(plate_worms_row) + window_lims + 1); %add one for matlab indexing
    range_y = round(data.('coord_y')(plate_worms_row) + window_lims + 1);
    
    %continue if the range is out of the image limit
    %TODO: deal with this in a more clever way
    if range_y(1) < 1 || (range_y(2) > MASK_CHUNK_SIZE(1)) || ...
            range_x(1) < 1 || (range_x(2) >= MASK_CHUNK_SIZE(2))
        continue
    end
    
    %obtain binary image
    worm_img = I(range_y(1):range_y(2), range_x(1):range_x(2));
    %worm_img = ordfilt2(worm_img, 1, ones(3,3));
    
    
    %}
    %%
    thresh = round(data.('threshold')(plate_worms_row));
    worm_mask = (worm_img <= thresh &  (worm_img~=0));
    worm_mask = bwmorph(worm_mask, 'close', 2);
    worm_mask = bwmorph(worm_mask, 'erode', 1);
    
    %%
    
    
    if ~isempty(prev_worms{worm_index}) && ...
            current_frame - prev_worms{worm_index}.frame > MAX_DT_ALLOWED
        prev_worms{worm_index} = [];
    end
    
    %segworm!
    [worm_results, ~] = getWormSkeletonM(worm_mask, current_frame, prev_worms{worm_index}, RESAMPLE_SIZE);
    if isempty(worm_results)
        continue
    end
    
    prev_worms{worm_index} = worm_results; %save previous result with the ROI coordinate system
    
    for ff = {'skeleton', 'contour_ventral', 'contour_dorsal'}
        %get data into image absolute coordinates before saving to the bufer
        %-2 is to come back into python indexing (-1 from range_y and -1 from worm_results)
        worm_results.(ff{1})(:,1) =  worm_results.(ff{1})(:,1) + range_y(1)-2;
        worm_results.(ff{1})(:,2) =  worm_results.(ff{1})(:,2) + range_x(1)-2;
    end
    
    %add data to the buffer
    tot_segworm_rows = tot_segworm_rows+1;
    buff_ind = mod(tot_segworm_rows-1, BUFF_SIZE)+1;
    for ff = {'plate_worms_id', 'worm_index_joined', 'frame_number'}
        data2write.(ff{1})(buff_ind) = data.(ff{1})(plate_worms_row);
    end
    for ff = {'skeleton', 'contour_ventral', 'contour_dorsal'}
        data2write.(ff{1})(:,:,buff_ind) = worm_results.(ff{1});
    end
    
    %write data when the buffer is full
    if buff_ind == BUFF_SIZE
        offset = tot_segworm_rows-buff_ind+1;
        for ff = {'plate_worms_id', 'worm_index_joined', 'frame_number'}
            h5write(save_file, ['/segworm_results/' ff{1}], data2write.(ff{1}), offset, buff_ind);
        end
        for ff = {'skeleton', 'contour_ventral', 'contour_dorsal'}
            h5write(save_file, ['/segworm_results/' ff{1}], data2write.(ff{1}), [1,1,offset], [RESAMPLE_SIZE,2,buff_ind]);
        end
    end
    %
    figure
    imshow(I)
    hold on
    xlim(range_x)
    ylim(range_y)
    plot(worm_results.skeleton(:,2)+1, worm_results.skeleton(:,1)+1)
    plot(worm_results.contour_ventral(:,2)+1, worm_results.contour_ventral(:,1)+1)
    plot(worm_results.contour_dorsal(:,2)+1, worm_results.contour_dorsal(:,1)+1)
    %}
end

%write any data remaining in the buffer
if buff_ind ~= BUFF_SIZE
    offset = tot_segworm_rows-buff_ind+1;
    for ff = {'plate_worms_id', 'worm_index_joined', 'frame_number'}
        h5write(save_file, ['/segworm_results/' ff{1}], data2write.(ff{1})(1:buff_ind), offset, buff_ind);
    end
    for ff = {'skeleton', 'contour_ventral', 'contour_dorsal'}
        h5write(save_file, ['/segworm_results/' ff{1}], data2write.(ff{1})(:,:,1:buff_ind), [1,1,offset], [RESAMPLE_SIZE,2,buff_ind]);
    end
end
toc