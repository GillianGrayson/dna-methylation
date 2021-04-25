clear all;

part = 'v2';

x_var = 'Age';
x_label = 'Age';
xlims = [10, 100];

xNumPlots = 3;
yNumPlots = 4;

scatterSize = 15;
opacity = 0.5;
globalFontSize = 16;
legendFontSize = 6;
legend_location = 'NorthWest';

group_feature = 'Group';
groups = {'Control', 'Disease'}';
group_base = 'Control';
colors = {[0 1 0], [1 0 1]}';

path = 'E:/YandexDisk/Work/pydnameth/unn_epic';
figures_path = sprintf('E:/YandexDisk/Work/pydnameth/unn_epic/figures/features/manyPlots_byGroup/part(%s)', part);
if ~exist(figures_path, 'dir')
    mkdir(figures_path)
end
fn = sprintf('%s/all_data/table_part(%s).xlsx', path, part);
opts = detectImportOptions(fn);
tbl = readtable(fn, opts);

features = importdata('manyPlots_byGroup/features.txt');
featuresLabels = importdata('manyPlots_byGroup/labels.txt');
ylims = importdata('manyPlots_byGroup/ylims.txt');

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

block = 0;
for f_id = 1:size(features, 1)
    
    mod_id = mod(f_id - 1, xNumPlots * yNumPlots);
    mod_id_x = floor(mod_id/xNumPlots) + 1;
    mod_id_y = mod_id - (mod_id_x - 1) * xNumPlots + 1;
    
    if mod_id == 0
        fig = figure;
        propertyeditor('on');
        block = block + 1;
    end
    
    subplot(yNumPlots, xNumPlots, mod_id + 1);
    
    for g_id = 1:size(groups, 1)
        
        xs = tbl{strcmp(tbl.(group_feature), groups{g_id}), x_var};
        ys = tbl{strcmp(tbl.(group_feature), groups{g_id}), features{f_id}};
        
        hold all;
        color = colors{g_id};
        h = scatter(xs, ys, scatterSize, 'o', 'LineWidth',  0.1, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', color, 'MarkerEdgeAlpha', opacity, 'MarkerFaceAlpha', opacity);
        legend(h, sprintf('%s', groups{g_id}), 'Interpreter','latex');
        
        T = table(xs, ys, 'VariableNames', {x_var,  features{f_id}});
        lm = fitlm(T, sprintf('%s~%s',  features{f_id}, x_var));
        R2 = lm.Rsquared.Ordinary;
        RMSE = lm.RMSE;
        x_fit = [min(xs); max(xs)];
        y_fit = lm.Coefficients{'(Intercept)','Estimate'} + x_fit * lm.Coefficients{x_var,'Estimate'};
        %h = plot(x_fit, y_fit, 'LineWidth', 1, 'Color', color);
        %h.Annotation.LegendInformation.IconDisplayStyle = 'off';
    end
    
    hold all;
    set(gca, 'FontSize', globalFontSize);
    xlabel(x_label, 'Interpreter', 'latex');
    ylabel(strrep(featuresLabels{f_id},'_','\_'), 'Interpreter', 'latex');
    ax = gca;
    set(ax,'TickLabelInterpreter','Latex')
    legend(gca,'off');
    legend('Location', legend_location, 'NumColumns', 1, 'Interpreter', 'latex');
    legend('FontSize', legendFontSize);
    box on;
    hold all;
    ylim(ylims(f_id, :));
    xlim(xlims);
    
    if (mod_id == 11) || (f_id == size(features, 1))
        fn_fig = sprintf('%s/x(%s)_block(%d)', figures_path, x_var, block);
        oqs_save_fig(fig, fn_fig)
    end
end

