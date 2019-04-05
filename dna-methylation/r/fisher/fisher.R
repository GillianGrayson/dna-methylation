GSE87571_all <- data.frame(table(m$UCSC_RefGene_Group))
GSE87571_curr <- data.frame(table(mm$UCSC_RefGene_Group))
colnames(GSE87571_all) <- c("UCSC_RefGene_Group", "TOTAL")
colnames(GSE87571_curr) <- c("UCSC_RefGene_Group", "CURR")
GSE87571_UCSC_RefGene_Group <- merge(GSE87571_all, GSE87571_curr, by="UCSC_RefGene_Group")


save(GSE87571_CHR, GSE87571_Relation_to_UCSC_CpG_Island, GSE87571_UCSC_RefGene_Group, file="GSE87571_tables.RData")

input = GSE87571_UCSC_RefGene_Group
input$CURR_TOT <- rep(sum(input[,2]),nrow(input))
input$ALL_TOT <- rep(sum(input[,3]),nrow(input))


input=read.table("CRC_paraffina_input_Fisher_E075_nominal0.001_POSNEG_ClassAGreater2.txt",sep="\t",header=T,quote="")

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
write.csv(input_exactfisher, "fisher_UCSC_RefGene_Group.csv", row.names = F)
