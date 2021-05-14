clear all;

chip = '850k';
dataset = 'unn_epic';

dataset_path = sprintf('E:/YandexDisk/Work/pydnameth/%s', dataset);

data_type = 'betas';
norm = 'fun';
part = 'v1';
config = '0.01_0.10_0.10';

if strcmp(dataset, 'unn_epic')
    fn_obs = sprintf('%s/observables_part(%s).xlsx', dataset_path, part);
    fn_betas = sprintf('%s/betas_part(%s)_config(%s)_norm(%s).txt', dataset_path, part, config, norm);
    fn_ann = sprintf('%s/annotations.txt', dataset_path);
else
    fn_obs = sprintf('%s/observables.txt', dataset_path);
    fn_betas = sprintf('%s/betas.txt', dataset_path);
    fn_ann = sprintf('%s/annotations.txt', dataset_path);
end

obs = readtable(fn_obs, 'ReadRowNames', true);
betas = readtable(fn_betas, 'ReadRowNames', true);
ann = readtable(fn_ann, 'ReadRowNames', true);
