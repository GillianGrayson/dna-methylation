clear all;

part = 'v2';
pdist_metric = 'cosine';
rect_height = 0.1;
y_max = 1.5;

features = {'DNAmAgeHannumAA_scaled', 'DNAmAgeAA_scaled', 'DNAmPhenoAgeAA_scaled', 'DNAmGrimAgeAA_scaled', 'PhenoAgeAA_scaled', 'ImmunoAgeAA_scaled'}';
featuresLabels = {'DNAmAgeHannumAcc', 'DNAmAgeAcc', 'DNAmPhenoAgeAcc', 'DNAmGrimAge', 'PhenotypicalAgeAcc', 'ImmunoAgeAcc'}';
pca_features = {'AA_pc_0_scaled', 'AA_pc_1_scaled'}';

group_feature = 'Group';
groups = {'Control', 'Disease'}';
colors = {[0 1 0], [1 0 1]}';

scatterSize = 15;
opacity = 0.65;
globalFontSize = 36;
legendFontSize = 18;
legend_location = 'NorthEast';

path = 'E:/YandexDisk/Work/pydnameth/unn_epic';
figures_path = sprintf('E:/YandexDisk/Work/pydnameth/unn_epic/figures/features/clustering/part(%s)', part);
if ~exist(figures_path, 'dir')
    mkdir(figures_path)
end
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

data = tbl{:, features};

dist = pdist(data, pdist_metric);
clustTree = linkage(dist, 'average');
cophenetCorr = cophenet(clustTree, dist);
leafOrder = optimalleaforder(clustTree, dist);

fig = figure;
propertyeditor('on');
subplot(2, 1, 2);
h = plot([0.5, height(tbl) + 0.5], [0 0], 'LineWidth',  1, 'Color', 'black');
h.Annotation.LegendInformation.IconDisplayStyle = 'off';
scatterColors = distinguishable_colors(size(features, 1));
for s_id = 1:height(tbl)
    x = s_id;
    for f_id = 1:size(features, 1)
        real_id = leafOrder(s_id);
        y = tbl{real_id, features{f_id}};
        h = scatter(x, y, scatterSize, 'o', 'LineWidth',  0.1, 'MarkerEdgeColor', scatterColors(f_id, :), 'MarkerFaceColor', scatterColors(f_id, :), 'MarkerEdgeAlpha', opacity, 'MarkerFaceAlpha', opacity);
        hold all;
        if s_id == 1
            legend(h, sprintf('%s', featuresLabels{f_id}))
        else
            h.Annotation.LegendInformation.IconDisplayStyle = 'off';
        end
    end
end
xticklabels([]);
xticks(linspace(1, height(tbl), height(tbl)));
set(gca, 'FontSize', globalFontSize);
ylabel({'Normalized', 'Age Acceleration'}, 'Interpreter', 'latex');
set(gca, 'TickLabelInterpreter', 'latex')
set(gca, 'Position', [0.12 0.10 0.8 0.4]);
box on;
grid off;
legend(gca,'off');
legend('Location', legend_location, 'NumColumns', 1, 'Interpreter', 'latex');
legend('FontSize', legendFontSize);
xlim([0.5, height(tbl) + 0.5]);

subplot(2, 1, 1);
[lines, nodes, leafOrder] = dendrogram(clustTree, 0, 'reorder', leafOrder);
hold all;
xt = xticks;
xtl = xticklabels;
xticklabels([]);
xtickangle(90);
for s_id = 1:height(tbl)
    curr_group = tbl{leafOrder(s_id), 'Group'};
    if strcmp(curr_group, groups{1})
        color = colors{1};
    else
        color = colors{2};
    end
    
    h = rectangle('Position',[s_id - 0.5, -rect_height, 1, rect_height], 'FaceColor', color, 'EdgeColor', 'black', 'LineWidth', 0.1);
end
ylim([-rect_height, y_max]);
xlim([0.5, height(tbl) + 0.5]);
%axis tight;
set(gca, 'FontSize', globalFontSize);
ylabel('Distance', 'Interpreter', 'latex');
set(gca, 'TickLabelInterpreter', 'latex')
set(gca, 'Position', [0.12 0.5 0.8 0.4]);
box off;
ax=gca;
axes('position',ax.Position,'box','on','ytick',[],'xtick',[],'color','none')
box on;
hold all;





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

ololo = 1
