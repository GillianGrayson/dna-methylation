clear all;

norm = 'fun';
part = 'wo_noIntensity_detP';
target = 'DNAmAgeHannum';

groups = {'C', 'T'}';
colors = {[0 1 0], [1 0 1]}';
%colors = distinguishable_colors(size(groups, 1));

opacity = 0.65;

path = 'E:/YandexDisk/Work/pydnameth/unn_epic/horvath';
figures_path = sprintf('E:/YandexDisk/Work/pydnameth/unn_epic/figures/horvath/norm(%s)_part(%s)', norm, part);
if ~exist(figures_path, 'dir')
    mkdir(figures_path)
end
fn = sprintf('%s/data/betas_horvath_calculator_norm_%s_part_%s.output.csv', path, norm, part);
opts = detectImportOptions(fn);
opts = setvartype(opts, {'Sample_Group'}, 'string');
obs = readtable(fn, opts);

status = obs.Sample_Group;
age = obs.Age;
age_dnam = obs.(target);

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
    
    for id = 1 : size(age, 1)
        if status{id}(1) == groups{g_id}
            xs = vertcat(xs, age(id));
            ys = vertcat(ys, age_dnam(id));
        end
    end
    
    xs_all{g_id} = xs;
    ys_all{g_id} = ys;
    
    figure(fig1);
    hold all;
    color = colors{g_id};
    h = scatter(xs, ys, 250, 'o', 'LineWidth',  1, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', color, 'MarkerEdgeAlpha', opacity, 'MarkerFaceAlpha', opacity);
    legend(h, groups{g_id})
    
    if (groups{g_id} == 'C') || ((groups{g_id} == 'T') && (size(groups, 1) == 1))
        T = table(xs, ys, 'VariableNames', {'Age', target});
        lm = fitlm(T, sprintf('%s~Age', target));
        coeffs = lm.Coefficients;
        x_fit = [0; 100];
        y_fit = coeffs{'(Intercept)','Estimate'} + x_fit * coeffs{'Age','Estimate'};
        h = plot(x_fit, y_fit, 'LineWidth', 2, 'Color', color);
        h.Annotation.LegendInformation.IconDisplayStyle = 'off';
    end
end

for g_id = 1:size(groups, 1)
    xs = xs_all{g_id};
    ys = ys_all{g_id};
    
    diffs = zeros(size(xs, 1), 1);
    for p_id = 1:size(xs, 1)
        y_fit = coeffs{'(Intercept)','Estimate'} + xs(p_id) * coeffs{'Age','Estimate'};
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
        fn_fig = sprintf('%s/%s_AccelerationDiff_(%s)', figures_path, target, groups{g_id});
        oqs_save_fig(gcf, fn_fig)
    end 
end

figure(fig1);
hold all;
set(gca, 'FontSize', 40);
xlabel('Age', 'Interpreter', 'latex');
set(gca, 'FontSize', 40);
ylabel(target, 'Interpreter', 'latex');
h = plot([0 100], [0 100], 'k');
h.Annotation.LegendInformation.IconDisplayStyle = 'off';
legend(gca,'off');
legend('Location','Southeast','NumColumns',1)
box on;
fn_fig = sprintf('%s/Age_%s', figures_path, target);
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
    ylabel('AccelerationDiff')
    str = sprintf('Kruskal-Wallis p-value: %0.2e', p);
    tb = annotation('textbox', dim, 'String', str, 'verticalalignment', 'Bottom', 'FitBoxToText', 'on', 'FontSize', 24);
    hold all;
    
    for g_id = 1:size(groups, 1)
        h = scatter(g_id * ones(size(diffs_all{g_id}, 1), 1).*(1+(rand(size(diffs_all{g_id}))-0.5)/10), diffs_all{g_id}, 100, 'o', 'LineWidth',  1, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', colors{g_id}, 'MarkerEdgeAlpha', opacity, 'MarkerFaceAlpha', opacity);
        h.Annotation.LegendInformation.IconDisplayStyle = 'off';
    end
    
    box on;
    fn_fig = sprintf('%s/%s_AccelerationDiff_all', figures_path, target);
    oqs_save_fig(gcf, fn_fig)
    saveas(gcf, sprintf('%s.png', fn_fig));
end
