library(dplyr)

database_name = '~/Documents/GitHub/Work_In_Progress/work_in_progress/compare_features/control_experiments.db'

my_db <- src_sqlite(database_name)
experiments = as.data.frame(tbl(my_db, sql("SELECT * FROM experiments")))

features_means = tbl(my_db, 
                     sql("SELECT * FROM features_means AS fm JOIN experiments AS e ON e.video_id=fm.video_id"))
features_means = select(features_means, -c(plate_id, full_name))
features_means = as.data.frame(features_means)

features_means$strain <- as.factor(features_means$strain)
features_means$plate_id <- as.factor(features_means$plate_id)

features_means$video_timestamp = as.POSIXct(features_means$video_timestamp)
features_means$experiment_timestamp = as.POSIXct(features_means$experiment_timestamp)

#valid_dates = features_means$date >= as.Date("2016-06-23")
#features_means = features_means[valid_dates,]

feat_means_manual = features_means[features_means$is_manual==1, ]
feat_means_auto = features_means[features_means$is_manual==0, ]

library(ggplot2)
library(gridExtra)

#ggplot(feat_means_manual, aes(x=developmental_stage, y=midbody_speed, colour=developmental_stage)) + 
#  geom_boxplot() + geom_jitter(width = 0.2)
#ggplot(feat_means_manual, aes(x=developmental_stage, y=midbody_speed, colour=date)) + 
#  geom_boxplot() 
#ggplot(feat_means_manual, aes(x=developmental_stage, y=midbody_speed_neg, colour=date)) + 
#  geom_boxplot() 


group_type = "strain"   #"developmental_stage"


plot4means = function(df, field){
  plot_fun <- function(extra) {
    field_name = paste(field, extra, sep='')
    p = ggplot(df, aes_string(x=group_type, y=field_name, colour=group_type)) + 
      geom_violin(draw_quantiles = c(0.5)) #geom_boxplot() 
    return(p)
  } 
  plist = lapply(c('', '_pos', '_neg', '_abs'), plot_fun)
  n <- length(plist)
  nCol <- floor(sqrt(n))
  do.call("grid.arrange", c(plist, ncol=nCol))
  
}

#plot4means(feat_means_auto, 'midbody_speed')

#p1 = ggplot(feat_means_auto, aes_string(x="strain", y='length', colour=group_type)) + 
#  geom_violin(draw_quantiles = c(0.5)) #+ geom_boxplot(width=0.1, fill="white")
#p2 = ggplot(feat_means_manual, aes_string(x=group_type, y='length', colour=group_type)) + 
#  geom_violin(draw_quantiles = c(0.5)) 
#grid.arrange(p1, p2, nrow=2)

#ggplot(feat_means_auto, aes_string(x="date", y="length", colour=group_type)) + geom_jitter()
#ggplot(feat_means_auto, aes_string(x="date", y="area", colour=group_type)) + geom_jitter()

#plot4means(features_means, 'midbody_speed')



p = ggplot(features_means, aes_string(x="experiment_delta", y="length", colour=group_type)) 
p + geom_jitter() + facet_wrap( ~ strain)
p 


dd = lm(length ~ strain + experiment_timestamp + experiment_delta + plate_id, data =features_means)


mod = model.matrix(~ strain + experiment_timestamp + experiment_delta + plate_id, data=features_means)
fit = lm.fit(mod, as.matrix(features_means[, c('area', 'length')]))
fit$coefficients[2,]

#%% combat
batch = 
modcombat = model.matrix(~1, data=features_means)
modstrain = model.matrix(~strain, data=features_means)

combat_edata = ComBat(dat=edata, batch=batch, mod=modcombat, par.prior=T, prior.plots=TRUE)

#removing pc does not work in normal cases, only if the signal is low enough like wide association studies.
#normalization between samples does not makes much sense, the distribution are likely to be due to real biological variations between samples rather than techinical issueslibrary(dagdata)
data(admissions)


