rm(list=ls())
library(parallel)
load("/home/mgbacalini/EPIC_PROPAGAGEING_ADAGE_DIAB_gennaio_2019/PROPAGAGEING_ADAGE_DIAB_Beta_Funnorm_filtered_post_combat_Zhou_probesfiltered.RData")
SampleSheet <- read.csv("/home/mgbacalini/EPIC_PROPAGAGEING_ADAGE_DIAB_gennaio_2019/EPIC_PROPAGAGEING_ADAGE_DIAB_starting_samplesheet_noKI.csv",sep=",",quote="",header=T)
ls()
data.temp <- combat_data_filtered
dim(data.temp)
str(data.temp)
data.temp <- data.temp[,colnames(data.temp) %in% paste("X",SampleSheet$Basename,sep="")]
dim(data.temp)
data.temp <- data.frame(rownames(data.temp), data.temp)
colnames(data.temp)[1] <- "ID_REF"
dim(data.temp)
str(data.temp)

table(colnames(data.temp)[2:312]== paste("X",SampleSheet$Basename,sep=""))

load("/home/mgbacalini/ANNOTATION_INFINIUM/annotationsEPIC.RData")
data <- merge(data.temp,annotationsEPIC,by="ID_REF")
dim(data)

# NA removal
data_noNA <- data[rowSums(is.na(data[,2:312]))==0,]

# CHRX and CHRY removal
data_noNA_noXY <- subset(data_noNA,data_noNA$CHR!="X"&data_noNA$CHR!="Y") 
data_noNA_noXY <- droplevels(data_noNA_noXY)
input <- data_noNA_noXY

CTR <- SampleSheet[SampleSheet$Group=="CTR_GENERAL","Basename"]
CTR <-paste("X",CTR,sep="")







betas = read.table("E:/YandexDisk/Work/pydnameth/GSE87571/cpg_beta.txt", header = TRUE, sep = "\t", nrows = 10)
CpG = betas[,1]
betas_d = betas[, 2:730]
input_CTR = betas_d
input2 <- data.frame(betas, results)
colnames(input2) <- c(colnames(betas),c("Q1","Q3","IQR"))
CpG <- input2[,1]
EpimutationsResults <- lapply(CpG, function(x) EpimutationsFunction(x))
write.table(EpimutationsResults, "asdasd.csv", sep = ",", dec = ".", row.names = FALSE, col.names = FALSE)
save(EpimutationsResults,file="EpimutationsResults_TEMP.RData")





input_CTR <-input[,colnames(input) %in% CTR]

QuantileFunction <- function(x) {
  q1 <- quantile(x)[2]
  q3 <- quantile(x)[4]
  iqr <- IQR(x)
  return(c(q1,q3,iqr))
}

results <- apply(input_CTR,1,QuantileFunction)
results <- t(results)
head(results)

input2 <- data.frame(input,results)
dim(input)
dim(input2)
colnames(input2) <- c(colnames(input),c("Q1","Q3","IQR"))
str(input2[,361:364])

EpimutationsFunction <- function(x) {
  Q1 <- input2[input2$ID_REF==x,"Q1"]
  Q3 <- input2[input2$ID_REF==x,"Q3"]
  IQR <- input2[input2$ID_REF==x,"IQR"]
  dat <- input2[input2$ID_REF==x,c(2:730)]
  condition <- dat<(Q1-(IQR*3))  | dat>(Q3+(IQR*3))
  return(condition)
}

CpG <- input2[,1]
EpimutationsResults <- mclapply(CpG,function(x) EpimutationsFunction(x),mc.cores=25,mc.preschedule=TRUE)
save(EpimutationsResults,file="EpimutationsResults_TEMP.RData")
EpimutationsResults <- data.frame(matrix(unlist(EpimutationsResults), nrow=length(CpG), byrow=T))
head(EpimutationsResults)
EpimutationsResults <- data.frame(input2[,1],EpimutationsResults)
head(EpimutationsResults)
colnames(EpimutationsResults) <- c("ID_REF",colnames(input2)[2:312])
head(EpimutationsResults)
save(EpimutationsResults,file="PROPAGAGEING_ADAGE_EpimutationsResults.RData")