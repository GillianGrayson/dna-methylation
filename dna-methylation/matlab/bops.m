clear all;

num_top_bops = 50;

groups = {'C', 'T'}';
colors = {[0 1 0],[1 0 0]}';
opacity = 0.65;

dataset_path = 'E:/YandexDisk/Work/pydnameth/unn_epic';
bop_path = 'E:/YandexDisk/Work/pydnameth/unn_epic/bop/table/manova/3c48cd40ad58b06cc3b1f27e3c72554c/ABC_mod.xlsx';
suffix_in_bop_file = '';

data_type = 'betas';
norm = 'fun';
part = 'wo_noIntensity_detP';

cell_types = {'''Bcell''', '''CD4T''', '''CD8T''', '''Neu''', '''NK'''}';
tmp = join(cell_types, ', ');
cells_string = sprintf('[%s]', tmp{:});

figures_path = sprintf('%s/figures/bops/dataType(%s)_norm(%s)_part(%s)', dataset_path, data_type, norm, part);
if ~exist(figures_path, 'dir')
    mkdir(figures_path)
end

fn = '';
if strcmp(data_type, 'betas')
    fn = sprintf('%s/betas_norm(%s)_part(%s).txt', dataset_path, norm, part);
    y_label = 'Methylation Level';
    show_pval = 1;
elseif strcmp(data_type, 'residuals')
    fn = sprintf('%s/residuals_cells(%s)_norm(%s)_part(%s).csv', dataset_path, cells_string, norm, part);
    y_label = 'Residuals';
    show_pval = 0;
end
data = readtable(fn, 'ReadRowNames', true);

tmp = zeros(size(data.Properties.RowNames, 1), 1);
cpgs_dict = containers.Map(data.Properties.RowNames, tmp);

bop_info = readtable(bop_path, 'ReadRowNames', true);
bop_names = bop_info.Properties.RowNames;
target_bops = bop_names(1:num_top_bops);

fn = sprintf('%s/observables_part(%s).csv', dataset_path, part);
opts = detectImportOptions(fn);
opts = setvartype(opts, {'Sample_Group'}, 'string');
obs = readtable(fn, opts);

group_indeces = {};
for g_id = 1 : size(groups, 1)
    group_indeces{g_id} = find(obs.('Sample_Group') == groups{g_id});
end

for bop_id = 1:size(target_bops, 1)
    bop = target_bops{bop_id};
    save_name = replace(bop, {':', '*'}, '_');
    cpgs_raw = bop_info{bop, 'aux'};
    p_val = bop_info{bop, end};
    cpgs_all = split(cpgs_raw, ';');
    cpgs = [];
    for cpg_id = 1:size(cpgs_all, 1)
        if isKey(cpgs_dict, cpgs_all(cpg_id))
            cpgs = vertcat(cpgs, cpgs_all(cpg_id));
        end
    end
    num_cpgs = size(cpgs, 1);
    
    x_font = 20;
    if num_cpgs > 15
        x_font = 8;
    elseif num_cpgs > 25
        x_font = 2;
    end
    
    xs = linspace(0.5, 0.5 * num_cpgs, num_cpgs);
    fig = figure;propertyeditor('on');
    for cpg_id = 1:num_cpgs
        cpg = cpgs{cpg_id};
        cpg_data = data{cpg, :};
        
        for g_id = 1 : size(groups, 1)
            curr_data = cpg_data(group_indeces{g_id})';
            color = colors{g_id};
            
            position = xs(cpg_id) + 0.09 * sign(g_id - 1.5);
            
            b = boxplot(curr_data,'Notch','on','positions', [position], 'Colors', color);
            all_items = handle(b);
            t = get(all_items,'tag');
            idx = strcmpi(t,'box');
            boxes = all_items(idx);
            set(all_items,'linewidth',1)
            idx = strcmpi(t,'Outliers');
            outliers = all_items(idx);
            set(outliers, 'visible', 'off')
            hold all;  
        end
        
    end
    xticks(xs);
    xticklabels(cpgs);
    xtickangle(90);
    axis auto;
    xlim([min(xs) - 0.3, max(xs) + 0.3])
    box on;
    grid on;
    
    ax = gca;
    ax.XAxis.FontSize = x_font;
    ylabel(y_label, 'Interpreter', 'latex');
    ax.YAxis.FontSize = 42;
    if show_pval == 1
        title(sprintf('%s (p-value: %0.4e)', replace(bop, {'_'}, '-'), p_val), 'FontSize', 20, 'FontWeight', 'normal');
    else
        title(sprintf('%s', replace(bop, {'_'}, '-')), 'FontSize', 20, 'FontWeight', 'normal');
    end
    
    fn_fig = sprintf('%s/%d_%s', figures_path, bop_id, save_name);
    oqs_save_fig(fig, fn_fig)
    saveas(gcf, sprintf('%s.png', fn_fig));
end
