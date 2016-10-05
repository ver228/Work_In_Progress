library(dplyr)
library(RSQLite)
library(lme4)
library(lubridate)
library(lmerTest)


read.experiments = function(my_db) { 
  exp_fields = c("plate_id", "video_id", "base_name", "experiment_delta", "channel", "experiment_timestamp", "strain", "video_timestamp")          
  exp_sql = sql(paste('SELECT', paste(exp_fields, collapse = ','), 'FROM experiments'))
  experiments <- as.data.table(tbl(my_db, exp_sql))
  experiments = experiments[order(plate_id, base_name)]
  experiments <- within(experiments, {
    strain <- as.factor(strain)
    plate_id <- as.factor(plate_id)
    video_id <- as.factor(video_id)
    channel <- as.factor(channel)
    experiment_id <- factor(experiment_timestamp, label=1:length(unique(experiment_timestamp)))
    experiment_timestamp <- ymd_hms(experiment_timestamp)
    video_timestamp <- ymd_hms(video_timestamp)
    day_hour <- hour(video_timestamp) + minute(video_timestamp)/60 + second(video_timestamp)/3600
  })
  return(experiments)
}

read.features <- function(my_db){
  sql_cmd = paste0("SELECT * FROM features_means_split")
  feat_means = as.data.table(tbl(my_db, sql(sql_cmd)))
  return (feat_means)
}

get.comp.data = function(feat_table, strain, ctr_strain) {
  strain_ind = feat_table$strain == strain
  ctr_strain_ind = feat_table$strain == ctr_strain
  
  exp_ind = levels(droplevels(feat_table$experiment_id[strain_ind]))
  good_ind = (feat_table$experiment_id %in% exp_ind) & (strain_ind | ctr_strain_ind)
  comp_data = feat_table[good_ind, ]
  
  #drop extra levels
  comp_data <- within(comp_data, {
    strain_cmp <- strain != ctr_strain
    plate_id <- droplevels(plate_id)
    video_id <- droplevels(video_id)
    experiment_id <- droplevels(experiment_id)
    strain <- droplevels(strain)
  })
  
  #check if i am really selecting two strains...
  n_strains_to_compare = length(levels(comp_data$strain))
  stopifnot(n_strains_to_compare==2)
  
  return(comp_data)
}

calc.model = function(feat, comp_data, frac_thresh = 0.1){
  good_frac = 1 - sum(is.na(comp_data[[feat]]))/dim(comp_data)[1]
  
  if(good_frac > frac_thresh)
  {
    fit.full <- lmer(paste0('log10(abs(', feat, ') + 1) ~ strain_cmp + ', RANDOM_EFFECTS), 
                     data = comp_data, na.action = na.exclude)
  }
  else {fit.full = NULL}
  
  return(fit.full)
}

calc.model.strain = function(pred_feats, comp_data){
  ff = function(x) {progress.wrapper(x, calc.model, x, comp_data)}
  feats_stats = sapply(pred_feats, ff)
  return(feats_stats)
}

progress.wrapper = function(progress_txt, FUNC, ...){
  start.time <- Sys.time()
  output = FUNC(...)
  print(paste(progress_txt, Sys.time() - start.time))
  return(output)
}

database_name <- '~/OneDrive - Imperial College London/compare_strains_DB/control_experiments.db'
my_db <- src_sqlite(database_name)

experiments = read.experiments(my_db)
pred_feats = c('midbody_speed') #read.features.names(my_db)
features_means <- read.features(my_db)

#select only the first video of each experiment (we want to reduce extra data)
exp_tt = experiments[, .SD[2,], by=plate_id]
exp_tt = filter(exp_tt, as.integer(experiment_id)<=4)

exp_tt <- within(exp_tt, {
  strain <- droplevels(strain)
  plate_id <- droplevels(plate_id)
  video_id <- droplevels(video_id)
  experiment_id <- droplevels(experiment_id)
})

#merge experiments data with the features table
feat_table = merge(exp_tt, features_means, by="video_id")

comp_data = get.comp.data(feat_table, 'unc-9', 'WT')
fit.full <- lmer(log10(abs(midbody_speed_abs)+1) ~ strain_cmp + (1 + strain_cmp | experiment_id/channel), 
                 data = comp_data, na.action = na.exclude)
anova(fit.full)

library(ggplot2)
#ggplot( aes(x = experiment_id, y = log10(abs(midbody_speed_abs+1)), fill=strain), data=feat_table) + geom_boxplot()
ggplot( aes(x = experiment_id, y = (midbody_width), fill=strain), data=feat_table) + geom_boxplot()

#fit.null <- lmer(log2(abs(midbody_speed) + 1) ~ (strain_cmp | plate_id),
#                 data = comp_data, REML=FALSE)

#likelihood <- anova(fit.null, fit.full, test="F")