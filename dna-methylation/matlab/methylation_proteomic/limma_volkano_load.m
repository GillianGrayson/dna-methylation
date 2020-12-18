clear all;

chip = '450k';
dataset = 'GSE74193';
data_type = 'betas';

dataset_path = sprintf('E:/YandexDisk/Work/pydnameth/methylation_and_proteomic/limma/%s', dataset);
fn_data = sprintf('%s/%s_filtered.xlsx', dataset_path, data_type);
data = readtable(fn_data);


