rm(list=ls())

library(minfi)
library(limma)
library(openxlsx)

path = "E:/YandexDisk/Work/pydnameth/datasets/GPL13534/GSE74193"
path = "E:/YandexDisk/Work/pydnameth/datasets/GPL13534/GSE87571"
path = "E:/YandexDisk/Work/pydnameth/liver"

path_wd = paste(path, "/limma", sep='')
setwd(path_wd)

dataset <- read.table(paste(path, "/betas_part(control)_config(0.01_0.10_0.10)_norm(fun).txt",  sep=''), header = TRUE, sep = "\t")
dataset <- read.table(paste(path, "/betas_part(wo_missedFeatures)_config(0.01_0.10_0.10)_norm(fun).txt",  sep=''), header = TRUE, sep = "\t")
dataset <- read.csv(paste(path, "/betas_filtered.csv",  sep=''), header = TRUE)


data <- dataset
rownames(data) <- data[,1]
data_b <- data[,-1]
data_m <- logit2(data_b)

obs<-read.table(paste(path, "/observables_part(control).txt",  sep=''), header=TRUE, sep= "\t")
obs<-read.table(paste(path, "/observables_part(wo_missedFeatures).txt",  sep=''), header=TRUE, sep= "\t")
obs<-read.table(paste(path, "/observables.txt",  sep=''), header=TRUE, sep= "\t")

table(colnames(data_m)==obs$Sample_Name)
table(colnames(data_m)==obs$geo_accession)
table(colnames(data_m)==obs$geo_accession)

Sex <- obs$Sex
Age <- obs$Age

Sex <- obs$gender
Age <- obs$age

Sex <- obs$gender
Age <- obs$age

cells<-read.csv(paste(path, "/cells_counts_part(control).csv",  sep=''), header=TRUE)
cells<-read.csv(paste(path, "/cells_counts_part(wo_missedFeatures).csv",  sep=''), header=TRUE)

table(colnames(data_m)==cells$SampleID)

CD8T = cells$CD8T
CD4T = cells$CD4T
NK = cells$NK
Bcell = cells$Bcell
Gran = cells$Gran

propNeuron <- cells$propNeuron

# design <- model.matrix(~Sex+Age+propNeuron, data = data_m)
# design <- model.matrix(~Sex+Age+CD8T+CD4T+NK+Bcell+Gran, data = data_m)
# design <- model.matrix(~Sex+Age+CD8T+CD4T+NK+Bcell+Gran, data = data_beta)
# design <- model.matrix(~Sex+Age, data = data_beta)
design <- model.matrix(~Sex+Age+propNeuron, data = data_m)
design <- model.matrix(~Sex+Age+CD8T+CD4T+NK+Bcell+Gran, data = data_m)
design <- model.matrix(~Sex+Age, data = data_m)


head(design)
fit <- lmFit(data_m, design)
fit2 <- eBayes(fit)
topl1_Sex <- topTable(fit2, num=Inf,coef="SexM",sort.by="none")

topl1_Sex <- topTable(fit2, num=Inf,coef="SexMale",sort.by="none")

colnames(topl1_Sex) <- paste0("Sex_",colnames(topl1_Sex))
topl1_Age <- topTable(fit2, num=Inf,coef="Age",sort.by="none")
colnames(topl1_Age) <- paste0("Age_",colnames(topl1_Age))
table(rownames(topl1_Sex)==rownames(topl1_Age))
results <- data.frame(topl1_Sex,topl1_Age)

write.xlsx(results, 
           paste(path_wd, "/ms.xlsx", sep=''), 
           col.names = TRUE,
           row.names = TRUE)

# In case we decide to use M values, we have to find good thresholds; just as an example
dim(results[abs(results$Age_logFC)>0.001 & results$Age_adj.P.Val<0.01,])
dim(results[abs(results$Sex_logFC)>0.01 & results$Sex_adj.P.Val<0.01,])


