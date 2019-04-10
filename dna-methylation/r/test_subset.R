rm(list=ls())

getwd()
setwd("D:/YandexDisk/Work/pydnameth") 

hm450_hg19_manifest <- read.table("hm450.hg19.manifest.txt",sep="\t",header=T)

length(hm450_hg19_manifest)
dim(hm450_hg19_manifest)
str(hm450_hg19_manifest)

summary(hm450_hg19_manifest $ MASK_general)

bad_cpgs = hm450_hg19_manifest $ probeID[hm450_hg19_manifest $ MASK_general == TRUE]
bad_cpgs <- droplevels(bad_cpgs)

write(as.character(bad_cpgs), 'bad_cpgs.txt')
