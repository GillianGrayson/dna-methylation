clear all;

x_var = 'Age';
target = 'Sample_Group';
target_vals = {'C', 'T'}';
colors = {[0 1 0],[1 0 1]}';
age_bin = 3;
FaceAlpha = 0.5;

part = 'wo_noIntensity_detP';

path = 'E:/YandexDisk/Work/pydnameth/unn_epic';
figures_path = 'E:/YandexDisk/Work/pydnameth/unn_epic/figures/observables';
if ~exist(figures_path, 'dir')
    mkdir(figures_path)
end

fn = sprintf('%s/observables_part(%s).csv', path, part);
data = readtable(fn);
x = data.(x_var);
min_x = min(x);
max_x = max(x);
shift_x = max_x - min_x;
num_bins = floor(shift_x / age_bin);
min_x = floor(min_x - 0.05 * shift_x);
max_x = ceil(max_x + 0.05 * shift_x);
edges = (min_x : age_bin : max_x)';

fig = figure;
propertyeditor('on');
for t_id = 1:size(target_vals, 1)
    val = target_vals{t_id};
    
    sub_data = data(cell2mat(data.(target)) == val, :);
    sub_x = sub_data.(x_var);
    
    h = histogram(sub_x, edges, 'FaceColor', colors{t_id}, 'FaceAlpha', FaceAlpha);
    leg = legend(h, sprintf('%s:%s(%d)', replace(target, {':', '*', '_'}, ' '), val, size(sub_x, 1)));
    hold all;
end


set(gca, 'FontSize', 40);
xlabel(x_var, 'Interpreter', 'latex');
set(gca, 'FontSize', 40);
ylabel('Number of subjects', 'Interpreter', 'latex');
grid on;
legend(gca,'off');
legend('Location','Northwest','NumColumns',1)
legend('FontSize', 12);

fn_fig = sprintf('%s/(%s)_part(%s)', figures_path, target, part);
oqs_save_fig(fig, fn_fig)
saveas(gcf, sprintf('%s.png', fn_fig));
