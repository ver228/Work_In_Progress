addpath('/Users/ajaver/GitHub_repositories/SegWorm/Only_segWorm/normWorms')
main_dir = '/Users/ajaver/Desktop/Gecko_compressed/image_dums/';

files = dir([main_dir '*.txt']);

moves = [0, 0];
origins = [0,0];
pixel2MicronScale = [1, 1];
rotation = 1;
downSamples = 65;
for frame = 1:numel(files)
    mask = csvread([main_dir, files(frame).name]);
    imgData = mask(:);
    maskData = mask(:);
    imgWidth = size(mask,1); 
    imgHeight =  size(mask,2);
    bodyScale = 0.1;
    verbose = false;
    
    resampleNum = 50;
    [worm_results, worm] = getWormSkeletonM(mask, frame, [], resampleNum);
    %[worm, errNum, errMsg] = segWormBWimgSimple(imgData, maskData, imgWidth, imgHeight, frame, bodyScale, verbose);
    disp(frame)
    %disp(errMsg)
    
    %{
    figure
    imshow(mask)
    hold on
    if ~isempty(worm)
        plot(worm.skeleton.pixels(:,2), worm.skeleton.pixels(:,1))
        plot(worm.contour.pixels(:,2), worm.contour.pixels(:,1), 'r')
        %{
        [vulvaContour nonVulvaContour skeleton skeletonAngles ...
                    inOutTouch skeletonLength widths headArea tailArea ...
                    vulvaArea nonVulvaArea] = normWorms({worm}, ...
                    downSamples);%, origins, moves, pixel2MicronScale, rotation, false);
                
        plot(worm.skeleton.pixels(:,2), worm.skeleton.pixels(:,1))
        plot(worm.contour.pixels(:,2), worm.contour.pixels(:,1), 'r')
        plot(skeleton(:,1), skeleton(:,2), '.-g')
        plot(nonVulvaContour(:,1), nonVulvaContour(:,2), '.-g')
        plot(vulvaContour(:,1), vulvaContour(:,2), '.-g')
        %}
    end
    %}
end