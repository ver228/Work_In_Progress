library(h5)
file = "/Users/ajaver/Desktop/Videos/pratheeban/Results/L1_Early/15_07_07/15_07_07_C1_overnt_Ch1_07072015_160917_feat_manual.hdf5" 

fid <- h5file(file, 'r')
dfeat_means <- fid['/features_means']
h5close(fid)
