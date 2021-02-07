clear all;

part = 'wo_noIntensity_detP_subset';

x_var = 'Age';
xlims = [0; 250];
y_var = 'CKDAge';
ylims = [0; 250];

groups = {'C', 'T'}';
group_base = 'C';
colors = {[0 1 0], [1 0 1]}';

opacity = 0.65;

path = 'E:/YandexDisk/Work/pydnameth/unn_epic';
figures_path = sprintf('E:/YandexDisk/Work/pydnameth/unn_epic/figures/features/Versus_Linear_ByGroup/part(%s)', part);
if ~exist(figures_path, 'dir')
    mkdir(figures_path)
end
fn = sprintf('%s/all_data/part(%s).xlsx', path, part);
opts = detectImportOptions(fn);
opts = setvartype(opts, {'Sample_Group'}, 'string');
obs = readtable(fn, opts);

status = obs.Sample_Group;
x_values = obs.(x_var);
y_values = obs.(y_var);

fig1 = figure;
propertyeditor('on');
grid on;

xs_all = {};
ys_all = {};
diffs_all = {};
coeffs = table();

for g_id = 1:size(groups, 1)
    
    xs = [];
    ys = [];
    
    for id = 1 : size(x_values, 1)
        if status{id}(1) == groups{g_id}
            xs = vertcat(xs, x_values(id));
            ys = vertcat(ys, y_values(id));
        end
    end
    
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
    legend(h, sprintf('%s $(R^2=%0.2f)$', groups{g_id}, R2), 'Interpreter','latex');
    
    x_fit = [xlims(1); xlims(2)];
    y_fit = lm.Coefficients{'(Intercept)','Estimate'} + x_fit * lm.Coefficients{x_var,'Estimate'};
    h = plot(x_fit, y_fit, 'LineWidth', 2, 'Color', color);
    h.Annotation.LegendInformation.IconDisplayStyle = 'off';
    
    if (groups{g_id} == group_base)
        coeffs = lm.Coefficients;
    end
end

for g_id = 1:size(groups, 1)
    xs = xs_all{g_id};
    ys = ys_all{g_id};
    
    diffs = zeros(size(xs, 1), 1);
    for p_id = 1:size(xs, 1)
        y_fit = coeffs{'(Intercept)','Estimate'} + xs(p_id) * coeffs{x_var,'Estimate'};
        diffs(p_id) = ys(p_id) - y_fit;
    end

    diffs_all{g_id} = diffs;

    if size(groups, 1) == 1
        fig2 = figure;
        propertyeditor('on');
        b = boxplot(diffs,'Notch','on','Labels',{groups(g_id)}, 'Colors', 'k');
        set(gca, 'FontSize', 40);
        a = get(get(gca, 'children'), 'children');
        t = get(a,'tag');
        idx = strcmpi(t,'box');
        boxes = a(idx);
        set(a,'linewidth',3)
        idx = strcmpi(t,'Outliers');
        outliers = a(idx);
        set(outliers, 'visible', 'off')
        hold all;
        h = scatter(1. * ones(size(diffs, 1), 1).*(1+(rand(size(diffs))-0.5)/10), diffs, 100, 'o', 'LineWidth',  1, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', color, 'MarkerEdgeAlpha', opacity, 'MarkerFaceAlpha', opacity);
        h.Annotation.LegendInformation.IconDisplayStyle = 'off';
        ylabel('Acceleration Diff', 'Interpreter', 'latex');
        box on;
        grid on;
        fn_fig = sprintf('%s/x(%s)_y(%s)_AccelerationDiff_(%s)', figures_path, x_var, y_var, groups{g_id});
        oqs_save_fig(gcf, fn_fig)
    end 
end

figure(fig1);
hold all;
set(gca, 'FontSize', 40);
xlabel(x_var, 'Interpreter', 'latex');
set(gca, 'FontSize', 40);
ylabel(y_var, 'Interpreter', 'latex');
bissectrice_s = min(xlims(1), ylims(1));
bissectrice_f = max(xlims(2), ylims(2));
hold all;
h = plot([bissectrice_s bissectrice_f], [bissectrice_s bissectrice_f], 'k');
h.Annotation.LegendInformation.IconDisplayStyle = 'off';
legend(gca,'off');
legend('Location', 'Southeast', 'NumColumns', 1, 'Interpreter', 'latex');
box on;
xlim(xlims);
ylim(ylims);
fn_fig = sprintf('%s/x(%s)_y(%s)_scatter', figures_path, x_var, y_var);
oqs_save_fig(fig1, fn_fig)
saveas(fig1, sprintf('%s.png', fn_fig));

if size(groups, 1) > 1
    
    agediff  = [];
    mod_status = [];
    for g_id = 1:size(groups, 1)
        agediff = vertcat(agediff, diffs_all{g_id});
        tmp = strings(size(diffs_all{g_id}, 1), 1);
        tmp(:) = groups{g_id};
        mod_status = vertcat(mod_status, tmp);
    end
    
    p = kruskalwallis(agediff, mod_status, 'on');
    grid on;
    propertyeditor('on')
    set(gca, 'FontSize', 40);
    a = get(get(gca,'children'),'children');
    t = get(a,'tag');
    idx = strcmpi(t,'box');
    boxes = a(idx);
    set(a,'linewidth',3);
    idx = strcmpi(t,'Outliers');
    outliers = a(idx);
    set(outliers,'visible','off')
    dim = [.165 .13 .3 .3];
    ylabel(sprintf('AccelerationDiff'), 'Interpreter', 'latex')
    str = sprintf('Kruskal-Wallis p-value: %0.2e', p);
    tb = annotation('textbox', dim, 'String', str, 'verticalalignment', 'Bottom', 'FitBoxToText', 'on', 'FontSize', 24);
    title(y_var, 'FontSize', 30, 'FontWeight', 'normal', 'Interpreter', 'latex');
    hold all;
    
    for g_id = 1:size(groups, 1)
        h = scatter(g_id * ones(size(diffs_all{g_id}, 1), 1).*(1+(rand(size(diffs_all{g_id}))-0.5)/10), diffs_all{g_id}, 100, 'o', 'LineWidth',  1, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', colors{g_id}, 'MarkerEdgeAlpha', opacity, 'MarkerFaceAlpha', opacity);
        h.Annotation.LegendInformation.IconDisplayStyle = 'off';
    end
    
    box on;
    fn_fig = sprintf('%s/x(%s)_y(%s)_KW', figures_path, x_var, y_var);
    oqs_save_fig(gcf, fn_fig)
    saveas(gcf, sprintf('%s.png', fn_fig));
end
