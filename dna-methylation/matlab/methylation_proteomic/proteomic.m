clear all;


datPath = sprintf('E:/YandexDisk/Work/pydnameth/methylation_and_proteomic/proteomic_data');

obs = readtable(fn_obs, 'ReadRowNames', true);
betas = readtable(fn_betas, 'ReadRowNames', true);
ann = readtable(fn_ann, 'ReadRowNames', true);


fn_data = sprintf('%s/%s_filtered.xlsx', datPath, data_type);
data = readtable(fn_data);


