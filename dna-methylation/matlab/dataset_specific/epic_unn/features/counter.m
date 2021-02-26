clear all;

part = 'wo_noIntensity_detP_H17+_negDNAmPhenoAge';

count_target = 'yes';
count_limit = 3;

features_type = 'drug';
y_label = 'Medicines';

opacity = 0.65;
fontSizeX = 36;
fontSizeY = 20;

path = 'E:/YandexDisk/Work/pydnameth/unn_epic';
figures_path = sprintf('E:/YandexDisk/Work/pydnameth/unn_epic/figures/features/counter/part(%s)', part);
if ~exist(figures_path, 'dir')
    mkdir(figures_path)
end

target_features = importdata(sprintf('%s/all_data/%s_list.txt', path, features_type));

fn = sprintf('%s/all_data/table_part(%s).xlsx', path, part);
opts = detectImportOptions(fn);
tbl = readtable(fn, opts);

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
