clear all;

part = 'v2';

count_target = 'yes';
count_limit = 5;

features_type = 'drugs';
y_label = 'Medicines';

opacity = 0.65;
fontSizeX = 36;
fontSizeY = 20;

path = 'E:/YandexDisk/Work/pydnameth/unn_epic';
figures_path = sprintf('E:/YandexDisk/Work/pydnameth/unn_epic/figures/features/counter/part(%s)', part);
if ~exist(figures_path, 'dir')
    mkdir(figures_path)
end

target_features = importdata(sprintf('%s/all_data/%s.txt', path, features_type));

fn = sprintf('%s/all_data/table_part(%s).xlsx', path, part);
opts = detectImportOptions(fn);
tbl = readtable(fn, opts);

keySet_inc = {'Group'};
valueSet_inc = {{'Disease'}};
keySet_dec = {};
valueSet_dec = {{}};
base_filter = true(height(tbl), 1);
if size(keySet_inc, 1) > 0
    fitering_inc = containers.Map(keySet_inc,valueSet_inc);
else
    fitering_inc = containers.Map();
end
for k = keys(fitering_inc)
    b = false(height(tbl), 1);
    vals = fitering_inc(k{1});
    column = tbl.(k{1});
    for v_id = 1:size(vals, 2)
        if iscell(column)
            b = b | strcmp(column, vals{v_id});
        else
            b = b | (column == vals{v_id});
        end
    end
    base_filter = base_filter & b;
end
if size(keySet_dec, 1) > 0
    fitering_dec = containers.Map(keySet_dec,valueSet_dec);
else
    fitering_dec = containers.Map();
end
for k = keys(fitering_dec)
    b = false(height(tbl), 1);
    vals = fitering_dec(k{1});
    column = tbl.(k{1});
    for v_id = 1:size(vals, 2)
        if iscell(column)
            b = b | (~strcmp(column, vals{v_id}));
        else
            b = b | (column ~= vals{v_id});
        end
    end
    base_filter = base_filter & b;
end
sum(base_filter)

tbl = tbl(base_filter, :);

counts = zeros(size(target_features, 1), 1);
for f_id = 1:size(target_features, 1)
    feat = tbl.(strrep(target_features{f_id},'.','_'));
    counts(f_id) = size(feat(strcmp(feat,count_target)), 1);
end

[counts, order] = sort(counts);
target_features = target_features(order);

order = counts>=count_limit;
counts = counts(order);
target_features = target_features(order);

fig = figure;
propertyeditor('on');

barh(counts, 'FaceColor', [0.7 0.7 0.7]);
yticks(linspace(1, size(counts, 1), size(counts, 1)))
ylim([0.5, size(counts, 1) + 0.5])
hold all;
set(gca, 'yTickLabel', target_features);
ax = gca;
ax.YAxis.FontSize = fontSizeY;
set(gca, 'TickLabelInterpreter', 'none')
xlabel('Number of subjects', 'Interpreter', 'latex', 'FontSize', fontSizeX + 4);
ylabel(y_label, 'Interpreter', 'latex', 'FontSize', fontSizeX + 6);
ax.XAxis.FontSize = fontSizeX;
grid on;

fn_fig = sprintf('%s/%s', figures_path,  features_type);
oqs_save_fig(fig, fn_fig)
saveas(gcf, sprintf('%s.png', fn_fig));
