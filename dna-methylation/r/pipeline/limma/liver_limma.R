rm(list=ls())

library(minfi)
library(limma)

path <- "E:/YandexDisk/Work/pydnameth/limma"
setwd(path)

#gse = "liver"
#dataset <- read.table(paste("E:/YandexDisk/Work/pydnameth/", gse, "/betas.txt",  sep=''), header = TRUE, sep = "\t")


gse = "GSE74193"
dataset <- read.table(paste("E:/YandexDisk/Work/pydnameth/script_datasets/GPL13534/filtered/brain(DLPFC)/", gse, "/betas_norm(fun)_part(control).txt",  sep=''), header = TRUE, sep = "\t")


# the input should be a dataframe of methylation values; limma should work better with M values, try to convert beta values in M and launch limma first on M values and then on beta values
data<-dataset
rownames(data) <- data[,1]
data_beta <- data[,-1]
data_m <- logit2(data_beta)

#ss<-read.table(paste("E:/YandexDisk/Work/pydnameth/", gse, "/observables.txt",  sep=''), header=TRUE, sep= "\t")
#str(ss)

ss<-read.table(paste("E:/YandexDisk/Work/pydnameth/script_datasets/GPL13534/filtered/brain(DLPFC)/", gse, "/observables_part(control).txt",  sep=''), header=TRUE, sep= "\t")#str(ss)

#table(colnames(data_m)==ss$geo_accession)
#table(colnames(data_beta)==ss$geo_accession)

#table(colnames(data_m)==ss$Basename)
table(colnames(data_beta)==ss$Sample_Name)

#Sex <- ss$gender
#Age <- ss$age

Sex <- ss$Sex
Age <- ss$Age

cells<-read.table(paste("E:/YandexDisk/Work/pydnameth/script_datasets/GPL13534/filtered/brain(DLPFC)/", gse, "/cells_counts_part(control).txt",  sep=''), header=TRUE, sep= "\t")
#cells<-read.table(paste("E:/YandexDisk/Work/pydnameth/", gse, "/cells_horvath_calculator.txt",  sep=''), header=TRUE, sep= "\t")


CD8T = cells$CD8T
CD4T = cells$CD4T
NK = cells$NK
Bcell = cells$Bcell
Gran = cells$Gran

propNeuron <- cells$propNeuron

# design <- model.matrix(~Sex+Age, data = data_m)
# design <- model.matrix(~Sex+Age+propNeuron, data = data_m)
# design <- model.matrix(~Sex+Age+CD8T+CD4T+NK+Bcell+Gran, data = data_m)
# design <- model.matrix(~Sex+Age+CD8T+CD4T+NK+Bcell+Gran, data = data_beta)
# design <- model.matrix(~Sex+Age, data = data_beta)
design <- model.matrix(~Sex+Age+propNeuron, data = data_beta)


head(design)
#fit <- lmFit(data_m, design)
fit <- lmFit(data_beta, design)
fit2 <- eBayes(fit)
topl1_Sex <- topTable(fit2, num=Inf,coef="SexM",sort.by="none")
colnames(topl1_Sex) <- paste0("Sex_",colnames(topl1_Sex))
topl1_Age <- topTable(fit2, num=Inf,coef="Age",sort.by="none")
colnames(topl1_Age) <- paste0("Age_",colnames(topl1_Age))
table(rownames(topl1_Sex)==rownames(topl1_Age))
results <- data.frame(topl1_Sex,topl1_Age)

write.table(data.frame(results),file=paste(gse, "_beta.txt", sep=''),col.name=TRUE, row.names=TRUE,sep="\t",quote=F)

# In case we decide to use M values, we have to find good thresholds; just as an example
dim(results[abs(results$Age_logFC)>0.001 & results$Age_adj.P.Val<0.01,])
dim(results[abs(results$Sex_logFC)>0.01 & results$Sex_adj.P.Val<0.01,])
