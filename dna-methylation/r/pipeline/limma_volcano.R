rm(list=ls())

if (!requireNamespace("BiocManager", quietly=TRUE))
  install.packages("BiocManager")
BiocManager::install("ChAMP")
BiocManager::install("minfi")
BiocManager::install("minfiData")
BiocManager::install("wateRmelon")
BiocManager::install("shinyMethyl")
BiocManager::install("FlowSorted.Blood.EPIC")

library(ChAMP)
library(minfi)
library(minfiData)
library(shinyMethyl)
library(wateRmelon)
library(FlowSorted.Blood.EPIC)

path <- "E:/YandexDisk/Work/pydnameth/script_datasets/GPL13534/filtered/brain(DLPFC)/GSE74193/raw_data"
setwd(path)

myLoad = champ.load(directory = path, method="minfi", arraytype = "450k")
passed_cpgs_origin = rownames(myLoad$beta)

RGset <- myLoad$rgSet

# QC ==========================================================================
h = 5

pdf("NEGATIVE.pdf", width = 10, height = h)
controlStripPlot(RGset, controls="NEGATIVE")
dev.off()

pdf("BISULFITE CONVERSION I.pdf", width = 10, height = h)
controlStripPlot(RGset, controls="BISULFITE CONVERSION I")
dev.off()

pdf("BISULFITE CONVERSION II.pdf", width = 10, height = h)
controlStripPlot(RGset, controls="BISULFITE CONVERSION II")
dev.off()

pdf("EXTENSION.pdf", width = 10, height = h)
controlStripPlot(RGset, controls="EXTENSION")
dev.off()

pdf("HYBRIDIZATION.pdf", width = 10, height = h)
controlStripPlot(RGset, controls="HYBRIDIZATION")
dev.off()

pdf("NON-POLYMORPHIC.pdf", width = 10, height = h)
controlStripPlot(RGset, controls="NON-POLYMORPHIC")
dev.off()

pdf("SPECIFICITY I.pdf", width = 10, height = h)
controlStripPlot(RGset, controls="SPECIFICITY I")
dev.off()

pdf("SPECIFICITY II.pdf", width = 10, height = h)
controlStripPlot(RGset, controls="SPECIFICITY II")
dev.off()

pdf("TARGET REMOVAL.pdf", width = 10, height = h)
controlStripPlot(RGset, controls="TARGET REMOVAL")
dev.off()

qcReport(RGset,
         sampGroups = myLoad$pd$Sample_Group, 
         pdf = "qcReport.pdf", 
         controls = c("NEGATIVE",
                      "BISULFITE CONVERSION I",
                      "BISULFITE CONVERSION II",
                      "EXTENSION",
                      "HYBRIDIZATION",
                      "NON-POLYMORPHIC",
                      "SPECIFICITY I",
                      "SPECIFICITY II",
                      "TARGET REMOVAL"
         )
)


qc <- getQC(myLoad$mset)
pdf("QCplot.pdf")
plotQC(qc)
dev.off()

# Raw =========================================================================
pdf("density_raw.pdf")
densityPlot(myLoad$beta, sampGroups = myLoad$pd$Sample_Group)
dev.off()

pdf("boxplot_raw.pdf",width=15,height=5)
par(mfrow=c(1,1))
boxplot(myLoad$beta, outline=F, main="No Normalization")
dev.off()

# funnorm =====================================================================
funnorm <- preprocessFunnorm(RGset)
beta_funnorm <- getBeta(funnorm)

passed_cpgs = intersect(passed_cpgs_origin, rownames(beta_funnorm))
beta_funnorm_filtered <- beta_funnorm[passed_cpgs,]

pdf("boxplots_funnorm.pdf",width=15,height=5)
par(mfrow=c(1,1))
boxplot(beta_funnorm_filtered,outline=F,main="Funnorm Normalization")
dev.off()

pdf("density_funnorm.pdf")
densityPlot(beta_funnorm_filtered, sampGroups = myLoad$pd$Sample_Group)
dev.off()

beta_funnorm_filtered_df <- data.frame(row.names(beta_funnorm_filtered),beta_funnorm_filtered)
colnames(beta_funnorm_filtered_df)[1] <- "IlmnID"
write.table(beta_funnorm_filtered_df,file="beta_funnorm_filtered.txt",row.names=F,sep="\t",quote=F)

# quantile =====================================================================
quantile <- preprocessQuantile(RGset)
beta_quantile <- getBeta(quantile)

passed_cpgs = intersect(passed_cpgs_origin, rownames(beta_quantile))
beta_quantile_filtered <- beta_quantile[passed_cpgs,]

pdf("boxplots_quantile.pdf",width=15,height=5)
par(mfrow=c(1,1))
boxplot(beta_quantile_filtered,outline=F,main="Quantile Normalization")
dev.off()

pdf("density_quantile.pdf")
densityPlot(beta_quantile_filtered, sampGroups = myLoad$pd$Sample_Group)
dev.off()

beta_quantile_filtered_df <- data.frame(row.names(beta_quantile_filtered),beta_quantile_filtered)
colnames(beta_quantile_filtered_df)[1] <- "IlmnID"
write.table(beta_quantile_filtered_df,file="beta_quantile_filtered",row.names=F,sep="\t",quote=F)

# BMIQ =====================================================================
myNorm <- champ.norm(beta=myLoad$beta,
                     rgSet=myLoad$rgSet,
                     mset=myLoad$mset,
                     method="BMIQ",
                     arraytype="450k")

beta_filtered_normalized = data.frame(row.names(myNorm), myNorm)
colnames(beta_filtered_normalized)[1] <- "IlmnID"
write.table(beta_filtered_normalized,file="beta_BMIQ_filtered.txt",col.name=TRUE, row.names=FALSE,sep="\t",quote=F)

