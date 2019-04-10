rm(list=ls())
library(minfi)
source("https://bioconductor.org/biocLite.R")
biocLite("FlowSorted.Blood.450k")

# ====== Parameters =======
dataset <- "test"
calc_cell_counts = TRUE
raw_analysis = TRUE
funnorm_analysis = TRUE
# =========================

# ====== File system =======
nodename <- Sys.info()[[4]]
if (nodename == "MSI"){
  root_path <- "D:/YandexDisk/Work/pydnameth"
} else if (nodename == "DESKTOP-K9VO2TI"){
  root_path <- "E:/YandexDisk/Work/pydnameth"
} else {
  root_path <- getwd()
}

raw_path <- "raw"
setwd(paste(root_path, "/", dataset, "/", raw_path, sep=''))
raw_rg_path <- "raw/rg"
# ==========================

# ======= RGset ========
RGset_fn <- paste(root_path, "/", dataset, "/", raw_path, "/", "RGset.RData",  sep='')
if (!file.exists(RGset_fn)){
  # Setting up targets
  baseDir <- paste(root_path, "/", dataset, "/", raw_rg_path, sep='')
  list.files(baseDir)
  targets <- read.metharray.sheet(baseDir)
  RGset <- read.metharray.exp(targets = targets)
  save(RGset,file=RGset_fn)
} else {
  load(RGset_fn)
}
# ======================

# ======= CellCounts ======
if (calc_cell_counts){
  CellCounts_fn <- paste(root_path, "/", dataset, "/", raw_path, "/", "CellCounts.RData",  sep='')
  if (!file.exists(CellCounts_fn)){
    CellCounts <- estimateCellCounts(RGset)
  }
  else{
    load(CellCounts_fn)
  }
}
# =========================

# ======== preprocessRaw =========
if (raw_analysis){
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
  
  pdf("boxplots_beta_raw.pdf",width=15,height=5)
  par(mfrow=c(1,1))
  boxplot(beta_raw,outline=F,main="No Normalization")
  dev.off()
}
# ===============================

# ======== preprocessFunnorm =========
if (funnorm_analysis){
  funnorm <- preprocessFunnorm(RGset)
  beta_funnorm <- getBeta(funnorm)
  
  pdf("boxplots_beta_funnorm.pdf",width=15,height=5)
  par(mfrow=c(1,1))
  boxplot(beta_funnorm,outline=F,main="Funnorm Normalization")
  dev.off()
  
  beta_funnorm <- data.frame(row.names(beta_funnorm),beta_funnorm)
  colnames(beta_funnorm)[1] <- "ID_REF"
  save(beta_funnorm,file="beta_funnorm.RData")
  write.table(beta_funnorm,file="beta_funnorm.txt",row.names=F,sep="\t",quote=F)
}
