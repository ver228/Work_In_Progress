library(dplyr)
library(RSQLite)
library(lme4)
library(lubridate)

read.experiments = function(my_db) { 
  
  exp_sql = sql(paste('SELECT', '*', 'FROM experiments'))
  experiments <- as.data.frame(tbl(my_db, exp_sql))
  experiments <- within(experiments, {
    video_id <- as.factor(video_id)
  })
  return(experiments)
}

read.features.names <- function(my_db){
  #get list of features to be predicted
  pred_feats = colnames(tbl(my_db, sql("SELECT * FROM features_means LIMIT 1")))
  pred_feats = pred_feats[-which(pred_feats %in% c("worm_index", "n_frames", "n_valid_skel", "video_id", "first_frame"))]
  return(pred_feats)  
}

read.features <- function(my_db, pred_feats){
  sql_cmd = paste0("SELECT video_id, ", paste(pred_feats, collapse = ',') ," FROM features_means")
  feat_means = as.data.frame(tbl(my_db, sql(sql_cmd)))
  return (feat_means)
}

database_name <- '~/OneDrive - Imperial College London/compare_strains_DB/control_single.db'
#search the sqlite database
my_db <- src_sqlite(database_name)

#read db data
experiments = read.experiments(my_db)
pred_feats = read.features.names(my_db)
features_means <- read.features(my_db, pred_feats)

feat_table = merge(experiments, features_means, by="video_id")

library(ggplot2)
ggplot( aes(x = strain, y =  midbody_speed, fill=strain), data=feat_table) + geom_jitter()

