clear all;

part = 'wo_noIntensity_detP_H17+_negDNAmPhenoAge';

target = 'IL_13';
group_feature = 'Group';
groups = {'Control', 'Disease'}';

colors = {[0 1 0], [1 0 1]}';

opacity = 0.65;

path = 'E:/YandexDisk/Work/pydnameth/unn_epic';
figures_path = sprintf('E:/YandexDisk/Work/pydnameth/unn_epic/figures/features/boxplot_byGroup/part(%s)', part);
if ~exist(figures_path, 'dir')
    mkdir(figures_path)
end
fn = sprintf('%s/all_data/table_part(%s).xlsx', path, part);
opts = detectImportOptions(fn);
opts = setvartype(opts, {group_feature}, 'string');
obs = readtable(fn, opts);

status = obs.(group_feature);
features = obs.(target);

features_byGroup = {};
for g_id = 1:size(groups, 1)
    
    accs = [];
    for id = 1 : size(features, 1)
        if status{id} == groups{g_id}
            accs = vertcat(accs, features(id));
        end
    end
    
    features_byGroup{g_id} = accs;
end

if size(groups, 1) > 1
    
    features_ordered  = [];
    mod_status = [];
    for g_id = 1:size(groups, 1)
        features_ordered = vertcat(features_ordered, features_byGroup{g_id});
        tmp = strings(size(features_byGroup{g_id}, 1), 1);
        tmp(:) = groups{g_id};
        mod_status = vertcat(mod_status, tmp);
    end
    
    fig = figure;
    propertyeditor('on');
    positions = 0.5 * linspace(1, size(groups, 1), size(groups, 1));
    for g_id = 1:size(groups, 1)
        b = boxplot(features_byGroup{g_id},'Notch', 'off', 'positions', positions(g_id), 'Colors', 'k');
        set(gca, 'FontSize', 40);
        all_items = handle(b);
        tags = get(all_items,'tag');
        idx = strcmpi(tags,'box');
        boxes = all_items(idx);
        set(all_items,'linewidth',3)
        idx = strcmpi(tags,'Outliers');
        outliers = all_items(idx);
        set(outliers, 'visible', 'off')
        hold all;
        xs = positions(g_id) * ones(size(features_byGroup{g_id}, 1), 1) + ((rand(size(features_byGroup{g_id}))-0.5)/10);
        h = scatter(xs, features_byGroup{g_id}, 100, 'o', 'LineWidth',  1, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', colors{g_id}, 'MarkerEdgeAlpha', opacity, 'MarkerFaceAlpha', opacity);
        h.Annotation.LegendInformation.IconDisplayStyle = 'off';
        hold all;
    end
    xticks(positions);
    xticklabels(groups);
    axis auto;
    xlim([min(positions) - 0.3, max(positions) + 0.3])
    set(gca, 'TickLabelInterpreter', 'latex')
    ylabel(target, 'Interpreter', 'latex')
    box on;
    grid on;
    p = kruskalwallis(features_ordered, mod_status, 'off');
    str = sprintf('Kruskal-Wallis p-value: %0.2e', p);
    title(str, 'FontSize', 30, 'FontWeight', 'normal', 'Interpreter', 'latex');
    hold all;
    
    fn_fig = sprintf('%s/%s_group(%s)', figures_path, target, group_feature);
    oqs_save_fig(gcf, fn_fig)
end
