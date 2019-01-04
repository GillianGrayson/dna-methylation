clear all;

metric = "r_test";

data_base = 'GSE87571';
data_type = 'cpg';

exclude = 'none';
cross_reactive = 'ex';
snp = 'ex';
chr = 'NG';
gene_region = 'yes';
geo = 'any';
probe_class = 'any';

cells = 'none';
obs = containers.Map();
obs('gender') = ['vs'];

obs_keys = obs.keys;

base_experiment = 'base';
base_task = 'table';
base_method = 'linreg_mult';

base_params = containers.Map();
base_params('exog_num') = ["100"];
base_params('exog_num_comb') = ["100"];
base_params('exog_type') = ["all"];

if isempty(base_params)
    base_name = 'default';
else
    params_keys = sort(base_params.keys);
    base_name = strcat(params_keys{1, 1}, '(', base_params(params_keys{1, 1}), ')');
    if size(params_keys, 2) > 1
        for params_id = 2:size(params_keys, 2)
            base_name = strcat(base_name, '_', params_keys{1, params_id}, '(', base_params(params_keys{1, params_id}), ')');
        end
    end
end

advanced_experiment = 'advanced';
advanced_task = 'clock';
advanced_method = 'linreg';

advanced_params = containers.Map();
advanced_params('exog_num') = ["100"];
advanced_params('exog_num_comb') = ["100"];
advanced_params('exog_type') = ["all"];

if isempty(advanced_params)
    advanced_name = 'default';
else
    params_keys = sort(advanced_params.keys);
    advanced_name = strcat(params_keys{1, 1}, '(', advanced_params(params_keys{1, 1}), ')');
    if size(params_keys, 2) > 1
        for params_id = 2:size(params_keys, 2)
            advanced_name = strcat(advanced_name, '_', params_keys{1, params_id}, '(', advanced_params(params_keys{1, params_id}), ')');
        end
    end
end

% ======== config_base ========
config_base.data_base = data_base;
config_base.data_type = data_type;

config_base.experiment = base_experiment;
config_base.task = base_task;
config_base.method = base_method;

config_base.exclude = exclude;
config_base.cross_reactive = cross_reactive;
config_base.snp = snp;
config_base.chr = chr;
config_base.gene_region = gene_region;
config_base.geo = geo;
config_base.probe_class = probe_class;

config_base.obs = obs;

config_base.cells = cells;
for obs_id = 1:size(obs_keys, 2)
    config_base.(genvarname(obs_keys{1, obs_id})) = obs(obs_keys{1, obs_id});
end

config_base.is_clustering = 0;

config_base.up = get_up_data_path();

config_base.name = base_name;

% ======== config_advanced ========
config_advanced.data_base = data_base;
config_advanced.data_type = data_type;

config_advanced.experiment = advanced_experiment;
config_advanced.task = advanced_task;
config_advanced.method = advanced_method;

config_advanced.exclude = exclude;
config_advanced.cross_reactive = cross_reactive;
config_advanced.snp = snp;
config_advanced.chr = chr;
config_advanced.gene_region = gene_region;
config_advanced.geo = geo;
config_advanced.probe_class = probe_class;

config_advanced.obs = obs;

config_advanced.cells = cells;
for obs_id = 1:size(obs_keys, 2)
    config_advanced.(genvarname(obs_keys{1, obs_id})) = obs(obs_keys{1, obs_id});
end

config_advanced.is_clustering = 0;

config_advanced.up = get_up_data_path();

config_advanced.name = advanced_name;

% ======== processing ========
f = figure;
if strcmp(config_advanced.gender, 'vs')
    config_advanced.gender = 'F';
    config_advanced.color = 'r';
    plot_clock_metrics(config_base, config_advanced, metric)
    config_advanced.gender = 'M';
    config_advanced.color = 'b';
    plot_clock_metrics(config_base, config_advanced, metric)
    config_advanced.gender = 'vs';
else
    config_advanced.color = 'g';
    plot_clock_metrics(config_base, config_advanced, metric)
end

suffix = sprintf('metric(%s)', metric);

up_save = get_up_figure_path();

save_path = sprintf('%s/%s', ...
    up_save, ...
    get_result_path(config_advanced));
mkdir(save_path);

box on;
b = gca;
legend(b,'off');
xlim([1 100])
title(sprintf('clock_method(%s)', config_base.method), 'FontSize', 16, 'Interpreter', 'none')

savefig(f, sprintf('%s/method(%s)_metric(%s).fig', save_path, config_base.method, metric))
saveas(f, sprintf('%s/method(%s)_metric(%s).png', save_path, config_base.method, metric))