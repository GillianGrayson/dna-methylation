rm(list=ls())
library(minfi)
baseDir <- ("E:/YandexDisk/Work/pydnameth/E-MTAB-7309/r")
setwd(baseDir)

load("E-MTAB-7309_beta_Funnorm_filtered_samples_probes.RData")

write.table(beta_quantile,file="betas.txt",row.names=F,sep="\t",quote=F)

load("E-MTAB-7309_beta_Quantile_filtered_samples_probes.RData")

