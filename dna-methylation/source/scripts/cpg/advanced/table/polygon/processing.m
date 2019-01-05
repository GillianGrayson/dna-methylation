clear all;

% ======== params ========
config_base.metrics_rank = 1;
config_base.plot_method = 1;
config_base.metrics_diff_id = 2;
config_base.metrics_diff_direction = 'ascend';
config_base.part = 0.0005;

% ======== config ========
config_base.data_base = 'GSE87571';
config_base.data_type = 'cpg';

config_base.experiment = 'base';
config_base.task = 'table';
config_base.method = 'linreg';

config_base.exclude = 'none';
config_base.cross_reactive = 'ex';
config_base.snp = 'ex';
config_base.chr = 'NG';
config_base.gene_region = 'yes';
config_base.geo = 'any';
config_base.probe_class = 'any';

config_base.cells = 'none';

config_base.obs = containers.Map();
config_base.obs('gender') = ['vs'];

obs_keys = config_base.obs.keys;
for obs_id = 1:size(obs_keys, 2)
    config_base.(genvarname(obs_keys{1, obs_id})) = config_base.obs(obs_keys{1, obs_id});
end

config_base.params = containers.Map();
config_base.params('out_limit') = ['0.0'];
config_base.params('out_sigma') = ['0.0'];

params_keys = sort(config_base.params.keys);
config_base.name = strcat(params_keys{1, 1}, '(', config_base.params(params_keys{1, 1}), ')');
if size(params_keys, 2) > 1
    for params_id = 2:size(params_keys, 2)
        config_base.name = strcat(config_base.name, '_', params_keys{1, params_id}, '(', config_base.params(params_keys{1, params_id}), ')');
    end
end

config_base.is_clustering = 0;

config_base.up = get_up_data_path(); 

% ======== save_config ========
config_advanced.data_base = config_base.data_base;
config_advanced.data_type = config_base.data_type;

config_advanced.experiment = 'advanced';
config_advanced.task = 'table';
config_advanced.method = 'polygon';

config_advanced.exclude = config_base.exclude;
config_advanced.cross_reactive = config_base.cross_reactive;
config_advanced.snp = config_base.snp;
config_advanced.chr = config_base.chr;
config_advanced.gene_region = config_base.gene_region;
config_advanced.geo = config_base.geo;
config_advanced.probe_class = config_base.probe_class;

config_advanced.cells = config_base.cells;
config_advanced.obs = config_base.obs;

for obs_id = 1:size(obs_keys, 2)
    config_advanced.(genvarname(obs_keys{1, obs_id})) = config_advanced.obs(obs_keys{1, obs_id});
end

config_advanced.params = containers.Map();
config_advanced.params('sigma') = ['3'];

params_keys = sort(config_advanced.params.keys);
config_advanced.name = strcat(params_keys{1, 1}, '(', config_advanced.params(params_keys{1, 1}), ')');
if size(params_keys, 2) > 1
    for params_id = 2:size(params_keys, 2)
        config_advanced.name = strcat(config_advanced.name, '_', params_keys{1, params_id}, '(', config_advanced.params(params_keys{1, params_id}), ')');
    end
end

config_advanced.is_clustering = config_base.is_clustering;

config_advanced.up = get_up_data_path(); 

% ======== processing ========
specific(config_base, config_advanced);