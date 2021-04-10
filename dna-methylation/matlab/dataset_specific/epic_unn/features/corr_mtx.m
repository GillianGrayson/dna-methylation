clear all;

part = 'v2';

corrType = 'Pearson';
group = 'Control';

opacity = 0.5;
globalFontSize = 16;
xFontSize = 10;
yFontSize = 10;
xBinPos = 0.015;
yBinPos = 0.0167;

corr_x_features = importdata('corr_x_features.txt');
corr_x_labels = importdata('corr_x_labels.txt');
corr_y_features = importdata('corr_y_features.txt');
corr_y_labels = importdata('corr_y_labels.txt');
xSize = size(corr_x_features, 1);
ySize = size(corr_y_features, 1);

position = [0.1, 0.1, xBinPos * xSize, yBinPos * ySize];

path = 'E:/YandexDisk/Work/pydnameth/unn_epic';
figures_path = sprintf('E:/YandexDisk/Work/pydnameth/unn_epic/figures/features/corr_mtx/part(%s)', part);
if ~exist(figures_path, 'dir')
    mkdir(figures_path)
end
fn = sprintf('%s/all_data/table_part(%s).xlsx', path, part);
opts = detectImportOptions(fn);
tbl = readtable(fn, opts);

incKeys = {'Group'};
incVals = {{group}};
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

cm = zeros(xSize, ySize);
for x_id = 1:xSize
    for y_id = 1:ySize
        X = tbl.(corr_x_features{x_id});
        Y = tbl.(corr_y_features{y_id});
        rho = corr(X, Y, 'Type', corrType);
        cm(x_id, y_id) = rho;
    end
end

xs = linspace(1, xSize, xSize)';
ys = linspace(1, ySize, ySize)';

fig = figure;
propertyeditor('on');
imagesc(xs, ys, cm');
set(gca, 'FontSize', globalFontSize);
xlabel('', 'Interpreter', 'latex');
ylabel('', 'Interpreter', 'latex');
caxis([-1 1])
cmap = getPyPlot_cMap('bwr', 128);
%cmap = customcolormap([0 0.5 1], [1 0 0; 1 1 1; 0 0 1]);
colormap(cmap);
h = colorbar('northoutside');
title(h, {corrType;'Correlation';'Coefficient'}, 'FontSize', 14, 'Interpreter','Latex');
set(gca, 'FontSize', globalFontSize);
set(gca,'YDir','normal');
ax = gca;
xticks(xs);
xticklabels(corr_x_labels);
xtickangle(90);
ax.XAxis.FontSize = xFontSize;
yticks(ys);
yticklabels(strrep(corr_y_labels,'_','\_'));
ax.YAxis.FontSize = xFontSize;
set(ax,'TickLabelInterpreter','Latex')
set(gca, 'Position', position);
a = gca;
b = copyobj(a, gcf);
set(b, 'Xcolor', 'none', 'YColor', 'none', 'XTickLabel', [], 'YTickLabel', [])
hold all;

fn_fig = sprintf('%s/%s_%s', figures_path, corrType, group);
oqs_save_fig(gcf, fn_fig)

