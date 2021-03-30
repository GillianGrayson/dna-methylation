figures_path = sprintf('%s/covid/figures', dataset_path);
if ~exist(figures_path, 'dir')
    mkdir(figures_path)
end

colors = {[0 1 0], [1 0 1]}';
opacity = 0.65;

cpgs = importdata(sprintf('%s/covid/cpgs.txt', dataset_path));

res_table = readtable(sprintf('%s/covid/current_table.xlsx', dataset_path), 'ReadRowNames', true);

obs_before = obs((obs.('Sample_Chronology') == 1) & (~strcmp(obs.('ID'), 'I64_1')), :);
obs_before.('BetasColumn') = strcat('X', obs_before.Properties.RowNames);
sn_before = obs_before.('BetasColumn');
obs_after = obs((obs.('Sample_Chronology') == 2) & (~strcmp(obs.('ID'), 'I64_2')), :);
obs_after.('BetasColumn') = strcat('X', obs_after.Properties.RowNames);
sn_after = obs_after.('BetasColumn');

IDs_after = obs_after.('ID');
for i = 1:size(IDs_after, 1)
    tmp = erase(IDs_after{i}, ["+", " (1)"]);
    IDs_after{i} = tmp;
end
obs_after.('ID') = IDs_after;

for i = 1:size(obs_before.('ID'), 1)
    if strcmp(obs_before.('ID'){i}, obs_after.('ID'){i}) ~= 1
        error('Wrong ID order in after and before')
    end
end

betas_before = betas(:, sn_before);
betas_after = betas(:, sn_after);

obs_before_ctrl = obs_before(strcmp(obs_before.('COVID'), 'no'), :);
sn_before_ctrl = obs_before_ctrl.('BetasColumn');
obs_before_case = obs_before(strcmp(obs_before.('COVID'), 'before'), :);
sn_before_case = obs_before_case.('BetasColumn');

obs_after_ctrl = obs_after(strcmp(obs_after.('COVID'), 'no'), :);
sn_after_ctrl = obs_after_ctrl.('BetasColumn');
obs_after_case = obs_after(strcmp(obs_after.('COVID'), 'after'), :);
sn_after_case = obs_after_case.('BetasColumn');

betas_before_ctrl = betas(:, sn_before_ctrl);
betas_before_case = betas(:, sn_before_case);

betas_after_ctrl = betas(:, sn_after_ctrl);
betas_after_case = betas(:, sn_after_case);

datamat = zeros(height(obs_before), 2);
raw_factors = obs_before.('COVID');
between_factors = grp2idx(raw_factors);

res_table_local = table('Size', [height(betas), 4], 'VariableTypes', {'string', 'string', 'double', 'double'});
res_table_local.Properties.VariableNames = {'cpg', 'gene', 'mixed_anova_pval', 'diff_kw_pval'};
res_table_local.('cpg') = betas.Properties.RowNames;
res_table_local.Properties.RowNames = betas.Properties.RowNames;

