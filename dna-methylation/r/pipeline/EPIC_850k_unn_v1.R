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

path <- "E:/YandexDisk/Work/pydnameth/unn_epic/raw/data"
setwd(path)

myLoad = champ.load(directory = path, arraytype = "EPIC")
passed_cpgs_origin = rownames(myLoad$beta)
targets <- read.metharray.sheet(path)
RGset <- read.metharray.exp(targets = targets)

funnorm <- preprocessFunnorm(RGset)
beta_funnorm <- getBeta(funnorm)

passed_cpgs = intersect(passed_cpgs_origin, rownames(beta_funnorm))
beta_funnorm_filtered <- beta_funnorm[passed_cpgs,]

beta_funnorm_filtered_df <- data.frame(row.names(beta_funnorm_filtered),beta_funnorm_filtered)
colnames(beta_funnorm_filtered_df)[1] <- "IlmnID"









beta_raw_filtered = beta_raw[passed_cpgs,]

pdf("boxplots_beta_raw_filtered.pdf",width=15,height=5)
par(mfrow=c(1,1))
boxplot(beta_raw_filtered,outline=F,main="No Normalization")
dev.off()

pdf("densityPlot_raw_filtered.pdf")
densityPlot(beta_raw_filtered, sampGroups = targets$Sample_Group)
dev.off()




passed_cpgs = intersect(passed_cpgs_origin, rownames(beta_funnorm))
beta_funnorm_filtered <- beta_funnorm[passed_cpgs,]

pdf("boxplots_beta_Funnorm_filtered.pdf",width=15,height=5)
par(mfrow=c(1,1))
boxplot(beta_funnorm_filtered,outline=F,main="Funnorm Normalization")
dev.off()

pdf("densityPlot_Funnorm_filtered.pdf")
densityPlot(beta_funnorm_filtered, sampGroups = targets$Sample_Group)
dev.off()

beta_funnorm_filtered_df <- data.frame(row.names(beta_funnorm_filtered),beta_funnorm_filtered)
colnames(beta_funnorm_filtered_df)[1] <- "IlmnID"
write.table(beta_funnorm_filtered_df,file="beta_funnorm_filtered.txt",row.names=F,sep="\t",quote=F)





write.csv(data.frame(myLoad$beta), "beta_filtered.csv", row.names = TRUE)

myImport = champ.import(directory = path, arraytype = "EPIC")

beta_raw = data.frame(myImport$beta)
write.table(beta_raw, file="beta_raw.txt",col.name=TRUE, row.names=TRUE,sep="\t",quote=F)
write.csv(beta_raw, "beta_raw.csv", row.names = FALSE)

myLoad <- champ.filter(arraytype="EPIC")

champ.QC()

QC.GUI(beta=myLoad$beta,arraytype="EPIC")

myNorm <- champ.norm(beta=myLoad$beta,
                     rgSet=myLoad$rgSet,
                     mset=myLoad$mset,
                     method="BMIQ",
                     arraytype="EPIC")
myNorm <- champ.norm(beta=myLoad$beta,
                     rgSet=myLoad$rgSet,
                     mset=myLoad$mset,
                     method="FunctionalNormalization",
                     arraytype="EPIC")

champ.QC(beta = myNorm,
         pheno=myLoad$pd$Sample_Group,
         mdsPlot=TRUE,
         densityPlot=TRUE,
         dendrogram=TRUE,
         PDFplot=TRUE,
         Rplot=TRUE,
         Feature.sel="None",
         resultsDir="./CHAMP_QCimages_normed/")

QC.GUI(beta=myNorm,arraytype="EPIC")

beta_filtered_normalized = data.frame(row.names(myNorm), myNorm)
colnames(beta_filtered_normalized)[1] <- "IlmnID"
write.table(beta_filtered_normalized,file="beta_filtered_normalized.txt",col.name=TRUE, row.names=FALSE,sep="\t",quote=F)

pdf("boxplots_beta_BMIQ.pdf",width=15,height=5)
par(mfrow=c(1,1))
boxplot(myNorm,outline=F,main="BMIQ Normalization")
dev.off()

pdf("densityPlot_BMIQ.pdf")
targets <- read.metharray.sheet(path)
densityPlot(myNorm, sampGroups = targets$Sample_Group)
dev.off()

#write.table(data.frame(EPIC.manifest.hg19),file="EPIC.manifest.hg19.txt",col.name=TRUE, row.names=TRUE,sep="\t",quote=F)

