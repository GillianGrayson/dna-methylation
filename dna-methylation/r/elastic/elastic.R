rm(list=ls())

install.packages("Metrics")


library(readxl)
library(glmnet)
library(xlsx)
library(emdbook)
library(Metrics)
library(openxlsx)

rsq <- function(x, y) summary(lm(x~y))$r.squared 

path <- "E:/YandexDisk/Work/pydnameth/unn_epic/all_data"
fn = paste(path, "/table_part(wo_noIntensity_detP_H17+_negDNAmPhenoAge).xlsx",  sep='')
fn_save = paste(path, "/R_table_part(wo_noIntensity_detP_H17+_negDNAmPhenoAge).xlsx",  sep='')


target_feature = "DNAmAge"
target_part = "Control"
features = scan(paste(path, "/features_list.txt",  sep=''), character(), quote = "")

data = read_excel(fn)
X_All = data[, (names(data) %in% features)]
y_All = data[, target_feature]

X_Control = data[data$Group == "Control", (names(data) %in% features)]
y_Control = data[data$Group == "Control", target_feature]

X_Disease = data[data$Group == "Disease", (names(data) %in% features)]
y_Disease = data[data$Group == "Disease", target_feature]

X_target = as.matrix(X_All)
y_target = y_All[[target_feature]]

model = cv.glmnet(X_target, y_target, nfolds=10, nlambda=100, alpha=0.5, family="gaussian")
lambda_opt = model$lambda.min

y_All_pred = predict(model, as.matrix(X_All), type="response", s=lambda_opt)
RMSE_All = rmse(y_All[[target_feature]], y_All_pred)
R2_All = rsq(y_All[[target_feature]], y_All_pred)

y_Control_pred = predict(model, as.matrix(X_Control), type="response", s=lambda_opt)
RMSE_Control = rmse(y_Control[[target_feature]], y_Control_pred)
R2_Control = rsq(y_Control[[target_feature]], y_Control_pred)

y_Disease_pred = predict(model, as.matrix(X_Disease), type="response", s=lambda_opt)
RMSE_Disease = rmse(y_Disease[[target_feature]], y_Disease_pred)
R2_Disease = rsq(y_Disease[[target_feature]], y_Disease_pred)

data[paste("Immuno", target_feature, target_part, sep='')] = y_pred

write.xlsx(data, fn_save, sheetName = "Sheet1", col.names = TRUE, row.names = FALSE, append = FALSE)

coeffs_tmp <- coef(model, s = "lambda.min")
coeffs <- data.frame(name = coeffs_tmp@Dimnames[[1]][coeffs_tmp@i + 1], coefficient = coeffs_tmp@x)
fn <- paste(path, "/R_clock.xlsx",  sep='')
write.xlsx(coeffs, fn, sheetName = "Sheet1",col.names = TRUE, row.names = FALSE, append = FALSE)
