clear all;

features_types = {'CD4T', 'NK', 'Mono', 'Gran', 'PlasmaBlast', 'CD8pCD28nCD45RAn', 'CD8.naive'}';

part = 'v2';

group_feature = 'Group';
groups = {'Control', 'Disease'}';
colors = {[0 1 0], [1 0 1]}';

opacity = 0.65;
gap = 0.7;
globalFontSize = 40;
scatterSize = 30;
boxPlotLineWidth = 2;
xFontSize = 30;
textShift = 0.18;
textFontSize = 16;
textYAbove = 0.05;
ylims = [0; 1];
legend_location = 'NorthWest';


path = 'E:/YandexDisk/Work/pydnameth/unn_epic';
figures_path = sprintf('E:/YandexDisk/Work/pydnameth/unn_epic/figures/features/boxplots_byGroup/part(%s)', part);
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

fig = figure;
propertyeditor('on');
positions = linspace(0.7, 0.7 * size(features_types, 1), size(features_types, 1))';

for f_id = 1:size(features_types, 1)
    feature = strrep(features_types{f_id},'.','_');
    
    featuresByGroup = {};
    for g_id = 1:size(groups, 1)
        vars = tbl{strcmp(tbl.(group_feature), groups{g_id}), feature};
        featuresByGroup{g_id} = vars;
    end
    
    featuresOrdered  = [];
    featuresStatus = [];
    for g_id = 1:size(groups, 1)
        featuresOrdered = vertcat(featuresOrdered, featuresByGroup{g_id});
        tmp = strings(size(featuresByGroup{g_id}, 1), 1);
        tmp(:) = groups{g_id};
        featuresStatus = vertcat(featuresStatus, tmp);
    end
    
    for g_id = 1:size(groups, 1)
        position = positions(f_id) + 0.09 * sign(g_id - 1.5);
        b = boxplot(featuresByGroup{g_id}, 'Notch', 'off', 'positions', [position], 'Colors', 'k');
        set(gca, 'FontSize', globalFontSize);
        all_items = handle(b);
        tags = get(all_items,'tag');
        idx = strcmpi(tags,'box');
        boxes = all_items(idx);
        set(all_items, 'linewidth', boxPlotLineWidth)
        idx = strcmpi(tags,'Outliers');
        outliers = all_items(idx);
        set(outliers, 'visible', 'off')
        hold all;
        vars = position * ones(size(featuresByGroup{g_id}, 1), 1) + ((rand(size(featuresByGroup{g_id}))-0.5)/10);
        h = scatter(vars, featuresByGroup{g_id}, scatterSize, 'o', 'LineWidth',  0.1, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', colors{g_id}, 'MarkerEdgeAlpha', opacity, 'MarkerFaceAlpha', opacity);
        
        if f_id == 1
            legend(h, groups{g_id});
        else
            h.Annotation.LegendInformation.IconDisplayStyle = 'off';
        end
        hold all;
    end
    
    pValueKW = kruskalwallis(featuresOrdered, featuresStatus, 'off');
    if size(groups, 1) == 2
        pValue = ranksum(featuresByGroup{1}, featuresByGroup{2});
    else
        pValue = pValueKW;
    end
    
    pos_x = positions(f_id) - textShift;
    pos_y = max(featuresOrdered) + textYAbove;
    msg = sprintf('$\\mathrm{p-value}$:\n$%0.2e$', pValue);
    text(pos_x, pos_y, msg, 'FontSize', textFontSize, 'Interpreter', 'latex', 'Rotation', 0);
    
end

xticks(positions);
xticklabels(features_types);
axis auto;
xlim([min(positions) - 0.3, max(positions) + 0.3])
set(gca, 'TickLabelInterpreter', 'latex')
box on;
grid on;
ax = gca;
ax.XAxis.FontSize = xFontSize;
ylim(ylims);
legend(gca,'off');
legend('Location', legend_location, 'NumColumns', 1, 'Interpreter', 'latex');


tmp = strjoin(features_types, '_');
fn_fig = sprintf('%s/%s_group(%s)', figures_path, tmp, group_feature);
oqs_save_fig(gcf, fn_fig)
