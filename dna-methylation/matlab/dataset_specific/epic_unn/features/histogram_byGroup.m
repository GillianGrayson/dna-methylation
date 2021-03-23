clear all;

%x_var = 'Age';
%x_label = 'Age';
x_var = 'Dialysis_months_';
x_label = 'Dialysis (months)';
target = 'Group';
%target_vals = {'F', 'M'}';
%colors = {[1 0 0],[0 0 1]}';
target_vals = {'Disease'}';
colors = {[1 0 1]}';
bin_size = 5;
FaceAlpha = 0.5;

part = 'v2';

path = 'E:/YandexDisk/Work/pydnameth/unn_epic';
figures_path = sprintf('E:/YandexDisk/Work/pydnameth/unn_epic/figures/features/histogram_byGroup/part(%s)', part);
if ~exist(figures_path, 'dir')
    mkdir(figures_path)
end

fn = sprintf('%s/all_data/table_part(%s).xlsx', path, part);
opts = detectImportOptions(fn);
opts = setvartype(opts, {target}, 'string');
data = readtable(fn, opts);
x = data.(x_var);
min_x = min(x);
max_x = max(x);
shift_x = max_x - min_x;
num_bins = floor(shift_x / bin_size);
min_x = floor(min_x - 0.05 * shift_x);
max_x = ceil(max_x + 0.05 * shift_x);
edges = (min_x : bin_size : max_x)';

fig = figure;
propertyeditor('on');
for t_id = 1:size(target_vals, 1)
    val = string(target_vals{t_id});
    
    sub_data = data(strcmp(cell2mat(data.(target)), string(val)), :);
    sub_x = sub_data.(x_var);
    
    h = histogram(sub_x, edges, 'FaceColor', colors{t_id}, 'FaceAlpha', FaceAlpha);
    leg = legend(h, sprintf('%s:%s(%d)', replace(target, {':', '*', '_'}, ' '), val, size(sub_x, 1)));
    hold all;
end

set(gca, 'FontSize', 40);
xlabel(x_label, 'Interpreter', 'latex');
set(gca, 'FontSize', 40);
ylabel('Number of subjects', 'Interpreter', 'latex');
grid on;
legend(gca,'off');
legend('Location','Northwest','NumColumns',1)
legend('FontSize', 28);

fn_fig = sprintf('%s/x(%s)_group(%s)', figures_path, x_var, target);
oqs_save_fig(fig, fn_fig)
