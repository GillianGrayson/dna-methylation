clear all;

part = 'wo_noIntensity_detP';

cell_types = {'Bcell', 'CD4T', 'CD8T', 'Neu', 'NK'}';

groups = {'C', 'T'}';
colors = {[0 1 0], [1 0 1]}';

opacity = 0.65;

path = 'E:/YandexDisk/Work/pydnameth/unn_epic';
figures_path = 'E:/YandexDisk/Work/pydnameth/unn_epic/figures/cells/cells_group';
fn = sprintf('%s/cell_counts_part(%s).csv', path, part);
cells = readtable(fn);

fn = sprintf('%s/observables_part(%s).csv', path, part);
opts = detectImportOptions(fn);
opts = setvartype(opts, {'Sample_Group'}, 'string');
obs = readtable(fn, opts);

table = join(obs, cells);
table_c = table(table.Sample_Group=='C', :);
table_t = table(table.Sample_Group=='T', :);

status = table.Sample_Group;

for c_id = 1:size(cell_types, 1)
    cell_type = cell_types{c_id};
    cells_c = table_c.(cell_type);
    cells_t = table_t.(cell_type);
    cells_all = table.(cell_type);
    
    y_shift = max(cells_all) - min(cells_all);
    y_s = min(cells_all) - y_shift * 0.15;
    y_f = max(cells_all) + y_shift * 0.15;
    
    p = kruskalwallis(cells_all, status, 'on');
    grid on;
    propertyeditor('on')
    ylabel(cell_type, 'Interpreter','latex')
    set(gca, 'FontSize', 40);
    ylim([y_s y_f])
    a = get(get(gca,'children'),'children');
    t = get(a,'tag');
    idx = strcmpi(t,'box');
    boxes = a(idx);
    set(a,'linewidth',3);
    idx = strcmpi(t,'Outliers');
    outliers = a(idx);
    set(outliers,'visible','off')
    dim = [.15 .13 .3 .3];
    str = sprintf('Kruskal-Wallis p-value: %0.2e', p);
    tb = annotation('textbox', dim, 'String', str, 'verticalalignment', 'Bottom', 'FitBoxToText', 'on', 'FontSize', 24);
    hold all;
    h = scatter(1 * ones(size(cells_c, 1), 1).*(1+(rand(size(cells_c))-0.5)/10), cells_c, 100, 'o', 'LineWidth',  1, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', colors{1}, 'MarkerEdgeAlpha', opacity, 'MarkerFaceAlpha', opacity);
    h.Annotation.LegendInformation.IconDisplayStyle = 'off';
    hold all;
    h = scatter(2 * ones(size(cells_t, 1), 1).*(1+(rand(size(cells_t))-0.5)/10), cells_t, 100, 'o', 'LineWidth',  1, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', colors{2}, 'MarkerEdgeAlpha', opacity, 'MarkerFaceAlpha', opacity);
    h.Annotation.LegendInformation.IconDisplayStyle = 'off';
    box on;
    fn_fig = sprintf('%s/%s_group_part(%s)', figures_path, cell_type, part);
    oqs_save_fig(gcf, fn_fig) 
end
