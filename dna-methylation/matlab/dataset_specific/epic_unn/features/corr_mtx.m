clear all;

part = 'v2';

corrType = 'Pearson';
group = 'Disease';

is_pval = 0;

opacity = 0.5;
globalFontSize = 16;
xFontSize = 10;
yFontSize = 10;
numFontSize = 4;
xBinPos = 0.015;
yBinPos = 0.0167;
isNum = 1;

corr_x_features = importdata('corr_mtx/corr_x_features.txt');
corr_x_labels = importdata('corr_mtx/corr_x_labels.txt');
corr_y_features = importdata('corr_mtx/corr_y_features.txt');
corr_y_labels = importdata('corr_mtx/corr_y_labels.txt');
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

incKeys = {'Group', 'is_CMV'};
incVals = {{group}, {'yes'}};
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
        [rho, pval] = corr(X, Y, 'Type', corrType);
        if is_pval == 1
            cm(x_id, y_id) = -log10(pval);
        else
            cm(x_id, y_id) = rho;
        end
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
if is_pval == 1
    c_shift = max(cm(~isinf(cm))) - (-log10(0.05));
    c_add = c_shift / 100;
    c_min = -log10(0.05) - c_add;
    c_max = max(cm(~isinf(cm)));
    
    if c_max < c_min
        cmap = getPyPlot_cMap('winter', 100);
    else
        caxis([c_min, c_max])
        cmap1 = getPyPlot_cMap('Reds', 100);
        cmap2 = getPyPlot_cMap('winter', 100);
        cmap = vertcat(cmap2(70, :), cmap1);
    end
else
    caxis([-1 1])
    cmap = getPyPlot_cMap('bwr', 128);
end
colormap(cmap);
h = colorbar('northoutside');
if is_pval == 1
    title(h, {corrType;'$-\log_{10}($p-value$)$';}, 'FontSize', 14, 'Interpreter','Latex');
else
    title(h, {corrType;'Correlation';}, 'FontSize', 14, 'Interpreter','Latex');
end
set(gca, 'FontSize', globalFontSize);
set(gca,'YDir','normal');
ax = gca;
xticks(xs);
xticklabels(corr_x_labels);
xtickangle(90);
ax.XAxis.FontSize = xFontSize;
yticks(ys);
yticklabels(strrep(corr_y_labels,'_','\_'));
if isNum == 1
    for x_id = 1:xSize
        for y_id = 1:ySize
            pos_x = (x_id - 0.3);
            pos_y = y_id;
            
            msg = sprintf('%0.2f', cm(x_id, y_id));
            text(pos_x, pos_y, msg, 'FontSize', numFontSize, 'Interpreter', 'latex', 'Rotation', 0);
        end
    end
end
ax.YAxis.FontSize = xFontSize;
set(ax,'TickLabelInterpreter','Latex')
set(gca, 'Position', position);
a = gca;
b = copyobj(a, gcf);
set(b, 'Xcolor', 'none', 'YColor', 'none', 'XTickLabel', [], 'YTickLabel', [])
hold all;

if is_pval == 1
    fn_fig = sprintf('%s/%s_%s_pValue', figures_path, corrType, group);
else
    fn_fig = sprintf('%s/%s_%s_corrCoeff', figures_path, corrType, group);
end
oqs_save_fig(gcf, fn_fig)

