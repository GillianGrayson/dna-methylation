clear all;

dataset_path = 'E:/YandexDisk/Work/pydnameth/unn_epic';

data_type = 'betas';
norm = 'fun';
part = 'wo_noIntensity_detP';

figures_path = sprintf('%s/figures/cpgs/dataType(%s)_norm(%s)_part(%s)', dataset_path, data_type, norm, part);
if ~exist(figures_path, 'dir')
    mkdir(figures_path)
end

fn = sprintf('%s/observables_part(%s).csv', dataset_path, part);
obs = readtable(fn);

fn = '';
if strcmp(data_type, 'betas')
    fn = sprintf('%s/betas_norm(%s)_part(%s).txt', dataset_path, norm, part);
    y_label = 'Methylation Level';
elseif strcmp(data_type, 'residuals')
    fn = sprintf('%s/residuals_cells(%s)_norm(%s)_part(%s).csv', dataset_path, cells_string, norm, part);
    y_label = 'Residuals';
end
data = readtable(fn, 'ReadRowNames', true);

fn = sprintf('%s/annotations.txt', dataset_path);
ann = readtable(fn, 'ReadRowNames', true);