rm(list=ls())

setwd("D:/Work/dna-methylation/dna-methylation/r/fisher")
database = "GSE87571"
fn_all = "D:/YandexDisk/Work/pydnameth/GSE87571/betas/table/aggregator/d1bf8fe4acc69f65972ad2e2300002cf/default.csv"
fn_target = ""D:/YandexDisk/Work/pydnameth/draft/tables/v1/GSE87571.csv""

all_cpgs = read.csv(fn_all, header = TRUE)
target_cpgs = read.csv(fn_target, header = TRUE)

load("D:/YandexDisk/Work/MG/2/Illumina450Manifest.RData")

all_data = Illumina450Manifest[Illumina450Manifest$IlmnID %in% all_cpgs$item,]
all_data = droplevels(all_data)
target_data = Illumina450Manifest[Illumina450Manifest$IlmnID %in% target_cpgs$item,]
target_data = droplevels(target_data)

# ======= UCSC_RefGene_Group ========
all_groups = as.character(all_data$UCSC_RefGene_Group)
all_freq = list()
for (all_group_raw in all_groups){
  if (all_group_raw != ""){
    groups = unique(strsplit(as.character(all_group_raw), ";")[[1]])
  }
  else{
    groups = "NA"
  }
  for (i in 1:length(groups)){
    group = groups[[i]]
    if (group %in% names(all_freq)){
      all_freq[[group]] = all_freq[[group]] + 1
    }
    else{
      all_freq[[group]] = 1
    }
  }
}
all_freq = data.frame(group=names(all_freq), all_total=as.numeric(paste(unlist(all_freq))))

target_groups = as.character(target_data$UCSC_RefGene_Group)
target_freq = list()
for (group_raw in target_groups){
  if (group_raw != ""){
    groups = unique(strsplit(as.character(group_raw), ";")[[1]])
  }
  else{
    groups = "NA"
  }
  for (i in 1:length(groups)){
    group = groups[[i]]
    if (group %in% names(target_freq)){
      target_freq[[group]] = target_freq[[group]] + 1
    }
    else{
      target_freq[[group]] = 1
    }
  }
}
target_freq = data.frame(group=names(target_freq), target_total=as.numeric(paste(unlist(target_freq))))
table_group = merge(target_freq, all_freq, by="group")
table_group$TARGET_TOT <- rep(sum(table_group[,2]),nrow(table_group))
table_group$ALL_TOT <- rep(sum(table_group[,3]),nrow(table_group))


# ======= CHR ========
all_table_CHR = data.frame(table(all_data$CHR))
colnames(all_table_CHR) <- c("CHR", "ALL")
all_table_Relation_to_UCSC_CpG_Island = data.frame(table(all_data$Relation_to_UCSC_CpG_Island))
colnames(all_table_Relation_to_UCSC_CpG_Island) <- c("Relation_to_UCSC_CpG_Island", "ALL")

target_table_CHR = data.frame(table(target_data$CHR))
colnames(target_table_CHR) <- c("CHR", "TARGET")
target_table_Relation_to_UCSC_CpG_Island = data.frame(table(target_data$Relation_to_UCSC_CpG_Island))
colnames(target_table_Relation_to_UCSC_CpG_Island) <- c("Relation_to_UCSC_CpG_Island", "TARGET")

table_CHR <- merge(target_table_CHR, all_table_CHR, by="CHR")
table_CHR$TARGET_TOT <- rep(sum(table_CHR[,2]),nrow(table_CHR))
table_CHR$ALL_TOT <- rep(sum(table_CHR[,3]),nrow(table_CHR))


# ======= Relation_to_UCSC_CpG_Island ========
table_Relation_to_UCSC_CpG_Island <- merge(target_table_Relation_to_UCSC_CpG_Island, all_table_Relation_to_UCSC_CpG_Island, by="Relation_to_UCSC_CpG_Island")
table_Relation_to_UCSC_CpG_Island$TARGET_TOT <- rep(sum(table_Relation_to_UCSC_CpG_Island[,2]),nrow(table_Relation_to_UCSC_CpG_Island))
table_Relation_to_UCSC_CpG_Island$ALL_TOT <- rep(sum(table_Relation_to_UCSC_CpG_Island[,3]),nrow(table_Relation_to_UCSC_CpG_Island))

save(table_CHR, table_Relation_to_UCSC_CpG_Island, table_group, file=paste(database, "_tables.RData",  sep=''))

input = table_group
exactfisher.res=matrix(data=NA,nrow=nrow(input),ncol=4)
for (i in 1:nrow(input)) {
  table=matrix(nrow=2,ncol=2)
  table[1,1]= input[i,2]
  table[2,1]= input[i,3]-input[i,2]
  table[1,2]= input[i,4]-input[i,2]
  table[2,2]= input[i,5]-(table[1,1]+table[2,1]+table[1,2])
  f=fisher.test(table)
  exactfisher.res[i,1]=f[[1]][1]
  exactfisher.res[i,2]=f[[2]][1]
  exactfisher.res[i,3]=f[[2]][2]
  exactfisher.res[i,4]=f[[3]][[1]]
}
colnames(exactfisher.res) <- c("pvalue","Confidence interval Inf","Confidence interval Sup","OR")
input_exactfisher=cbind(input,exactfisher.res)
write.csv(input_exactfisher, "UCSC_RefGene_Group.csv", row.names = F)

input = table_CHR
exactfisher.res=matrix(data=NA,nrow=nrow(input),ncol=4)
for (i in 1:nrow(input)) {
  table=matrix(nrow=2,ncol=2)
  table[1,1]= input[i,2]
  table[2,1]= input[i,3]-input[i,2]
  table[1,2]= input[i,4]-input[i,2]
  table[2,2]= input[i,5]-(table[1,1]+table[2,1]+table[1,2])
  f=fisher.test(table)
  exactfisher.res[i,1]=f[[1]][1]
  exactfisher.res[i,2]=f[[2]][1]
  exactfisher.res[i,3]=f[[2]][2]
  exactfisher.res[i,4]=f[[3]][[1]]
}
colnames(exactfisher.res) <- c("pvalue","Confidence interval Inf","Confidence interval Sup","OR")
input_exactfisher=cbind(input,exactfisher.res)
write.csv(input_exactfisher, "CHR.csv", row.names = F)

input = table_Relation_to_UCSC_CpG_Island
exactfisher.res=matrix(data=NA,nrow=nrow(input),ncol=4)
for (i in 1:nrow(input)) {
  table=matrix(nrow=2,ncol=2)
  table[1,1]= input[i,2]
  table[2,1]= input[i,3]-input[i,2]
  table[1,2]= input[i,4]-input[i,2]
  table[2,2]= input[i,5]-(table[1,1]+table[2,1]+table[1,2])
  f=fisher.test(table)
  exactfisher.res[i,1]=f[[1]][1]
  exactfisher.res[i,2]=f[[2]][1]
  exactfisher.res[i,3]=f[[2]][2]
  exactfisher.res[i,4]=f[[3]][[1]]
}
colnames(exactfisher.res) <- c("pvalue","Confidence interval Inf","Confidence interval Sup","OR")
input_exactfisher=cbind(input,exactfisher.res)
write.csv(input_exactfisher, "Relation_to_UCSC_CpG_Island.csv", row.names = F)

