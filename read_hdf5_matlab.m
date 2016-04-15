filename = '/Volumes/behavgenom$/GeckoVideo/Compressed/20150216/CaptureTest_90pc_Ch1_16022015_174636.hdf5';
if ~exist('infoFile', 'var')
    infoFile =  h5info(filename);
end

chunkSize = [2048 2048 1];

image = h5read(filename, '/mask', [1,1,1], chunkSize);
[~, rect] = imcrop(image);

for frame_number = 1:25:200
    image = h5read(filename, '/mask', [1,1,frame_number], chunkSize);
    figure, imshow(imcrop(image, rect))
end

%imshow(image)