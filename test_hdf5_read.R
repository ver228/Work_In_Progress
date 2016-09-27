# To access HDF5 files in R, we will use the rhdf5 library which is part of the 
#Bioconductor suite of R libraries.

#install rhdf5 package
#source("http://bioconductor.org/biocLite.R")
#biocLite("rhdf5")

#Call the R HDF5 Library
library("rhdf5")

h5_file = "/Users/ajaver/Desktop/Videos/individual_feat_files/507 ED3054 on food L_2011_02_17__12_48_17___6___7_features.hdf5"
features_timeseries = h5read(file = h5_file, 
       name = "/features_timeseries")

head(features_timeseries)

dimnames.data.frame(features_timeseries)[2]