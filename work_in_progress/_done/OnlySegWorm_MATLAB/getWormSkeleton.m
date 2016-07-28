function [worm_results, worm] = getWormSkeleton(maskData, ... 
imgWidth, imgHeight, frame, worm_results_prev, resampleNum)

%prevOrientWorm = [];
%downSamples = 65;
%downSamples = double(downSamples); %make sure this quantity is a floating point
% Setup the stage movements.
%moves = [0, 0];
%origins = [0,0];
%pixel2MicronScale = [-1, -1];
%rotation = 1;

% Pre-compute the values for orienting successive worm frames.
%orientSamples = [1:5 7:11] / 12;
% Segment the video frame.
%worm = segWorm(img, frame, true,false);

worm_results = [];
worm = segWormBWimgSimple(maskData, maskData, imgWidth, imgHeight, frame, 0.1, false);

if ~isempty(worm)
    % Orient and downsample the worm.
    tailI = worm.contour.tailI;
    headI = worm.contour.headI;
    dorsal = worm.contour.pixels(headI:tailI,:);
    ventral = [worm.contour.pixels(tailI:end,:); worm.contour.pixels(1:headI,:)];
    ventral = flip(ventral);
    skeleton = worm.skeleton.pixels;
    
    worm_results.skeleton = curvspaceMex(skeleton, resampleNum);
    worm_results.ventral = curvspaceMex(ventral, resampleNum);
    worm_results.dorsal = curvspaceMex(dorsal, resampleNum);
    worm_results.frame = frame;
    
    if isempty(worm_results_prev)
        return
    end
    
    delta_head = sum((worm_results_prev.skeleton(1,:) - worm_results.skeleton(1,:)).^2);
    delta_tail = sum((worm_results_prev.skeleton(1,:) - worm_results.skeleton(end,:)).^2);
    if delta_head > delta_tail
        worm_results.dorsal = flip(worm_results.dorsal);
        worm_results.ventral = flip(worm_results.ventral);
        worm_results.skeleton = flip(worm_results.skeleton);
    end
    
    midpoint = round(resampleNum/2);
    %delta_DD = sum((worm_results_prev.dorsal(midpoint+(-1:1),:) - worm_results.dorsal(midpoint+(-1:1),:)).^2);
    %delta_DV = sum((worm_results_prev.dorsal(midpoint+(-1:1),:) - worm_results.ventral(midpoint+(-1:1),:)).^2);
    delta_DD = sum((worm_results_prev.dorsal(midpoint,:) - worm_results.dorsal(midpoint,:)).^2);
    delta_DV = sum((worm_results_prev.dorsal(midpoint,:) - worm_results.ventral(midpoint,:)).^2);
    
    if delta_DD > delta_DV
        dum = worm_results.dorsal;
        worm_results.dorsal = worm_results.ventral;
        worm_results.ventral = dum;
    end
    
    
end

%{
    % Determine the worm orientation.
    if isempty(prevOrientWorm)
        % Are the head and tail flipped?
        if worm.orientation.head.confidence.head < worm.orientation.head.confidence.tail;
            worm = flipWormHead(worm);
        end
        
        % Where is the vulva?
        if worm.orientation.vulva.confidence.vulva < worm.orientation.vulva.confidence.nonVulva
            worm = flipWormVulva(worm);
        end
    else
        % Orient the worm relative to the nearest segmented frame.
        [worm, ~, ~] = ...
            orientWorm(prevOrientWorm, worm, orientSamples);
    end
    
    tailI = worm.contour.tailI;
    headI = worm.contour.headI;
    dorsal = worm.contour.pixels(headI:tailI,:);
    ventral = [worm.contour.pixels(tailI:end,:); worm.contour.pixels(1:headI,:)];
    ventral = flip(ventral);
    skeleton = worm.skeleton.pixels;
    
    worm_results.skeleton = curvspace(skeleton, resampleNum);
    worm_results.ventral = curvspace(ventral, resampleNum);
    worm_results.dorsal = curvspace(dorsal, resampleNum);
    
    
    
    %{
    if worm.orientation.head.isFlipped
        worm_results.dorsal = flip(worm_results.dorsal);
        worm_results.ventral = flip(worm_results.ventral);
        worm_results.skeleton = flip(worm_results.skeleton);
        
        dum = worm_results.dorsal;
        worm_results.dorsal = worm_results.ventral;
        worm_results.ventral = dum;
    end
    
    
    if ~worm.orientation.vulva.isClockwiseFromHead && ~worm.orientation.head.isFlipped
        dum = worm_results.dorsal;
        worm_results.dorsal = flip(worm_results.ventral);
        worm_results.ventral = flip(dum);
    end
    %}
    
    %{
    % Downsample the worm.
    % Normalize the worm.
    [vulvaContour, nonVulvaContour, skeleton, skeletonAngles, ...
        inOutTouch, skeletonLength, widths, headArea, tailArea, ...
        vulvaArea, nonVulvaArea] = normWorms({worm}, ...
        downSamples, origins, moves, pixel2MicronScale, ...
        rotation, false);
    
    % Reconstruct the normalized worm.
    worm = norm2Worm(frame, vulvaContour, nonVulvaContour, ...
        skeleton, skeletonAngles, inOutTouch, ...
        skeletonLength, widths, ...
        headArea, tailArea, vulvaArea, nonVulvaArea, ...
        origins, pixel2MicronScale, rotation, worm);
    %}
    %save('./dum.mat', 'worm')
end
%}
