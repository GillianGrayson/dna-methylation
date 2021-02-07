rm(list=ls())
library(minfi)
load("/Users/digitalhandicrafts/Downloads/GSE74193.RData")

# the input should be a dataframe of methylation values; limma should work better with M values, try to convert beta values in M and launch limma first on M values and then on beta values
data <- GSE74193
rownames(data) <- data[,1]
data <- data[,-1]
data_Mvalues <- ilogit2(data)
ss <- read.table("/Users/digitalhandicrafts/Dropbox/Brain_Aging/Brain_datasets_condiviso_Camilla_ok/Horvath_propNeuron/ss_propNeuron/GSE74193Header_OK_propNeuron.txt",header=T,sep="\t",stringsAsFactors = T)
str(ss)

table(colnames(data_Mvalues)==ss$Sample)

Sex <- ss$Sex
Age <- ss$Age
#...add the covariates, for example here I use
propNeuron <- ss$propNeuron
#etc...

library(limma)
design <- model.matrix(~Sex+Age+propNeuron, data= data_Mvalues)
head(design)
fit <- lmFit(data_Mvalues, design)
fit2 <- eBayes(fit)
topl1_Sex <- topTable(fit2, num=Inf,coef="SexM",sort.by="none")
colnames(topl1_Sex) <- paste0("Sex_",colnames(topl1_Sex))
topl1_Age <- topTable(fit2, num=Inf,coef="Age",sort.by="none")
colnames(topl1_Age) <- paste0("Age_",colnames(topl1_Age))
table(rownames(topl1_Sex)==rownames(topl1_Age))
results <- data.frame(topl1_Sex,topl1_Age)

# In case we decide to use M values, we have to find good thresholds; just as an example
dim(results[abs(results$Age_logFC)>0.0005 & results$Age_adj.P.Val<0.05,])
dim(results[abs(results$Sex_logFC)>0.01 & results$Sex_adj.P.Val<0.05,])

