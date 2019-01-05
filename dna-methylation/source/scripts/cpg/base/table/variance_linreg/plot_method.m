clear all;

cpgs = string(importdata('cpgs.txt'));
config.is_plot_regions = 1;

% ======== config ========
config.data_base = 'GSE87571';
config.data_type = 'cpg';

config.experiment = 'base';
config.task = 'table';
config.method = 'variance_linreg';

config.exclude = 'none';
config.cross_reactive = 'ex';
config.snp = 'ex';
config.chr = 'NG';
config.gene_region = 'yes';
config.geo = 'any';
config.probe_class = 'any';

config.cells = 'none';
config.obs = containers.Map();
config.obs('gender') = ['vs'];

obs_keys = config.obs.keys;
for obs_id = 1:size(obs_keys, 2)
    config.(genvarname(obs_keys{1, obs_id})) = config.obs(obs_keys{1, obs_id});
end

config.params = containers.Map();

if isempty(config.params)
    config.name = 'default';
else
    params_keys = sort(config.params.keys);
    config.name = strcat(params_keys{1, 1}, '(', config.params(params_keys{1, 1}), ')');
    if size(params_keys, 2) > 1
        for params_id = 2:size(params_keys, 2)
            config.name = strcat(config.name, '_', params_keys{1, params_id}, '(', config.params(params_keys{1, params_id}), ')');
        end
    end
end

config.is_clustering = 0;

config.color = '';

config.up = get_up_data_path(); 

[annotations_map, labels] = get_annotations(config);

for cpg_id = 1:size(cpgs, 1)
    
    cpg = cpgs(cpg_id)
    
    curr_ann = annotations_map(cpg);
    genes_str = curr_ann(find(labels=="UCSC_REFGENE_NAME"));
    genes = strsplit(genes_str,';');
    genes = unique(genes);
    genes = strjoin(genes, ';');
    
    up_save = get_up_figure_path();
    
    save_path = sprintf('%s/%s', ...
        up_save, ...
        get_result_path(config));
    mkdir(save_path);
    
    suffix = sprintf('cpg(%s)', cpg);
    
    % ======== processing ========
    f = figure;
    if strcmp(config.gender, 'vs')
        config.is_plot_regions = 1;
        config.gender = 'F';
        config.color = 'r';
        plot_variance_linreg_cpg(config, cpg)
        config.gender = 'M';
        config.color = 'b';
        plot_variance_linreg_cpg(config, cpg)
        config.gender = 'vs';
    else
        plot_variance_linreg_cpg(config, cpg)
    end
   
    box on;
    b = gca;
    legend(b,'off');
    yl = ylim;
    if yl(1) < 0
       ylim([0, yl(2)]); 
    end
    if yl(2) > 1
       ylim([yl(1), 1]);
    end
    title(sprintf('%s(%s)', cpg, genes), 'FontSize', 16)
    
    savefig(f, sprintf('%s/%d_%s.fig', save_path, cpg_id, suffix))
    saveas(f, sprintf('%s/%d_%s.png', save_path, cpg_id, suffix))
    
    f = figure;
    if strcmp(config.gender, 'vs')
        config.is_plot_regions = 0;
        config.gender = 'F';
        config.color = 'r';
        plot_variance_linreg_delta(config, cpg)
        config.gender = 'M';
        config.color = 'b';
        plot_variance_linreg_delta(config, cpg)
        config.gender = 'vs';
    else
        plot_variance_linreg_delta(config, cpg)
    end
    
    box on;
    b = gca;
    legend(b,'off');
    yl = ylim;
    if yl(1) < 0
       ylim([0, yl(2)]); 
    end
    if yl(2) > 1
       ylim([yl(1), 1]);
    end
    title(sprintf('%s(%s)', cpg, genes), 'FontSize', 16)
    
    savefig(f, sprintf('%s/%d_delta_%s.fig', save_path, cpg_id, suffix))
    saveas(f, sprintf('%s/%d_delta_%s.png', save_path, cpg_id, suffix))
    
end
