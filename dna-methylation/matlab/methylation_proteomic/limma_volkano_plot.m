fc_var = 'Age_logFC';
pValue_var = 'Age_P_Value_fdr_bh';
fc_lim = 0.0015;
pValue_lim = 0.001;

data.(pValue_var) = data.(pValue_var) + 1e-300; 

minX = min(data.(fc_var));
maxX = max(data.(fc_var));
shiftX = maxX - minX;
xLim = max(abs(minX - 0.1 * shiftX), abs(maxX + 0.1 * shiftX));
maxY = max(-log10(data.(pValue_var)));

data_fc_only = data(abs(data.(fc_var)) > fc_lim & data.(pValue_var) > pValue_lim, :);
data_pValue_only = data(abs(data.(fc_var)) < fc_lim & data.(pValue_var) < pValue_lim, :);
data_fc_pValue = data(abs(data.(fc_var)) > fc_lim & data.(pValue_var) < pValue_lim, :);
data_not = data(abs(data.(fc_var)) < fc_lim & data.(pValue_var) > pValue_lim, :);

opacity = 0.5;
marker_size = 50;

fig = figure;
color = 'black';
h = scatter(data_not.(fc_var), -log10(data_not.(pValue_var)), marker_size, 'o', 'LineWidth',  1, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', color, 'MarkerEdgeAlpha', opacity, 'MarkerFaceAlpha', opacity);
legend(h, sprintf('NS'), 'Interpreter', 'latex');
hold all;

set(gca, 'FontSize', 40);
xlabel('$\log_{2}($Fold Change$)$', 'Interpreter', 'latex');
set(gca, 'FontSize', 40);
ylabel('$-\log_{10}($p-value$)$', 'Interpreter', 'latex');

color = 'green';
h = scatter(data_fc_only.(fc_var), -log10(data_fc_only.(pValue_var)), marker_size, 'o', 'LineWidth',  1, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', color, 'MarkerEdgeAlpha', opacity, 'MarkerFaceAlpha', opacity);
legend(h, sprintf('$\\log_{2}($Fold Change$)$'), 'Interpreter', 'latex');
hold all;

color = 'blue';
h = scatter(data_pValue_only.(fc_var), -log10(data_pValue_only.(pValue_var)), marker_size, 'o', 'LineWidth',  1, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', color, 'MarkerEdgeAlpha', opacity, 'MarkerFaceAlpha', opacity);
legend(h, sprintf('p-value'), 'Interpreter', 'latex');
hold all;

color = 'red';
h = scatter(data_fc_pValue.(fc_var), -log10(data_fc_pValue.(pValue_var)), marker_size, 'o', 'LineWidth',  1, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', color, 'MarkerEdgeAlpha', opacity, 'MarkerFaceAlpha', opacity);
legend(h, sprintf('$\\log_{2}($Fold Change$)$ and p-value'), 'Interpreter', 'latex');
hold all;

h = plot([-fc_lim -fc_lim], [1e-10 maxY*1.5], ':', 'Color', 'k', 'LineWidth',  3);
h.Annotation.LegendInformation.IconDisplayStyle = 'off';
hold all;

h = plot([fc_lim fc_lim], [1e-10 maxY*1.5], ':', 'Color', 'k', 'LineWidth',  3);
h.Annotation.LegendInformation.IconDisplayStyle = 'off';
hold all;

h = plot([-xLim xLim], [-log10(pValue_lim) -log10(pValue_lim)], ':', 'Color', 'k', 'LineWidth',  3);
h.Annotation.LegendInformation.IconDisplayStyle = 'off';
hold all;

propertyeditor on;
grid on;
box on;
legend(gca,'off');
legend('Location', 'SouthWest', 'NumColumns', 1, 'Interpreter', 'latex');
legend('FontSize', 16);
xlim([-xLim, xLim])
ylim([0.01 maxY*1.3])
set(gca, 'YScale', 'log')
title(dataset, 'FontSize', 40, 'FontWeight', 'normal', 'Interpreter', 'latex');
fn_fig = sprintf('%s/%s_%s(%0.2e)_%s(%0.2e)', dataset_path, data_type, fc_var, fc_lim, pValue_var, pValue_lim);
oqs_save_fig(fig, fn_fig);

fn_tbl = sprintf('%s/%s_%s(%0.2e)_%s(%0.2e).xlsx', dataset_path, data_type, fc_var, fc_lim, pValue_var, pValue_lim);
writetable(data_fc_pValue, fn_tbl, 'Sheet', 1);

genes_raw = data_fc_pValue.('UCSC_REFGENE_NAME');
genes = {};
num_cells = size(genes_raw, 1);
for gene_row_id = 1:num_cells
    genes_row = genes_raw{gene_row_id};
    cells_genes = strsplit(genes_row, ';');
    for gene = cells_genes
        if ~strcmp(gene, '')
            genes = vertcat(genes, gene);
        end
    end
end
unique_genes = unique(genes);
fn_tbl = sprintf('%s/genes_%s_%s(%0.2e)_%s(%0.2e).csv', dataset_path, data_type, fc_var, fc_lim, pValue_var, pValue_lim);
writecell(unique_genes, fn_tbl);
