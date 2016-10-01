library(dplyr)
library(RSQLite)
library(data.table)
library(lme4)
library(lubridate)
library(foreach)
library(doParallel)

#RANDOM_EFFECTS = '(1+strain_cmp | experiment_delta) + 
#                  (1+strain_cmp | experiment_timestamp) + 
#                  (1+strain_cmp | plate_id)'

RANDOM_EFFECTS = '(1+strain_cmp | plate_id)'

get.model = function(pred_feat, comp_data, frac_thresh = 0.05){
  good_frac = 1 - sum(is.na(comp_data[[pred_feat]]))/dim(comp_data)[1]
  
  if(good_frac > frac_thresh)
    {
    fit.full <- lmer(paste0(pred_feat, ' ~ strain_cmp + ', RANDOM_EFFECTS), 
                    data = comp_data, REML=FALSE, na.action = na.exclude)
  
    fit.null <- lmer(paste0(pred_feat, ' ~ ', RANDOM_EFFECTS),
                    data = comp_data, REML=FALSE)
    
    likelihood <- anova(fit.null, fit.full, test="F")
    
    output = list('likelihood' = likelihood, 'fit.full' = fit.full, 'fit.null' = fit.null)
    }
  else {output = NA}

  return(output)
}

progress_wrapper = function(progress_txt, FUNC, ...){
  start.time <- Sys.time()
  output = FUNC(...)
  print(paste(progress_txt, Sys.time() - start.time))
  return(output)
}

get.mod.linear = function(pred_feats, comp_data){
  get.model.comp = function(feat) {
    progress_wrapper(feat, get.model, feat, comp_data)
  }
  feats_stats = sapply(pred_feats, get.model.comp)
  return(feats_stats)
}

get.mod.parallel = function(pred_feats, comp_data, n_cores = detectCores() - 1){
  registerDoParallel(n_cores)
  feats_stats <- foreach(pred_feat = pred_feats, .combine=list) %dopar%  get.model(pred_feat, comp_data)
  stopImplicitCluster()
  return(feats_stats)
}

get.experiments = function(my_db) { 
  exp_fields = c("plate_id", "video_id", "base_name", "channel", "experiment_delta", "experiment_timestamp", "strain", "video_timestamp")          
  exp_sql = sql(paste('SELECT', paste(exp_fields, collapse = ','), 'FROM experiments'))
  experiments <- as.data.table(tbl(my_db, exp_sql))
  experiments = experiments[order(plate_id, base_name)]
  experiments <- within(experiments, {
    strain <- as.factor(strain)
    plate_id <- as.factor(plate_id)
    video_id <- as.factor(video_id)
    experiment_id <- factor(experiment_timestamp, label=1:length(unique(experiment_timestamp)))
    experiment_timestamp <- ymd_hms(experiment_timestamp)
    video_timestamp <- ymd_hms(video_timestamp)
    day_hour <- hour(video_timestamp) + minute(video_timestamp)/60 + second(video_timestamp)/3600
  })
  return(experiments)
}

get.features.names <- function(my_db){
  #get list of features to be predicted
  pred_feats = colnames(tbl(my_db, sql("SELECT * FROM features_means LIMIT 1")))
  pred_feats = pred_feats[-which(pred_feats %in% c("worm_index", "n_frames", "n_valid_skel", "video_id", "first_frame"))]
  return(pred_feats)  
}


get.model.strain = function(strain, ctr_strain, pred_feats){
  comp_data <- rbind(feat_table[ctr_strain], feat_table[strain])
  n_strains_to_compare = length(levels(comp_data$strain))
  stopifnot(n_strains_to_compare==2)
  
  comp_data <- within(comp_data, {
    strain_cmp <- strain != ctr_strain
    plate_id <- droplevels(plate_id)
    video_id <- droplevels(video_id)
    experiment_id <- droplevels(experiment_id)
  })
  
  feats_stats = progress_wrapper('T1', get.mod.linear, pred_feats, comp_data)
  return(feats_stats)
}

read.pvals = function(feats_stats){
  read.pval = function(x){if(! is.na(x)) x$likelihood$`Pr(>Chisq)`[2] else NA}
  sapply(feats_stats, read.pval)
}

database_name <- '~/Documents/GitHub/Work_In_Progress/work_in_progress/compare_features/control_experiments.db'
#'/Users/ajaver/OneDrive - Imperial College London/compare_strains_DB/control_experiments.db'

#search the sqlite database
my_db <- src_sqlite(database_name)

#read db data
experiments = get.experiments(my_db)
features_means <- as.data.table(tbl(my_db, sql("SELECT * FROM features_means_split")))
pred_feats = get.features.names(my_db)

#select only the first video of each experiment (we want to reduce extra data)
exp_tt = experiments[, .SD[1,], by=plate_id]

#merge experiments data with the features table
feat_table = as.data.table(merge(exp_tt, features_means, by="video_id"))
#make strain a key to allow us to search
setkeyv(feat_table, "strain");


ctr_strain = 'WT' #here the control strain is "WT"
strains = levels(feat_table$strain)
strains = strains[-which(strains == ctr_strain)]
strains_stats = sapply(strains, function(x){get.model.strain(x, ctr_strain, pred_feats)})
names(strains_stats) = strains

strains_pvals = do.call(rbind, lapply(strains_stats, read.pvals))
strains_pvals_adj = apply(strains_pvals, 1, function(x) {p.adjust(x, 'BH')})
