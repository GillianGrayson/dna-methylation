clear all;

metric = "mae_test";

config.data_base = 'GSE87571';
config.data_type = 'cpg';

config.exclude = 'none';
config.cross_reactive = 'ex';
config.snp = 'ex';
config.chr = 'NG';
config.gene_region = 'yes';
config.geo = 'any';
config.probe_class = 'any';

obs = containers.Map();
obs('gender') = ['all'];
obs_keys = obs.keys;
config.obs = obs;
for obs_id = 1:size(obs_keys, 2)
    config.(genvarname(obs_keys{1, obs_id})) = config.obs(obs_keys{1, obs_id});
end
config.cells = 'any';

config.experiment = 'advanced';
config.task = 'clock';
config.method = 'linreg';

params = containers.Map();
params('type') = ["all"];
params('exogs') = ["100"];
params('combs') = ["100"];
params('runs') = ["100"];

if isempty(params)
    file_name = 'default';
else
    params_keys = sort(params.keys);
    file_name = strcat(params_keys{1, 1}, '(', params(params_keys{1, 1}), ')');
    if size(params_keys, 2) > 1
        for params_id = 2:size(params_keys, 2)
            file_name = strcat(file_name, '_', params_keys{1, params_id}, '(', params(params_keys{1, params_id}), ')');
        end
    end
end
config.file_name = file_name;

config.up = get_up_data_path();

% ======== processing ========
f = figure;
if strcmp(config.gender, 'vs')
    config.gender = 'F';
    config.color = 'r';
    plot_clock_metrics(config, metric)
    config.gender = 'M';
    config.color = 'b';
    plot_clock_metrics(config, metric)
    config.gender = 'vs';
elseif strcmp(config.gender, 'all')
    config.gender = 'F';
    config.color = 'r';
    plot_clock_metrics(config, metric)
    config.gender = 'M';
    config.color = 'b';
    plot_clock_metrics(config, metric)
    config.gender = 'any';
    config.color = 'k';
    plot_clock_metrics(config, metric)
    config.gender = 'all';
else
    config.color = 'g';
    plot_clock_metrics(config, metric)
end

suffix = sprintf('metric(%s)', metric);

save_path = sprintf('%s/%s', ...
    config.up, ...
    get_result_path(config));
mkdir(save_path);

box on;
b = gca;
legend(b,'off');
xlim([1 100])
title(sprintf('clock_method(%s)', config.method), 'FontSize', 16, 'Interpreter', 'none')

savefig(f, sprintf('%s/method(%s)_metric(%s).fig', save_path, config.method, metric))
saveas(f, sprintf('%s/method(%s)_metric(%s).png', save_path, config.method, metric))