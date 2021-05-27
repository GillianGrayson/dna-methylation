clear all;

dataset = 'EPIC';

x_var = 'age';
x_label = 'Age';
xlims = [0; 120];
y_var = 'age_pred';
y_label = 'Estimated Age';
ylims = [0; 110];

opacity = 0.5;
globalFontSize = 36;
legendFontSize = 18;
legend_location = 'NorthWest';
yLimAA = [-15, 70];

path = sprintf('E:/YandexDisk/Work/pydnameth/unn_epic/agena/%s', dataset);
figures_path = path;
if ~exist(figures_path, 'dir')
    mkdir(figures_path)
end

fn = sprintf('%s/table.xlsx', path);
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

fig1 = figure;
propertyeditor('on');
grid on;

xs = tbl{:, x_var};
ys = tbl{:, y_var};


T = table(xs, ys, 'VariableNames', {x_var, y_var});
lm = fitlm(T, sprintf('%s~%s', y_var, x_var));
R2 = lm.Rsquared.Ordinary;
RMSE = lm.RMSE;
MAE = mae(xs, ys);

color = 'red';
h = scatter(xs, ys, 100, 'o', 'LineWidth',  1, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', color, 'MarkerEdgeAlpha', opacity, 'MarkerFaceAlpha', opacity);
legend(h, sprintf('$R^2=%0.2f$  $RMSE=%0.2f$  $MAE=%0.2f$', R2, RMSE, MAE), 'Interpreter',' latex');
hold all;
    
x_fit = [min(xs); max(xs)];
y_fit = lm.Coefficients{'(Intercept)','Estimate'} + x_fit * lm.Coefficients{x_var,'Estimate'};
h = plot(x_fit, y_fit, 'LineWidth', 2, 'Color', 'k');
h.Annotation.LegendInformation.IconDisplayStyle = 'off';

hold all;
set(gca, 'FontSize', 40);
xlabel(x_label, 'Interpreter', 'latex');
set(gca, 'FontSize', 40);
ylabel(y_label, 'Interpreter', 'latex');
ax = gca;
set(ax,'TickLabelInterpreter','Latex')
bissectrice_s = min(xlims(1), ylims(1));
bissectrice_f = max(xlims(2), ylims(2));
hold all;
legend(gca, 'off');
legend('Location', legend_location, 'NumColumns', 1, 'Interpreter', 'latex');
legend('FontSize', 30);
title(dataset, 'FontSize', globalFontSize, 'FontWeight', 'normal', 'Interpreter', 'latex');
box on;
xlim(xlims);
ylim(ylims);
fn_fig = sprintf('%s/x(%s)_y(%s)_scatter', figures_path, x_var, y_var);
oqs_save_fig(fig1, fn_fig)

