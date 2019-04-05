rm(list=ls())
library(minfi)
source("https://bioconductor.org/biocLite.R")
biocLite("FlowSorted.Blood.450k")

nodename <- Sys.info()[[4]]
if (nodename == "MSI"){
  root_path <- "D:/YandexDisk/Work/pydnameth"
} else if (nodename == "DESKTOP-K9VO2TI"){
  root_path <- "E:/YandexDisk/Work/pydnameth"
} else {
  root_path <- getwd()
}


# ====== Parameters: =======
dataset <- "test"
calc_cell_counts = TRUE
# ==========================

raw_path <- "raw"
setwd(paste(root_path, "/", dataset, "/", raw_path, sep=''))
input_data_path <- "raw/input_data"

RGset_fn <- paste(root_path, "/", dataset, "/", raw_path, "/", "RGset.RData",  sep='')
if (!file.exists(RGset_fn)){
  # Setting up targets
  baseDir <- paste(root_path, "/", dataset, "/", input_data_path, sep='')
  list.files(baseDir)
  targets <- read.metharray.sheet(baseDir)
  RGset <- read.metharray.exp(targets = targets)
  save(RGset,file=RGset_fn)
} else {
  load(RGset_fn)
}

if (calc_cell_counts){
  CellCounts_fn <- paste(root_path, "/", dataset, "/", raw_path, "/", "RCellCounts.RData",  sep='')
  if (!file.exists(RGset_fn)){
    CellCounts <- estimateCellCounts(RGset)
    
  }
}

CellCounts <- estimateCellCounts(RGset)
save(CellCounts,file="GSE87571_CellCounts.RData")
load("GSE87571_CellCounts.RData")
ls()
head(CellCounts)
list.files()

MSet_Raw <- preprocessRaw(RGset)

green <- getGreen(RGset)
red <- getRed(RGset)
beta <- getBeta(RGset)

pdf("GSE87571_boxplots_intensities.pdf",width=15,height=5)
par(mfrow=c(3,1))
boxplot(green,outline=F)
boxplot(red,outline=F)
boxplot(beta,outline=F)
dev.off()

# Controlli di qualità
# qcplot
qc <- getQC(MSet_Raw)
pdf("GSE87571_QCplot.pdf")
plotQC(qc)
dev.off()

funnorm <- preprocessFunnorm(RGset)
beta_funnorm <- getBeta(funnorm)
pdf("GSE87571_boxplots_beta_Funnorm.pdf",width=15,height=5)
par(mfrow=c(2,1))
boxplot(beta,outline=F,main="No Normalization")
boxplot(beta_funnorm,outline=F,main="Funnorm Normalization")
dev.off()

beta_funnorm <- data.frame(row.names(beta_funnorm),beta_funnorm)
colnames(beta_funnorm)[1] <- "ID_REF"
dim(beta_funnorm)
str(beta_funnorm)
getwd()
save(beta_funnorm,file="GSE87571_beta_funnorm.RData")
write.table(beta_funnorm,file="GSE87571_beta_funnorm.txt",row.names=F,sep="\t",quote=F)
