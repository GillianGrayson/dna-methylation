rm(list=ls())

library(minfi)
library(limma)

path <- "E:/YandexDisk/Work/pydnameth/unn_epic/limma"
setwd(path)

dataset <- read.table(
  paste("E:/YandexDisk/Work/pydnameth/unn_epic/betas_norm(fun)_part(wo_noIntensity_detP).txt",  sep=''),
  header = TRUE,
  sep = "\t"
  )
rownames(dataset) <- dataset[,1]
dataset <- dataset[,-1]

obs<-read.table("E:/YandexDisk/Work/pydnameth/unn_epic/observables_part(wo_noIntensity_detP).txt", header=TRUE, sep= "\t")
table(colnames(dataset)==obs$BetaColumns)

Sample_Group <- obs$Sample_Group
Sex <- obs$Sex
Age <- obs$Age

cells<-read.table("E:/YandexDisk/Work/pydnameth/unn_epic/cell_counts_part(wo_noIntensity_detP).txt", header=TRUE, sep= "\t")

Bcell = cells$Bcell
CD4T = cells$CD4T
CD8T = cells$CD8T
Neu = cells$Neu
NK = cells$NK

design <- model.matrix(~Sample_Group+Sex+Age+Bcell+CD4T+CD8T+Neu+NK, data = dataset)
head(design)

fit <- lmFit(dataset, design)
eb <- eBayes(fit)
cov_names = colnames(eb[["coefficients"]])
cov_names

topl1_group <- topTable(eb, num=Inf,coef="Sample_GroupT",sort.by="none")
colnames(topl1_group) <- paste0("Sample_Group_",colnames(topl1_group))
res = data.frame(topl1_group)

write.csv(res, paste(path, "/", "Sample_Group.csv",  sep=''), row.names = TRUE)

topl1_Age <- topTable(fit2, num=Inf,coef="Age",sort.by="none")
colnames(topl1_Age) <- paste0("Age_",colnames(topl1_Age))
table(rownames(topl1_Sex)==rownames(topl1_Age))
results <- data.frame(topl1_Sex,topl1_Age)
