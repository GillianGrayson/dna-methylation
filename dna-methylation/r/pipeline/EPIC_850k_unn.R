rm(list=ls())

if (!requireNamespace("BiocManager", quietly=TRUE))
  install.packages("BiocManager")
BiocManager::install("ChAMP")

library("ChAMP")

path <- "E:/YandexDisk/Work/pydnameth/unn_epic/raw/data"
setwd(path)

myLoad = champ.load(directory = path, arraytype = "EPIC")
myLoad = champ.load(directory = path, method="minfi", arraytype = "EPIC")
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

beta_filtered_normalized = data.frame(myNorm)
write.table(beta_filtered_normalized,file="beta_filtered_normalized.txt",col.name=TRUE, row.names=TRUE,sep="\t",quote=F)

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

qcReport(RGset, 
         sampGroups = targets$Sample_Group, 
         pdf = "qcReport.pdf", 
         controls = c("NEGATIVE", "BISULFITE CONVERSION I", "BISULFITE CONVERSION II", "EXTENSION", "HYBRIDIZATION", "NON-POLYMORPHIC", "SPECIFICITY I", "SPECIFICITY II", "TARGET REMOVAL"))

MSet_raw <- preprocessRaw(RGset)
green <- getGreen(RGset)
red <- getRed(RGset)
beta_raw <- getBeta(RGset)

pdf("boxplots_intensities.pdf", width=15, height=5)
par(mfrow=c(3,1))
boxplot(green,outline=F)
boxplot(red,outline=F)
boxplot(beta_raw,outline=F)
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
dim(beta_funnorm)
pdf("boxplots_beta_Funnorm.pdf",width=15,height=5)
par(mfrow=c(1,1))
boxplot(beta_funnorm,outline=F,main="Funnorm Normalization")
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