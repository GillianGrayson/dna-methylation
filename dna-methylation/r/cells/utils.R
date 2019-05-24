###
library(impute)
library(pracma)
library(parallel)
library(data.table)
library(rlist)
library(plyr)
library(lme4)
library(omics)
library(quadprog)

impute <- function(betas){
library(impute)
library(data.table)
M <- log2(betas/(1-betas))
M_imp <- impute.knn(M,k = 10)$data
betas_imp <- 2^M_imp / (1 + 2^M_imp)
rownames(betas_imp) <- rownames(betas)
colnames(betas_imp) <- colnames(betas)
return(as.data.table(betas_imp))}

peaks <- function(x){
   library(pracma)
   h <- density(x)
   xx <- h$y
   st <- mean(diff(h$x))
   mpd <- round(.15/st)
   p <- findpeaks(xx,minpeakheight=1,minpeakdistance=mpd,nups=3,ndown=3)
   if(is.matrix(p)){
   l <- list()
   for(i in 1:nrow(p)){
   l[[i]] <- c(h$x[p[i,2:4]])}} else{l <- list();l[[1]] <- c(h$x[p[2:4]])} 
   return(l)}

identify_SEMs <- function(x,k=3){
quant <- quantile(x,na.rm=T,c(0.25,0.75))
q1 <- quant[1] ; q3 <- quant[2]
iqr <- q3 - q1
L2 <- q1 - k*iqr ; U2 <- q3 + k*iqr
y <- rep(0,length(x))
y[which(x < L2)] <- -1 
y[which(x > U2)] <- 1 
return(y)}

identify_SEMs_ref <- function(x,k=3,idx){
quant <- quantile(x[idx],na.rm=T,c(0.25,0.75))
q1 <- quant[1] ; q3 <- quant[2]
iqr <- q3 - q1
L2 <- q1 - k*iqr ; U2 <- q3 + k*iqr
y <- rep(0,length(x))
y[which(x < L2)] <- -1 
y[which(x > U2)] <- 1 
return(y)}


summary_sd <- function(x){
y <- c(round(length(x),digits=0),round(sd(x,na.rm=T),digits=2),round(summary(x),digits=2))
names(y)[1:2] <- c("N","sd")
return(y)}

re.match <- function(pattern, x, ...) {
    do.call(rbind, regmatches(x, regexec(pattern, x, ...)))
}

resWBC <- function(x,data){
data$x <- x
fit <- glm(x~Monocytes+Gran+NK+CD8T+CD4T+B,data=data)
r <- resid(fit);return(r)}

resTechnical <- function(x,data){
data$x <- x
fit <- glm(x~chip+chip.pos,data=data)
r <- resid(fit);return(r)}

Sum_abs <- function(x){
return(sum(abs(x)))}

Sum_hyper <- function(x){
return(sum(x==1))}

Sum_hypo <- function(x){
return(sum(x== -1))}

trafo <- function(x,adult.age=20) { x=(x+1)/(1+adult.age); y=ifelse(x<=1, log( x),x-1);y }
anti.trafo <- function(x,adult.age=20) { ifelse(x<0, (1+adult.age)*exp(x)-1, (1+adult.age)*x+adult.age) }