champ.SVD(beta=myNorm,pd=myLoad$pd)

myCombat <- champ.runCombat(beta=myNorm, pd=myLoad$pd, batchname=c("Slide"))

write.table(data.frame(beta_filtered_normalized),file="beta_filtered_normalized_combat.txt",col.name=TRUE, row.names=TRUE,sep="\t",quote=F)




# Cells ===========================================================================================================
rm(list=ls())

if (!requireNamespace("BiocManager", quietly = TRUE))
  install.packages("BiocManager")
BiocManager::install("minfi")
BiocManager::install("FlowSorted.Blood.EPIC")

library(minfi)
library(FlowSorted.Blood.EPIC)

path <- "E:/YandexDisk/Work/pydnameth/unn_epic/raw/data"
setwd(path)

list.files(path)
targets <- read.metharray.sheet(path)
RGset <- read.metharray.exp(targets = targets)
cell_counts <- estimateCellCounts2(RGset,
                                   compositeCellType = "Blood",
                                   processMethod = "preprocessFunnorm", 
                                   referencePlatform="IlluminaHumanMethylationEPIC")
write.csv(cell_counts, "cell_counts.csv")
# =================================================================================================================


# minfi ===========================================================================================================
rm(list=ls())

if (!requireNamespace("BiocManager", quietly = TRUE))
  install.packages("BiocManager")
BiocManager::install("minfi")
BiocManager::install("minfiData")
BiocManager::install("wateRmelon")
BiocManager::install("shinyMethyl")
BiocManager::install("FlowSorted.Blood.EPIC")
BiocManager::install("ChAMP")

library("ChAMP")
library(minfi)
library(minfiData)
library(shinyMethyl)
library(wateRmelon)
library(FlowSorted.Blood.EPIC)

path <- "E:/YandexDisk/Work/pydnameth/unn_epic/raw/data"
setwd(path)

list.files(path)
targets <- read.metharray.sheet(path)
RGset <- read.metharray.exp(targets = targets)

RGset <- myLoad$rgSet

detP <- detectionP(RGset)
write.csv(data.frame(detP), "detP.csv", row.names = FALSE)
threshold <- 0.01
failed <- summary(detP>threshold)
failed <- data.frame(failed)
failed <- failed[seq(3,nrow(failed),3),2:3]
colnames(failed) <- c("Sample",paste("Number of probes (detP>",threshold,")",sep=''))
write.csv(failed, "failed.csv", row.names = FALSE)
failed

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
         sampGroups = targets$Sample_Group, 
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

MSet_raw <- preprocessRaw(RGset)
green <- getGreen(RGset)
red <- getRed(RGset)
beta_raw <- getBeta(RGset)

champ.QC(beta = beta_raw,
         pheno=targets$Sample_Group,
         mdsPlot=TRUE,
         densityPlot=TRUE,
         dendrogram=TRUE,
         PDFplot=TRUE,
         Rplot=TRUE,
         Feature.sel="None",
         resultsDir="./fun/")

QC.GUI(beta=beta_raw,arraytype="EPIC",pheno=targets$Sample_Group)

pdf("densityPlot_raw.pdf")
densityPlot(beta_raw, sampGroups = targets$Sample_Group)
dev.off()

pdf("densityPlot_raw_filtered.pdf")
densityPlot(myLoad$beta, sampGroups = targets$Sample_Group)
dev.off()

pdf("boxplots_intensities.pdf", width=15, height=5)
par(mfrow=c(3,1))
boxplot(green,outline=F)
boxplot(red,outline=F)
boxplot(beta_raw,outline=F)
dev.off()

pdf("red_intensities.pdf", width=15, height=5)
par(mfrow=c(1,1))
boxplot(red,outline=F)
dev.off()

pdf("green_intensities.pdf", width=15, height=5)
par(mfrow=c(1,1))
boxplot(green,outline=F)
dev.off()

qc <- getQC(MSet_raw)
pdf("QCplot.pdf")
plotQC(qc)
dev.off()

pdf("boxplots_beta_Raw.pdf",width=15,height=5)
par(mfrow=c(1,1))
boxplot(beta_raw,outline=F,main="No Normalization")
dev.off()
# =================================================================================================================

# preprocessFunnorm ===============================================================================================
funnorm <- preprocessFunnorm(RGset)

beta_funnorm <- getBeta(funnorm)

pdf("boxplots_beta_Funnorm.pdf",width=15,height=5)
par(mfrow=c(1,1))
boxplot(beta_funnorm,outline=F,main="Funnorm Normalization")
dev.off()

