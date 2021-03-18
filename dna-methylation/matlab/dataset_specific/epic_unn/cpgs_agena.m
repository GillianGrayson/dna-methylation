figures_path = sprintf('%s/figures/cpgs/agena/dataType(%s)_part(%s)_config(%s)_norm(%s)', dataset_path, data_type, norm, config, part);
if ~exist(figures_path, 'dir')
    mkdir(figures_path)
end

cgs = ...
    { ...
    'cg07553761', ...
    'cg00481951', ...
    'cg23256579', ...
    'cg06639320', ...
    'cg22454769' ...
    }';
num_cpgs = size(cgs, 1);

group_by = 'Sex';
groups = {'F', 'M'}';
colors = {[1 0 0],[0 0 1]}';
opacity = 0.65;

x_font = 20;

agena_tbl = readtable('E:/YandexDisk/Work/pydnameth/unn_epic/agena/11.02.xlsx', 'ReadRowNames', true);
target_subjects = agena_tbl.Properties.VariableNames';
ts_id = 6;

group_indeces = {};
for g_id = 1 : size(groups, 1)
    group_indeces{g_id} = find(cell2mat(obs.(group_by)) == groups{g_id});
end

x_positions = linspace(0.5, 0.5 * num_cpgs, num_cpgs);
fig = figure;
propertyeditor('on');

for cg_id = 1:size(cgs, 1)
    
    cg = cgs{cg_id};
    cg_data = betas{cg, :}';
    
    for g_id = 1 : size(groups, 1)
        curr_data = cg_data(group_indeces{g_id})';
        color = colors{g_id};
        
        position = x_positions(cg_id) + 0.09 * sign(g_id - 1.5);
        
        b = boxplot(curr_data, 'Notch', 'off', 'positions', [position], 'Colors', color);
        all_items = handle(b);
        tags = get(all_items,'tag');
        idx = strcmpi(tags, 'box');
        boxes = all_items(idx);
        set(all_items, 'linewidth', 2)
        idx = strcmpi(tags, 'Outliers');
        outliers = all_items(idx);
        set(outliers, 'visible', 'off')
        hold all;
        
        xs = position * ones(size(curr_data, 1), 1) + ((rand(size(curr_data))-0.5)/10);
        h = scatter(xs, curr_data, 50, 'o', 'LineWidth',  1, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', color, 'MarkerEdgeAlpha', 0.3, 'MarkerFaceAlpha', 0.3);
        h.Annotation.LegendInformation.IconDisplayStyle = 'off';
        hold all;
    end
    
    curr_indexes = strcmp(obs.('ID'), target_subjects(ts_id));
    curr_obs = obs(curr_indexes, :);
    curr_data = betas{cg, curr_indexes}';
    agena_data = agena_tbl{cg, ts_id} * 0.01;
    if strcmp(curr_obs.(group_by){1}, groups{1})
        curr_color = colors{1};
    else
        curr_color = colors{2};
    end
    
    h = scatter([x_positions(cg_id)], [curr_data], 250, 'o', 'LineWidth',  1, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', curr_color, 'MarkerEdgeAlpha', 0.8, 'MarkerFaceAlpha', 0.8);
    h.Annotation.LegendInformation.IconDisplayStyle = 'off';
    hold all;
    h = scatter([x_positions(cg_id)], [agena_data], 250, 'pentagramm', 'LineWidth',  1, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', curr_color, 'MarkerEdgeAlpha', 0.8, 'MarkerFaceAlpha', 0.8);
    h.Annotation.LegendInformation.IconDisplayStyle = 'off';
    hold all;
    
end

xticks(x_positions);
xticklabels(cgs);
xtickangle(90);
axis auto;
xlim([min(x_positions) - 0.3, max(x_positions) + 0.3])
box on;
grid on;

ax = gca;
ax.XAxis.FontSize = x_font;
ylabel('Methylation level', 'Interpreter', 'latex');
ax.YAxis.FontSize = 30;

title(target_subjects(ts_id), 'FontSize', 20, 'FontWeight', 'normal', 'Interpreter', 'latex');

fn_fig = sprintf('%s/%s', figures_path, target_subjects{ts_id});
oqs_save_fig(fig, fn_fig)

if strcmp(chip, '850k')
    gene_raw = string(ann{cg, 'UCSC_RefGene_Name'});
else
    gene_raw = string(ann{cg, 'UCSC_REFGENE_NAME'});
end
genes_list = unique(split(gene_raw, ';'));
genes = strjoin(genes_list,';');