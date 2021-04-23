clear all;

part = 'v2';

x_var = 'Age';
x_label = 'Age';
xlims = [10; 100];
y_var = 'CXCL9';
y_label = 'CXCL9';
ylims = [10; 100];
y_label_acceleration = 'Age Acceleration';
fit_range_mode = 'lim'; %'lim'; % 'minmax';

group_feature = 'Group';
groups = {'Control', 'Disease'}';
group_base = 'Control';
colors = {[0 1 0], [1 0 1]}';

opacity = 0.5;
globalFontSize = 36;
legendFontSize = 18;
legend_location = 'NorthWest';
yLimAA = [-15, 70];

path = 'E:/YandexDisk/Work/pydnameth/unn_epic';
figures_path = sprintf('E:/YandexDisk/Work/pydnameth/unn_epic/figures/features/versus_byGroup/part(%s)', part);
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

status = tbl.(group_feature);
x_values = tbl.(x_var);
y_values = tbl.(y_var);

fig1 = figure;
propertyeditor('on');
grid on;

xs_all = {};
ys_all = {};
coeffs = table();
for g_id = 1:size(groups, 1)
    
    xs = tbl{strcmp(tbl.(group_feature), groups{g_id}), x_var};
    ys = tbl{strcmp(tbl.(group_feature), groups{g_id}), y_var};
   
    xs_all{g_id} = xs;
    ys_all{g_id} = ys;
    
    figure(fig1);
    hold all;
    color = colors{g_id};
    h = scatter(xs, ys, 250, 'o', 'LineWidth',  1, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', color, 'MarkerEdgeAlpha', opacity, 'MarkerFaceAlpha', opacity);
    legend(h, groups{g_id})
    
    T = table(xs, ys, 'VariableNames', {x_var, y_var});
    lm = fitlm(T, sprintf('%s~%s', y_var, x_var));
    R2 = lm.Rsquared.Ordinary;
    RMSE = lm.RMSE;
    %legend(h, sprintf('%s $(R^2=%0.2f)$', groups{g_id}, R2), 'Interpreter','latex');
    legend(h, sprintf('%s', groups{g_id}), 'Interpreter','latex');

    
    if strcmp(fit_range_mode, 'minmax')
        x_fit = [min(xs); max(xs)];
    else
        x_fit = [xlims(1); xlims(2)];
    end
    y_fit = lm.Coefficients{'(Intercept)','Estimate'} + x_fit * lm.Coefficients{x_var,'Estimate'};
    h = plot(x_fit, y_fit, 'LineWidth', 2, 'Color', color);
    h.Annotation.LegendInformation.IconDisplayStyle = 'off';
    if (strcmp(groups{g_id}, group_base))
        coeffs = lm.Coefficients;
    end
end

diffs_all = {};
for g_id = 1:size(groups, 1)
    xs = xs_all{g_id};
    ys = ys_all{g_id};
    
    diffs = zeros(size(xs, 1), 1);
    for p_id = 1:size(xs, 1)
        y_fit = coeffs{'(Intercept)','Estimate'} + xs(p_id) * coeffs{x_var, 'Estimate'};
        diffs(p_id) = ys(p_id) - y_fit;
    end

    diffs_all{g_id} = diffs;
end

figure(fig1);
hold all;
set(gca, 'FontSize', 40);
xlabel(x_label, 'Interpreter', 'latex');
set(gca, 'FontSize', 40);
ylabel(strrep(y_label,'_','\_'), 'Interpreter', 'latex');
ax = gca;
set(ax,'TickLabelInterpreter','Latex')
bissectrice_s = min(xlims(1), ylims(1));
bissectrice_f = max(xlims(2), ylims(2));
hold all;
h = plot([bissectrice_s bissectrice_f], [bissectrice_s bissectrice_f], 'k');
h.Annotation.LegendInformation.IconDisplayStyle = 'off';
legend(gca,'off');
legend('Location', legend_location, 'NumColumns', 1, 'Interpreter', 'latex');
box on;
xlim(xlims);
ylim(ylims);
fn_fig = sprintf('%s/x(%s)_y(%s)_group(%s)_scatter', figures_path, x_var, y_var, group_feature);
oqs_save_fig(fig1, fn_fig)
saveas(fig1, sprintf('%s.png', fn_fig));


agediff  = [];
mod_status = [];
for g_id = 1:size(groups, 1)
    agediff = vertcat(agediff, diffs_all{g_id});
    tmp = strings(size(diffs_all{g_id}, 1), 1);
    tmp(:) = groups{g_id};
    mod_status = vertcat(mod_status, tmp);
end

fig = figure;
propertyeditor('on');


subplot(1, 2, 2)
for g_id = 1:size(groups, 1)
    [f,xi] = ksdensity(diffs_all{g_id});
     
    hline = plot(f, xi, 'LineWidth', 2, 'Color', colors{g_id});
    legend(hline, sprintf('%s', groups{g_id}))
    set(gca, 'FontSize', globalFontSize);
    ylabel('')
    set(gca,'yticklabel',{[]})
    hold all;
end
ylim(yLimAA);
yl = get(gca, 'YLim');
legend(gca,'off');
legend('Location', legend_location, 'NumColumns', 1, 'Interpreter', 'latex');
legend('FontSize', legendFontSize);
title('Density', 'FontSize', globalFontSize, 'FontWeight', 'normal', 'Interpreter', 'latex');
set(gca, 'TickLabelInterpreter', 'latex')
set(gca, 'Position', [0.705 0.09 0.28 0.835]);
box on;
grid on;

subplot(1, 2, 1)
positions = 0.5 * linspace(1, size(groups, 1), size(groups, 1));
for g_id = 1:size(groups, 1)
    b = boxplot(diffs_all{g_id},'Notch', 'off', 'positions', positions(g_id), 'Colors', 'k');
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
    xs = positions(g_id) * ones(size(diffs_all{g_id}, 1), 1) + ((rand(size(diffs_all{g_id}))-0.5)/10);
    h = scatter(xs, diffs_all{g_id}, 100, 'o', 'LineWidth',  1, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', colors{g_id}, 'MarkerEdgeAlpha', opacity, 'MarkerFaceAlpha', opacity);
    h.Annotation.LegendInformation.IconDisplayStyle = 'off';
    hold all;
end
xticks(positions);
xticklabels(groups);
axis auto;
xlim([min(positions) - 0.3, max(positions) + 0.3])
ylabel(sprintf(y_label_acceleration), 'Interpreter', 'latex')
set(gca, 'TickLabelInterpreter', 'latex')
box on;
grid on;

pValueKW = kruskalwallis(agediff, mod_status, 'off');
if size(groups, 1) == 2
    pValue = ranksum(diffs_all{1}, diffs_all{2});
else
    pValue = pValueKW;
end
str = sprintf('%s p-value: %0.2e', y_label, pValue);
title(str, 'FontSize', globalFontSize-8, 'FontWeight', 'normal', 'Interpreter', 'latex');
set(gca, 'Position', [0.13 0.09 0.57 0.835]);
ylim(yl);
hold all;

fn_fig = sprintf('%s/x(%s)_y(%s)_group(%s)_KW', figures_path, x_var, y_var, group_feature);
oqs_save_fig(gcf, fn_fig)
saveas(gcf, sprintf('%s.png', fn_fig));
