clear all;

part = 'v2_Controls';

x_var = 'Age';
x_label = 'Age';
xlims = [0; 100];
y_var = 'AgeEstimation';
y_label = 'Age Estimation';
ylims = [0; 100];
y_label_acceleration = 'Age Acceleration';
fit_range_mode = 'lim'; %'lim'; % 'minmax';
legend_location = 'NorthWest';

group_feature = 'Group';
groups = {'Control', 'Disease'}';
group_base = 'Control';
colors = {[0 1 0], [1 0 1]}';

opacity = 0.5;

path = 'E:/YandexDisk/Work/pydnameth/unn_epic';
fn = sprintf('%s/all_data/table_part(%s).xlsx', path, part);
opts = detectImportOptions(fn);
opts = setvartype(opts, {group_feature}, 'string');
tbl = readtable(fn, opts);

incKeys = {'Group'};
incVals = {{'Control'}};
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

eeaa = tbl.('EEAA');
age = tbl.(x_var);
ageLin = age + eeaa;

fig1 = figure;
propertyeditor('on');
grid on;

g_id = 1;
color = colors{g_id};
h = scatter(age, ageLin, 250, 'o', 'LineWidth',  1, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', color, 'MarkerEdgeAlpha', opacity, 'MarkerFaceAlpha', opacity);
legend(h, groups{g_id});

T = table(age, ageLin, 'VariableNames', {x_var, y_var});
lm = fitlm(T, sprintf('%s~%s', y_var, x_var));
resid = lm.Residuals.Raw;
fprintf('EEAA check: %0.16e\n', norm(eeaa - resid))
R2 = lm.Rsquared.Ordinary;
RMSE = lm.RMSE;
%legend(h, sprintf('%s $(R^2=%0.2f)$', groups{g_id}, R2), 'Interpreter','latex');
legend(h, sprintf('%s', groups{g_id}), 'Interpreter','latex');

if (strcmp(groups{g_id}, group_base))
    if strcmp(fit_range_mode, 'minmax')
        x_fit = [min(xs); max(xs)];
    else
        x_fit = [xlims(1); xlims(2)];
    end
    y_fit = lm.Coefficients{'(Intercept)','Estimate'} + x_fit * lm.Coefficients{x_var,'Estimate'};
    h = plot(x_fit, y_fit, 'LineWidth', 2, 'Color', color);
    h.Annotation.LegendInformation.IconDisplayStyle = 'off';
    coeffs = lm.Coefficients;
end


hold all;
set(gca, 'FontSize', 40);
xlabel(x_label, 'Interpreter', 'latex');
set(gca, 'FontSize', 40);
ylabel(y_label, 'Interpreter', 'latex');
legend(gca,'off');
legend('Location', legend_location, 'NumColumns', 1, 'Interpreter', 'latex');
box on;