pdf("densityPlot_Funnorm.pdf")
densityPlot(beta_funnorm, sampGroups = targets$Sample_Group)
dev.off()

champ.QC(beta = beta_funnorm,
         pheno=targets$Sample_Group,
         mdsPlot=TRUE,
         densityPlot=TRUE,
         dendrogram=TRUE,
         PDFplot=TRUE,
         Rplot=TRUE,
         Feature.sel="None",
         resultsDir="./fun/")

QC.GUI(beta=beta_funnorm,arraytype="EPIC")

beta_funnorm_df <- data.frame(row.names(beta_funnorm),beta_funnorm)
colnames(beta_funnorm_df)[1] <- "IlmnID"
write.table(beta_funnorm_df,file="beta_funnorm.txt",row.names=F,sep="\t",quote=F)
# =================================================================================================================

# preprocessQuantile ===============================================================================================
quantile <- preprocessQuantile(RGset)

beta_quantile <- getBeta(quantile)

pdf("boxplots_beta_quantile.pdf",width=15,height=5)
par(mfrow=c(1,1))
boxplot(beta_quantile,outline=F,main="Quantile Normalization")
dev.off()

pdf("densityPlot_Quantile.pdf")
densityPlot(beta_quantile, sampGroups = targets$Sample_Group)
dev.off()

champ.QC(beta = beta_quantile,
         pheno=targets$Sample_Group,
         mdsPlot=TRUE,
         densityPlot=TRUE,
         dendrogram=TRUE,
         PDFplot=TRUE,
         Rplot=TRUE,
         Feature.sel="None",
         resultsDir="./fun/")

QC.GUI(beta=beta_quantile,arraytype="EPIC")

beta_quantile_df <- data.frame(row.names(beta_quantile),beta_quantile)
colnames(beta_quantile_df)[1] <- "IlmnID"
write.table(beta_quantile_df,file="beta_quantile.txt",row.names=F,sep="\t",quote=F)
# =================================================================================================================



# Filtered analysis ===============================================================================================
myLoad = champ.load(directory = path, method="minfi", arraytype = "EPIC")
passed_cpgs_origin = rownames(myLoad$beta)

passed_cpgs = intersect(passed_cpgs_origin, rownames(beta_raw))
beta_raw_filtered = beta_raw[passed_cpgs,]

pdf("boxplots_beta_raw_filtered.pdf",width=15,height=5)
par(mfrow=c(1,1))
boxplot(beta_raw_filtered,outline=F,main="No Normalization")
dev.off()

pdf("densityPlot_raw_filtered.pdf")
densityPlot(beta_raw_filtered, sampGroups = targets$Sample_Group)
dev.off()




passed_cpgs = intersect(passed_cpgs_origin, rownames(beta_funnorm))
beta_funnorm_filtered <- beta_funnorm[passed_cpgs,]

pdf("boxplots_beta_Funnorm_filtered.pdf",width=15,height=5)
par(mfrow=c(1,1))
boxplot(beta_funnorm_filtered,outline=F,main="Funnorm Normalization")
dev.off()

pdf("densityPlot_Funnorm_filtered.pdf")
densityPlot(beta_funnorm_filtered, sampGroups = targets$Sample_Group)
dev.off()

beta_funnorm_filtered_df <- data.frame(row.names(beta_funnorm_filtered),beta_funnorm_filtered)
colnames(beta_funnorm_filtered_df)[1] <- "IlmnID"
write.table(beta_funnorm_filtered_df,file="beta_funnorm_filtered.txt",row.names=F,sep="\t",quote=F)




passed_cpgs = intersect(passed_cpgs_origin, rownames(beta_quantile))
beta_quantile_filtered <- beta_quantile[passed_cpgs,]

pdf("boxplots_beta_quantile_filtered.pdf",width=15,height=5)
par(mfrow=c(1,1))
boxplot(beta_quantile_filtered,outline=F,main="Quantile Normalization")
dev.off()

pdf("densityPlot_quantile_filtered.pdf")
densityPlot(beta_quantile_filtered, sampGroups = targets$Sample_Group)
dev.off()

beta_quantile_filtered_df <- data.frame(row.names(beta_quantile_filtered),beta_quantile_filtered)
colnames(beta_quantile_filtered_df)[1] <- "IlmnID"
write.table(beta_quantile_filtered_df,file="beta_quantile_filtered",row.names=F,sep="\t",quote=F)

