clear all;

part = 'v2';

epsilon = 1.5;
minpts = 3;
pca_features = {'PC_0', 'PC_1'}';

group_feature = 'Group';
groups = {'Control', 'Disease'}';
colors = {[0 1 0], [1 0 1]}';

scatterSize = 15;
opacity = 0.65;
globalFontSize = 34;
legendFontSize = 24;
legend_location = 'NorthEast';

path = 'E:/YandexDisk/Work/pydnameth/unn_epic';
figures_path = sprintf('E:/YandexDisk/Work/pydnameth/unn_epic/figures/features/dimReduction/part(%s)', part);
if ~exist(figures_path, 'dir')
    mkdir(figures_path)
end

fn = sprintf('%s/all_data/pca.xlsx', path);
opts = detectImportOptions(fn);
tbl_pca = readtable(fn, opts);

pos = [0.2, 0.2, 0.3, 0.4];

fig = figure;
propertyeditor('on');
tick_labels = tbl_pca.('features');
barh(tbl_pca.('PC0'), 'FaceColor', 'red');
yticks(linspace(1, size(tick_labels, 1), size(tick_labels, 1)))
ylim([0.5, size(tick_labels, 1) + 0.5])
xlim([-0.2, 1.1])
hold all;
set(gca, 'yTickLabel', tick_labels);
ax = gca;
ax.YAxis.FontSize = legendFontSize;
set(gca, 'TickLabelInterpreter', 'latex')
xlabel('PCA $1^{st}$ vector components', 'Interpreter', 'latex');
ax.XAxis.FontSize = legendFontSize;
set(gca, 'Position', pos);
grid on;
fn_fig = sprintf('%s/pca_0', figures_path);
oqs_save_fig(gcf, fn_fig)

fig = figure;
propertyeditor('on');
tick_labels = tbl_pca.('features');
barh(tbl_pca.('PC1'), 'FaceColor', 'red');
yticks(linspace(1, size(tick_labels, 1), size(tick_labels, 1)))
ylim([0.5, size(tick_labels, 1) + 0.5])
xlim([-0.2, 1.1])
hold all;
set(gca, 'yTickLabel', tick_labels);
ax = gca;
ax.YAxis.FontSize = legendFontSize;
set(gca, 'TickLabelInterpreter', 'latex')
xlabel('PCA $2^{nd}$ vector components', 'Interpreter', 'latex');
ax.XAxis.FontSize = legendFontSize;
set(gca, 'Position', pos);
grid on;
fn_fig = sprintf('%s/pca_1', figures_path);
oqs_save_fig(gcf, fn_fig)


fn = sprintf('%s/all_data/current_table.xlsx', path);
opts = detectImportOptions(fn);
tbl = readtable(fn, opts);

incKeys = {};
incVals = {{}};
decKeys = {};
decVals = {{}};
if size(incKeys, 1) > 0
    incMap = containers.Map(incKeys,incVals);
else
    incMap = containers.Map();
end
if size(decKeys, 1) > 0
    decMap = containers.Map(decKeys,decVals);
else
    decMap = containers.Map();
end
indexesFilt = get_filtered_indexes(tbl, incMap, decMap); 
tbl = tbl(indexesFilt, :);

fig = figure;
propertyeditor('on');
for g_id = 1:size(groups, 1)
    data = {};
    for f_id = 1:size(pca_features, 1)
        tmp = tbl{strcmp(tbl.(group_feature), groups{g_id}), pca_features{f_id}};
        data{f_id} = tmp;
    end
    
    if size(pca_features, 1) == 2
        h = scatter(data{1}, data{2}, 100, 'o', 'LineWidth',  1, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', colors{g_id}, 'MarkerEdgeAlpha', opacity, 'MarkerFaceAlpha', opacity);
        legend(h, sprintf('%s', groups{g_id}))
        set(gca, 'FontSize', globalFontSize);
        xlabel('PC1', 'Interpreter', 'latex')
        ylabel('PC2', 'Interpreter', 'latex')
        hold all;
    end
end
legend(gca,'off');
legend('Location', legend_location, 'NumColumns', 1, 'Interpreter', 'latex');
legend('FontSize', legendFontSize);
ax = gca;
set(ax,'TickLabelInterpreter','Latex');
box on;

fn_fig = sprintf('%s/pca', figures_path);
oqs_save_fig(gcf, fn_fig)


