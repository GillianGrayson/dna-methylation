clear all;

norm = 'none';
part = 'final_treatment';

groups = {'T'}';
colors = {[1 0 0]}';
%colors = distinguishable_colors(size(groups, 1));

opacity = 0.65;

path = 'E:/YandexDisk/Work/pydnameth/unn_epic/horvath';
figures_path = 'E:/YandexDisk/Work/pydnameth/unn_epic/figures/horvath';
fn = sprintf('%s/data/betas_horvath_calculator_norm_%s_part_%s.output.csv', path, norm, part);
opts = detectImportOptions(fn);
opts = setvartype(opts, {'Sample_Group'}, 'string');
obs = readtable(fn, opts);

status = obs.Sample_Group;
agediff = obs.AgeAccelerationDiff;
age = obs.Age;
age_dnam = obs.DNAmAge;

fig1 = figure;
propertyeditor('on');
grid on;

xs_all = {};
ys_all = {};
diffs_all = {};

for g_id = 1:size(groups, 1)
    xs = [];
    ys = [];
    diffs = [];
    
    for id = 1 : size(age, 1)

        if status{id}(1) == groups{g_id}
            xs = vertcat(xs, age(id));
            ys = vertcat(ys, age_dnam(id));
            diffs = vertcat(diffs, agediff(id));
        end
    end
    
    xs_all{g_id} = xs;
    ys_all{g_id} = ys;
    diffs_all{g_id} = diffs;
    
    figure(fig1);
    hold all;
    color = colors{g_id};
    h = scatter(xs, ys, 250, 'o', 'LineWidth',  1, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', color, 'MarkerEdgeAlpha', opacity, 'MarkerFaceAlpha', opacity);
    legend(h, groups{g_id})
    
    if size(groups, 1) == 1
        fig2 = figure;
        propertyeditor('on');
        b = boxplot(diffs,'Notch','on','Labels',{groups(g_id)}, 'Colors', 'k');
        set(gca, 'FontSize', 40);
        ylim([-20 30])
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
        ylabel('Age Acceleration Diff', 'Interpreter', 'latex');
        box on;
        grid on;
        fn_fig = sprintf('%s/AgeAccelerationDiff_(%s)_norm(%s)_part(%s)', figures_path, groups{g_id}, norm, part);
        oqs_save_fig(gcf, fn_fig)
    end 
end

figure(fig1);
hold all;
set(gca, 'FontSize', 40);
xlabel('Age', 'Interpreter', 'latex');
set(gca, 'FontSize', 40);
ylabel('DNAmAge', 'Interpreter', 'latex');
h = plot([0 100], [0 100], 'k');
h.Annotation.LegendInformation.IconDisplayStyle = 'off';
legend(gca,'off');
legend('Location','Southeast','NumColumns',1)
box on;
fn_fig = sprintf('%s/Age_DNAmAge_norm(%s)_part(%s)', figures_path, norm, part);
oqs_save_fig(fig1, fn_fig)

if size(groups, 1) > 1
    p = kruskalwallis(agediff, status, 'on');
    grid on;
    propertyeditor('on')
    set(gca, 'FontSize', 40);
    ylim([-20 30])
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
    
    for g_id = 1:size(groups, 1)
        h = scatter(g_id * ones(size(diffs_all{g_id}, 1), 1).*(1+(rand(size(diffs_all{g_id}))-0.5)/10), diffs_all{g_id}, 100, 'o', 'LineWidth',  1, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', colors{g_id}, 'MarkerEdgeAlpha', opacity, 'MarkerFaceAlpha', opacity);
        h.Annotation.LegendInformation.IconDisplayStyle = 'off';
    end
    
    box on;
    fn_fig = sprintf('%s/AgeAccelerationDiff_all_norm(%s)_part(%s)', figures_path, norm, part);
    oqs_save_fig(gcf, fn_fig)
end
