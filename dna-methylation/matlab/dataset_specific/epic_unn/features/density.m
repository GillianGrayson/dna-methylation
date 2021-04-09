clear all;

features_types = {'CD4T', 'NK', 'Mono', 'Gran', 'PlasmaBlast', 'CD8pCD28nCD45RAn', 'CD8.naive'}';

part = 'v2';

x_label = 'Cells';
xlims = [-inf; inf];
y_label = 'PDF';
legend_location = 'NorthEast';


path = 'E:/YandexDisk/Work/pydnameth/unn_epic';
figures_path = sprintf('E:/YandexDisk/Work/pydnameth/unn_epic/figures/features/density/part(%s)', part);
if ~exist(figures_path, 'dir')
    mkdir(figures_path)
end
fn = sprintf('%s/all_data/table_part(%s).xlsx', path, part);
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

colors = distinguishable_colors(size(features_types, 1));

fig = figure;
propertyeditor('on');
grid on;
for f_id = 1:size(features_types, 1)
    feat = tbl.(strrep(features_types{f_id},'.','_'));
    
    [f,xi] = ksdensity(feat);
    
    color = colors(f_id, :);
    
    hline = plot(xi, f, 'LineWidth', 2, 'Color', color);
    legend(hline, sprintf('%s', features_types{f_id}))
    set(gca, 'FontSize', 30);
    xlabel(x_label, 'Interpreter', 'latex');
    set(gca, 'FontSize', 30);
    ylabel('PDF', 'Interpreter', 'latex');
    hold all;
end

xlim(xlims);
legend(gca,'off');
legend('Location', legend_location, 'NumColumns', 1, 'Interpreter', 'latex');
box on;

tmp = strjoin(features_types, '_');
fn_fig = sprintf('%s/%s', figures_path, tmp);
oqs_save_fig(fig, fn_fig)



