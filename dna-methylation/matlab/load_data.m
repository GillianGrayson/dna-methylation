clear all;

chip = '450k';
dataset = 'GSE87571';

dataset_path = sprintf('E:/YandexDisk/Work/pydnameth/%s', dataset);

data_type = 'betas';
norm = '';
part = '';

if strcmp(dataset, 'unn_epic')
    fn_obs = sprintf('%s/observables_part(%s).csv', dataset_path, part);
    fn_betas = sprintf('%s/betas_norm(%s)_part(%s).txt', dataset_path, norm, part);
    fn_ann = sprintf('%s/annotations.txt', dataset_path);
else
    fn_obs = sprintf('%s/observables.txt', dataset_path);
    fn_betas = sprintf('%s/betas.txt', dataset_path);
    fn_ann = sprintf('%s/annotations.txt', dataset_path);
end

obs = readtable(fn_obs, 'ReadRowNames', true);
betas = readtable(fn_betas, 'ReadRowNames', true);
ann = readtable(fn_ann, 'ReadRowNames', true);
