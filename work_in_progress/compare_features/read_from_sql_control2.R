library(dplyr)
library(RSQLite)
library(data.table)
library(lme4)
library(lubridate)

#RANDOM_EFFECTS = '(1+strain_cmp | experiment_delta) + 
#                  (1+strain_cmp | experiment_timestamp) + 
#                  (1+strain_cmp | plate_id)'

RANDOM_EFFECTS = '(1+strain_cmp | experiment_id/channel)'

get.model = function(pred_feat, comp_data, frac_thresh = 0.1){
  good_frac = 1 - sum(is.na(comp_data[[pred_feat]]))/dim(comp_data)[1]
  
  if(good_frac > frac_thresh)
    {
    fit.full <- lmer(paste0('log10(abs(', pred_feat, ') + 1) ~ strain_cmp + ', RANDOM_EFFECTS), 
                    data = comp_data, na.action = na.exclude)#, REML=FALSE )
  
    fit.null <- lmer(paste0('log10(abs(', pred_feat, ') + 1) ~ ', RANDOM_EFFECTS),
                    data = comp_data)#, REML=FALSE)
    
    likelihood <- anova(fit.null, fit.full, test="F")
    
    output = list('likelihood' = likelihood, 'fit.full' = fit.full, 'fit.null' = fit.null)
    }
  else {output = list()}

  return(output)
}

get.mod.linear = function(pred_feats, comp_data){
  get.model.comp = function(feat) {
    progress_wrapper(feat, get.model, feat, comp_data)
  }
  feats_stats = sapply(pred_feats, get.model.comp)
  return(feats_stats)
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

get.model.strain = function(strain, ctr_strain, pred_feats){
  
  comp_data = get.comp.data(strain)
  #calculate the linear model, displaying the time per feature
  feats_stats = progress_wrapper('T1', get.mod.linear, pred_feats, comp_data)
  return(feats_stats)
}


progress_wrapper = function(progress_txt, FUNC, ...){
  start.time <- Sys.time()
  output = FUNC(...)
  print(paste(progress_txt, Sys.time() - start.time))
  return(output)
}

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

read.features.names <- function(my_db){
  #get list of features to be predicted
  pred_feats = colnames(tbl(my_db, sql("SELECT * FROM features_means LIMIT 1")))
  pred_feats = pred_feats[-which(pred_feats %in% c("worm_index", "n_frames", "n_valid_skel", "video_id", "first_frame"))]
  return(pred_feats)  
}

read.features <- function(my_db, pred_feats){
  sql_cmd = paste0("SELECT video_id, ", pred_feats ,", midbody_speed FROM features_means_split")
  feat_means = as.data.table(tbl(my_db, sql(sql_cmd)))
  return (feat_means)
}

read.pvals = function(feats_stats){
  read.pval = function(x) {
    output = x$likelihood$`Pr(>Chisq)`[2] 
    return (if (is.null(output)) NA else output)
  }
  sapply(feats_stats, read.pval)
}


database_name <- '~/OneDrive - Imperial College London/compare_strains_DB/control_experiments.db'

#search the sqlite database
my_db <- src_sqlite(database_name)

#read db data
experiments = read.experiments(my_db)
pred_feats = c('midbody_speed') #read.features.names(my_db)
features_means <- read.features(my_db, pred_feats)

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
feat_table = as.data.table(merge(exp_tt, features_means, by="video_id"))
#make strain a key to allow us to search
setkeyv(feat_table, "strain");

ctr_strain = 'WT' #here the control strain is "WT"
strains = levels(feat_table$strain)
strains = strains[-which(strains == ctr_strain)]

strains_stats = lapply(strains, function(x){get.model.strain(x, ctr_strain, pred_feats)})
names(strains_stats) = strains

#strains_pvals = do.call(rbind, lapply(strains_stats, read.pvals))
#strains_pvals = t(as.data.frame(strains_pvals))
#strains_pvals_adj = apply(strains_pvals, 2, function(x) {p.adjust(x, 'BH')})
#%%
dd = feat_table['tpr-4']
#plot(midbody_speed~plate_id, data=dd)
library(ggplot2)
ggplot( aes(x = experiment_id, y = log2(abs(midbody_speed+1)), fill=strain), data=feat_table) + geom_boxplot()
