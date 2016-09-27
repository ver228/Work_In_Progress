library(dplyr)

database_name = '~/Documents/GitHub/Work_In_Progress/work_in_progress/compare_features/pratheeban_features.db'
#database_name = '~/Documents/GitHub/Work_In_Progress/work_in_progress/compare_features/pratheeban_features.db'

my_db <- src_sqlite(database_name)
experiments = as.data.frame(tbl(my_db, sql("SELECT * FROM experiments")))

features_means = tbl(my_db, 
                     sql("SELECT * FROM features_means AS fm JOIN experiments AS e ON e.plate_id=fm.plate_id"))
features_means = select(features_means, -c(plate_id, full_name))
features_means = as.data.frame(features_means)

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



plot4means = function(df, field){
  plot_fun <- function(extra) {
    field_name = paste(field, extra, sep='')
    p = ggplot(df, aes_string(x="developmental_stage", y=field_name, colour="developmental_stage")) + 
      geom_violin(draw_quantiles = c(0.5)) #geom_boxplot() 
    return(p)
  } 
  plist = lapply(c('', '_pos', '_neg', '_abs'), plot_fun)
  n <- length(plist)
  nCol <- floor(sqrt(n))
  do.call("grid.arrange", c(plist, ncol=nCol))
  
}
plot4means(feat_means_auto, 'midbody_speed')

p1 = ggplot(feat_means_auto, aes_string(x="developmental_stage", y='length', colour="developmental_stage")) + 
  geom_violin(draw_quantiles = c(0.5)) #+ geom_boxplot(width=0.1, fill="white")
p2 = ggplot(feat_means_manual, aes_string(x="developmental_stage", y='length', colour="developmental_stage")) + 
  geom_violin(draw_quantiles = c(0.5)) 
grid.arrange(p1, p2, nrow=2)

ggplot(feat_means_auto, aes(x=date, y=length, colour=developmental_stage)) + geom_jitter()
ggplot(feat_means_auto, aes(x=date, y=area, colour=developmental_stage)) + geom_jitter()