for cpg_id = 1:size(cpgs, 1)
    fprintf(sprintf('cpg_id: %d\n', cpg_id));
    
    cpg = cpgs{cpg_id};
    
    gene_raw = ann{cpg, 'UCSC_RefGene_Name'};
    genes_list = unique(split(gene_raw, ';'));
    genes = string(strjoin(genes_list,';'));
    res_table_local{cpg, 'gene'} = genes;
    
    datamat(:, 1) = betas_before{cpg, :};
    datamat(:, 2) = betas_after{cpg, :};
    
    tbl = simple_mixed_anova(datamat, between_factors, {'Time'}, {'Group'});
    mixed_anova_pval = tbl{'Group:Time', 'pValue'};
    res_table_local{cpg, 'mixed_anova_pval'} = mixed_anova_pval;
    
    x_positions = linspace(0.5, 0.5 * 2, 2);
    fig = figure;
    propertyeditor('on');
    
    for time_id = 1:2
        
        plot_data = {};
        if time_id == 1
            plot_data{1} = betas_before_ctrl{cpg, :};
            plot_data{2} = betas_before_case{cpg, :};
        else
            plot_data{1} = betas_after_ctrl{cpg, :};
            plot_data{2} = betas_after_case{cpg, :};
        end
        
        for g_id = 1 : 2
            curr_data = plot_data{g_id}';
            color = colors{g_id};
            
            position = x_positions(time_id) + 0.09 * sign(g_id - 1.5);
            
            b = boxplot(curr_data, 'Notch', 'off', 'positions', [position], 'Colors', color);
            set(gca, 'FontSize', 40);
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
            h = scatter(xs, curr_data, 100, 'o', 'LineWidth',  1, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', color, 'MarkerEdgeAlpha', opacity, 'MarkerFaceAlpha', opacity);
            h.Annotation.LegendInformation.IconDisplayStyle = 'off';
            hold all;
        end
    end
    
    xticks(x_positions);
    xticklabels({'Before', 'After'});
    axis auto;
    xlim([min(x_positions) - 0.3, max(x_positions) + 0.3])
    box on;
    grid on;
    ylabel('$\beta$', 'Interpreter', 'latex');
    
    anova_pVal = res_table{cpg, 'mixed_anova_pval'};
    anova_pVal_fdr_bh = res_table{cpg, 'mixed_anova_pval_fdr_bh'};
    title(sprintf('%s (%s): mixed ANOVA p-value=%0.2e (FDR=%0.2e)', cpg, genes, anova_pVal, anova_pVal_fdr_bh), 'FontSize', 16, 'FontWeight', 'normal', 'Interpreter', 'latex');
    hold all;
    
    fn_fig = sprintf('%s/%d_%s(%s)_mANOVA', figures_path, cpg_id, cpg, genes);
    oqs_save_fig(gcf, fn_fig)
    close(fig);

    diff_beta = datamat(:, 2) - datamat(:, 1);
    diff_kw_pval = kruskalwallis(diff_beta, between_factors, 'off');
    res_table_local{cpg, 'diff_kw_pval'} = diff_kw_pval;
    
    kw_table = table('Size', [size(diff_beta, 1), 2], 'VariableTypes', {'double', 'double'});
    kw_table.Properties.VariableNames = {'diff', 'group'};
    kw_table.('diff') = diff_beta;
    kw_table.('group') = between_factors;
    
    diffs_by_group = {};
    groups = {1, 2}';
    groups_label = {'Control', 'Case'};
    for g_id = 1:size(groups, 1)
        diffs_by_group{g_id} = kw_table{kw_table.('group') == groups{g_id}, 'diff'};
    end
    
    fig = figure;
    propertyeditor('on');
    positions = 0.5 * linspace(1, size(groups, 1), size(groups, 1));
    for g_id = 1:size(groups, 1)
        b = boxplot(diffs_by_group{g_id},'Notch', 'off', 'positions', positions(g_id), 'Colors', colors{g_id});
        set(gca, 'FontSize', 40);
        all_items = handle(b);
        tags = get(all_items,'tag');
        idx = strcmpi(tags,'box');
        boxes = all_items(idx);
        set(all_items,'linewidth',3)
        idx = strcmpi(tags,'Outliers');
        outliers = all_items(idx);
        set(outliers, 'visible', 'off')
        hold all;
        xs = positions(g_id) * ones(size(diffs_by_group{g_id}, 1), 1) + ((rand(size(diffs_by_group{g_id}))-0.5)/10);
        h = scatter(xs, diffs_by_group{g_id}, 100, 'o', 'LineWidth',  1, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', colors{g_id}, 'MarkerEdgeAlpha', opacity, 'MarkerFaceAlpha', opacity);
        h.Annotation.LegendInformation.IconDisplayStyle = 'off';
        hold all;
    end
    xticks(positions);
    xticklabels(groups_label);
    axis auto;
    xlim([min(positions) - 0.3, max(positions) + 0.3])
    set(gca, 'TickLabelInterpreter', 'latex')
    box on;
    grid on;
    ylabel('$\beta_{\mathrm{after}} - \beta_{\mathrm{before}}$', 'Interpreter', 'latex')
    kw_pVal = res_table{cpg, 'diff_kw_pval'};
    kw_pVal_fdr_bh = res_table{cpg, 'diff_kw_pval_fdr_bh'};
    title(sprintf('%s (%s): KW p-value=%0.2e (FDR=%0.2e)', cpg, genes, kw_pVal, kw_pVal_fdr_bh), 'FontSize', 16, 'FontWeight', 'normal', 'Interpreter', 'latex');
    hold all;
    
    fn_fig = sprintf('%s/%d_%s(%s)_KW', figures_path, cpg_id, cpg, genes);
    oqs_save_fig(gcf, fn_fig)
    close(fig);
end

