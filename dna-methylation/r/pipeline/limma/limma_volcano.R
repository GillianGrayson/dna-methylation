rm(list=ls())

if (!requireNamespace("BiocManager", quietly=TRUE))
  install.packages("BiocManager")

BiocManager::install('EnhancedVolcano')
install.packages("readxl", dependencies = TRUE, INSTALL_opts = '--no-lock')
library(EnhancedVolcano)
library(readxl)

path <- "E:/YandexDisk/Work/pydnameth/methylation_and_proteomic/limma/GSE74193"
setwd(path)

data <- read_excel(paste(path, "/GSE74193_betas_filtered.xlsx",  sep=''))

EnhancedVolcano(data,
                lab = data$UCSC_REFGENE_NAME,
                x = 'Sex_logFC',
                y = 'Sex_P.Value_fdr_bh',
                pCutoff = 0.001,
                FCcutoff = 0.1)

