setwd("D:/Aaron/Bio/turin/test")
library(data.table)
dnam_raw <- fread("GSE40279.txt", header = TRUE, sep = "\t")
setDF(dnam_raw)
dnam <- dnam_raw[-1]
row.names(dnam) <- dnam_raw$ID_REF

dnam_keys <- fread("GSE40279_sample_key.txt", header = FALSE, sep = "\t")
setDF(dnam_keys)
column_names = list()
i <- 1
while(i < nrow(dnam_keys)+1) {
  column_names[[i]] <- dnam_keys[i, 3]
  i <- i + 1
}
colnames(dnam) = column_names

source("utils.R")
load("compute_SEMs.RData")
#load("data.RData")
#dnam <- betaFunnorm_detPfiltered

###############################################################################################
##### 6. compute WBC ##########################################################################

print("Houseman WBC estimation...")
dnam<-t(dnam)
i <- intersect(colnames(dnam),rownames(model[["coefficients"]]))
dnam <- dnam[,i]
model[["coefficients"]] <- model[["coefficients"]][i,]
model[["df.residual"]] <- model[["df.residual"]][i]
model[["pvals"]] <- model[["pvals"]][i]
idx <- order(model$pvals)[1:500]
coefs <- coef(model)[idx,]

dnam <- dnam[,which(colnames(dnam) %in% rownames(coefs))]
coefs <- coefs[colnames(dnam),]
tmp <- re.match("^(.+)_(.+)$", rownames(dnam))
samples <- data.frame(row.names=rownames(dnam),chip=tmp[,2],chip.pos=tmp[,3])
samples_tmp <- data.frame(row.names=rownames(dnam),chip=tmp[,2],chip.pos=tmp[,3])
samples_tmp$chip <- as.numeric(samples_tmp$chip)
samples_tmp$chip.pos <- as.numeric(samples_tmp$chip.pos)

for (i in 1:ncol(dnam)) {
    y <- as.numeric(dnam[,i])
    model <- lmer(y ~ (1 | chip) + (1 | chip.pos),
                  data=samples_tmp, REML=FALSE, na.action=na.exclude)
    dnam[,i] <- fixef(model)["(Intercept)"] + resid(model, type="response")}

types <- c("Monocytes","B","CD4T","NK","CD8T","Eosinophils","Neutrophils")
# Build projection matrix
L <- matrix(0, length(types), ncol(coefs),
            dimnames=list(types, colnames(coefs)))
L[,"(Intercept)"] <- 1
for (r in rownames(L)) {
    L[r,which(colnames(L) == r)] <- 1
}
L[c("Eosinophils", "Neutrophils"),"Granulocytes"] <- 1
L[c("Monocytes", "B", "CD4T", "NK", "CD8T"),"PBMC"] <- 1
# Project coefficients
coefs <- tcrossprod(coefs, L)
# Predict WBC differentials
wbc.predictions <- matrix(NA, nrow(dnam), ncol(coefs),
                          dimnames=list(rownames(dnam), colnames(coefs)))
A <- diag(ncol(coefs))
b <- rep(0, ncol(coefs))
for (i in 1:nrow(wbc.predictions)) {
    idx <- which(!is.na(dnam[i,]))
    D <- crossprod(coefs[idx,])
    d <- crossprod(coefs[idx,], as.numeric(dnam[i,idx]))
    tmp <- try(solve.QP(D, d, A, b)$solution, silent=TRUE)
    if (!inherits(tmp, "try-error")) {
        wbc.predictions[i,] <- tmp
    }}

wbc.predictions <- as.data.frame(wbc.predictions)
wbc.predictions$Gran <- wbc.predictions$Eosinophils + wbc.predictions$Neutrophils
wbc.predictions <- wbc.predictions[,c(1:5,8)]

colnames_raw<-colnames(dnam_raw)
colnames_raw<-colnames_raw[-1]
row.names(wbc.predictions)<-colnames_raw

fwrite(wbc.predictions,"GSE40279_cells.txt",sep="\t",row.names=FALSE, col.names = TRUE)
