clear all;

cpgs = string(importdata('cpgs.txt'));
data_bases = ["GSE40279"; "GSE87571"];
config.is_plot_regions = 1;

for cpg_id = 1:size(cpgs, 1)
    
    cpg = cpgs(cpg_id)
    
    f = figure;
    for data_base_id = 1:size(data_bases, 1)
        
        % ======== config ========
        
        config.data_base = data_bases(data_base_id);
        config.data_type = 'cpg';
        
        config.experiment = 'base';
        config.task = 'table';
        config.method = 'linreg';
        
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
        config.params('out_limit') = ["0.0"];
        config.params('out_sigma') = ["0.0"];
        
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
        
        % ======== processing ========
        subplot(1, size(data_bases, 1), data_base_id)
        
        if strcmp(config.gender, 'vs')
            config.is_plot_regions = 1;
            config.gender = 'F';
            config.color = 'r';
            plot_linreg_cpg(config, cpg)
            config.gender = 'M';
            config.color = 'b';
            plot_linreg_cpg(config, cpg)
            config.gender = 'vs';
        end
        
        box on;
        b = gca;
        legend(b,'off');
        title(config.data_base, 'FontSize', 16)
        yl = ylim;
        if yl(1) < 0
            ylim([0, yl(2)]);
        end
        if yl(2) > 1
            ylim([yl(1), 1]);
        end
        sgtitle(cpg, 'FontSize', 20)
        propertyeditor('on')
        
        suffix = sprintf('cpg(%s)_data_bases(%s)', cpg, join(sort(data_bases), '_'));
        
        config.data_base = "vs";
        
        up_save = get_up_figure_path();
        
        save_path = sprintf('%s/%s', ...
            up_save, ...
            get_result_path(config));
        mkdir(save_path);
        
        savefig(f, sprintf('%s/%s.fig', save_path, suffix))
        saveas(f, sprintf('%s/%s.png', save_path, suffix))
        
    end
    
end