library(rhdf5)
library(data.table)
library(iterators)
library(foreach)

splitPath <- function(fpath) {
  path_parts = strsplit(fpath, .Platform$file.sep)[[1]]
  
  developmental_stage = path_parts[[1]]
  full_path = file.path(main_dir, fpath)
  base_name = strsplit(path_parts[[3]], '_feat')[[1]][1] 
  
  dum = strsplit(base_name, '_Ch1_')[[1]]
  if (length(dum) == 2){
    datetime_str = dum[[2]]
    date_str = strsplit(datetime_str, "_")[[1]][1]
    date_f = as.Date(date_str, "%d%m%Y")
    time_f = as.POSIXct(datetime_str, "%d%m%Y_%H%M%S", tz="UTC")
  } 
  else {
    date_str = path_parts[[2]]
    date_f = as.Date(date_str, "%y_%m_%d")
    time_f = as.POSIXct(NA)
  }
  return(list(developmental_stage, base_name, full_path, date_f, time_f))
}

readExperimentsDF <- function(main_dir, is_manual){
  
  search_pattern = if(is_manual) '.*_feat_manual.hdf5' else '.*_features.hdf5'
  files = list.files(path = main_dir, recursive=T, pattern=search_pattern)
    
  splitted_files = lapply(files, splitPath)
  experiments = rbindlist(splitted_files)
  colnames(experiments) = c('developmental_stage', 'base_name', 'full_name', 'date', 'datetime')
  return(experiments)
}

main_dir = '/Users/ajaver/Desktop/Videos/pratheeban/Results'
experiments_manual = readExperimentsDF(main_dir, T)
experiments = readExperimentsDF(main_dir, F)


#features_timeseries = h5read(experiments$full_name[ind], '/features_timeseries')

readRowFeatMeans <- function(x) {
  start_time = Sys.time()
  print(x['full_name'])
  ff = h5read(x['full_name'], '/features_means')
  ff['date'] = as.Date(x['date'])
  ff['datetime'] = as.POSIXct(x['datetime'])
  ff['developmental_stage'] = x['developmental_stage']
  time_taken <-  Sys.time() - start_time
  print(time_taken)
  return(ff)
}

features_means = apply(experiments_manual, 1, readRowFeatMeans)
features_means = rbindlist(features_means)

library(ggplot2)
ggplot(features_means, aes(x=datetime, y=midbody_speed, colour=developmental_stage)) + 
  geom_point(size=3) + geom_jitter(width = 0.1, height = 0.1)





