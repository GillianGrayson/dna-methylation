clear all;

part = 'v2';
pdist_metric = 'cosine'; %'cosine';
onlyDendogram = 0;
rect_height = 0.1;
y_max = 1.5;

features = importdata('individual/features.txt');
featuresLabels = importdata('individual/labels.txt');

group_feature = 'Group';
groups = {'Control', 'Disease'}';
colors = {[0 1 0], [1 0 1]}';

scatterSize = 15;
opacity = 0.65;
globalFontSize = 28;
legendFontSize = 10;
legend_location = 'NorthEast';

path = 'E:/YandexDisk/Work/pydnameth/unn_epic';
figures_path = sprintf('E:/YandexDisk/Work/pydnameth/unn_epic/figures/features/individual/part(%s)', part);
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

if onlyDendogram ~= 1
    subplot(2, 1, 1);
end

%[lines, nodes, leafOrder] = dendrogram(clustTree, 0, 'reorder', leafOrder);
[lines, nodes, leafOrder] = dendrogram(clustTree, 0);
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
if onlyDendogram ~= 1
    set(gca, 'Position', [0.12 0.52 0.87 0.4]);
    box off;
    ax=gca;
    axes('position',ax.Position,'box','on','ytick',[],'xtick',[],'color','none')
end
box on;
hold all;

if onlyDendogram ~= 1
    subplot(2, 1, 2);
    h = plot([0.5, height(tbl) + 0.5], [0 0], 'LineWidth',  1, 'Color', 'black');
    h.Annotation.LegendInformation.IconDisplayStyle = 'off';
    hold all
    scatterColors = distinguishable_colors(size(features, 1));
    xs = linspace(1, height(tbl), height(tbl));
    for f_id = 1:size(features, 1)
        ys = tbl{leafOrder, features{f_id}};
        h = scatter(xs, ys, scatterSize, 'o', 'LineWidth',  0.1, 'MarkerEdgeColor', scatterColors(f_id, :), 'MarkerFaceColor', scatterColors(f_id, :), 'MarkerEdgeAlpha', opacity, 'MarkerFaceAlpha', opacity);
        hold all;
        legend(h, sprintf('%s', featuresLabels{f_id}))
    end
    xticklabels([]);
    xticks(linspace(1, height(tbl), height(tbl)));
    set(gca, 'FontSize', globalFontSize);
    ylabel({'Age Acceleration'}, 'Interpreter', 'latex');
    set(gca, 'TickLabelInterpreter', 'latex')
    set(gca, 'Position', [0.12 0.10 0.87 0.42]);
    box on;
    grid off;
    legend(gca,'off');
    legend('Location', legend_location, 'NumColumns', 1, 'Interpreter', 'latex');
    legend('FontSize', legendFontSize);
    xlim([0.5, height(tbl) + 0.5]);
end

fn_fig = sprintf('%s/%s', figures_path, pdist_metric);
oqs_save_fig(gcf, fn_fig)
