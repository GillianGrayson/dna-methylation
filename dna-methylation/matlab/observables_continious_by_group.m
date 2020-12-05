figures_path = sprintf('%s/figures/observables/part(%s)/', dataset_path, part);
if ~exist(figures_path, 'dir')
    mkdir(figures_path)
end

continious = 'age';
continious_lims = [8; 100];

group_by = 'gender';
target_vals = {'F', 'M'}';
colors = {[1 0 0],[0 0 1]}';
continious_bin = 3;
opacity = 0.5;

x = obs.(continious);
min_x = min(x);
max_x = max(x);
shift_x = max_x - min_x;
num_bins = floor(shift_x / continious_bin);
min_x = floor(min_x - 0.05 * shift_x);
max_x = ceil(max_x + 0.05 * shift_x);
edges = (min_x : continious_bin : max_x)';

fig = figure;
propertyeditor('on');
for t_id = 1:size(target_vals, 1)
    val = target_vals{t_id};
    
    sub_data = obs(cell2mat(obs.(group_by)) == val, :);
    sub_x = sub_data.(continious);
    
    h = histogram(sub_x, edges, 'FaceColor', colors{t_id}, 'FaceAlpha', opacity);
    leg = legend(h, sprintf('%s:%s(%d)', replace(group_by, {':', '*', '_'}, ' '), val, size(sub_x, 1)));
    hold all;
end

set(gca, 'FontSize', 40);
xlabel(continious, 'Interpreter', 'latex');
set(gca, 'FontSize', 40);
ylabel('Number of Subjects', 'Interpreter', 'latex');
box on;
grid on;
legend(gca,'off');
legend('Location','Northwest','NumColumns',1)
legend('FontSize', 12);
xlim([continious_lims(1), continious_lims(2)])

fn_fig = sprintf('%s/(%s)_by(%s)', figures_path, continious, group_by);
oqs_save_fig(fig, fn_fig)
saveas(gcf, sprintf('%s.png', fn_fig));
