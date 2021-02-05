rm(list=ls())

install.packages("Metrics")


library(readxl)
library(glmnet)
library(xlsx)
library(emdbook)
library(Metrics)

path <- "E:/YandexDisk/Work/pydnameth/unn_epic/all_data"
fn_ctrl <- paste(path, "/table/", "biochemMultiplex_part(ctrl_wo_noIntensity_detP_subset).xlsx",  sep='')
fn_ckd <- paste(path, "/table/", "biochemMultiplex_part(ckd_wo_noIntensity_detP_subset).xlsx",  sep='')

data_ctrl <- read_excel(fn_ctrl)
X_ctrl = data_ctrl[, !(names(data_ctrl) %in% c("DNAmPhenoAge", "CKDAge"))]
X_ctrl_mtx = data.matrix(X_ctrl)
y_ctrl = data_ctrl$DNAmPhenoAge

data_ckd <- read_excel(fn_ckd)
X_ckd = data_ckd[, !(names(data_ckd) %in% c("DNAmPhenoAge", "CKDAge"))]
X_ckd_mtx = data.matrix(X_ckd)
y_ckd = data_ckd$DNAmPhenoAge

dim(X_ctrl_mtx)
dim(X_ckd_mtx)

lambdas <- lseq(0.001, 100000, length= 91)
model_ctrl = cv.glmnet(X_ctrl_mtx, y_ctrl, nfolds=10, nlambda=100, alpha=0.5, family="gaussian")
lambda_opt = model_ctrl$lambda.min

y_ctrl_pred = predict(model_ctrl,X_ctrl_mtx,type="response",s=lambda_opt)
y_ckd_pred = predict(model_ctrl,X_ckd_mtx,type="response",s=lambda_opt)

y_ctrl_df = data.frame(y_ctrl, y_ctrl_pred)
rmse(y_ctrl, y_ctrl_pred)
colnames(y_ctrl_df) = c("y_gt", "y_pred")
str(y_ctrl_df)
fn <- paste(path, "/table/", "R_biochemMultiplex_part(ctrl_wo_noIntensity_detP_subset).xlsx",  sep='')
write.xlsx(y_ctrl_df, fn, sheetName = "Sheet1",col.names = TRUE, row.names = FALSE, append = FALSE)

y_ckd_df = data.frame(y_ckd, y_ckd_pred)
rmse(y_ckd, y_ckd_pred)
colnames(y_ckd_df) = c("y_gt", "y_pred")
str(y_ckd_df)
fn <- paste(path, "/table/", "R_biochemMultiplex_part(ckd_wo_noIntensity_detP_subset).xlsx",  sep='')
write.xlsx(y_ckd_df, fn, sheetName = "Sheet1",col.names = TRUE, row.names = FALSE, append = FALSE)

coeffs_tmp <- coef(model_ctrl, s = "lambda.min")
coeffs <- data.frame(name = coeffs_tmp@Dimnames[[1]][coeffs_tmp@i + 1], coefficient = coeffs_tmp@x)

fn <- paste(path, "/clock/", "R_biochemMultiplex_part(ctrl_wo_noIntensity_detP_subset).xlsx",  sep='')
write.xlsx(coeffs, fn, sheetName = "Sheet1",col.names = TRUE, row.names = FALSE, append = FALSE)
