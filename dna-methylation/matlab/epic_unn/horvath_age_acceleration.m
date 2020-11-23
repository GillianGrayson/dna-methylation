clear all;

norm = 'fun';
part = 'wo_noIntensity_detP';
target = 'EEAA';

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
acceleration = obs.(target);



diffs_all = {};

for g_id = 1:size(groups, 1)
    
    accs = [];
    for id = 1 : size(age, 1)
        if status{id}(1) == groups{g_id}
            accs = vertcat(accs, acceleration(id));
        end
    end
    
    diffs_all{g_id} = accs;
end

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
    ylabel(target)
    str = sprintf('Kruskal-Wallis p-value: %0.2e', p);
    tb = annotation('textbox', dim, 'String', str, 'verticalalignment', 'Bottom', 'FitBoxToText', 'on', 'FontSize', 24);
    hold all;
    
    for g_id = 1:size(groups, 1)
        h = scatter(g_id * ones(size(diffs_all{g_id}, 1), 1).*(1+(rand(size(diffs_all{g_id}))-0.5)/10), diffs_all{g_id}, 100, 'o', 'LineWidth',  1, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', colors{g_id}, 'MarkerEdgeAlpha', opacity, 'MarkerFaceAlpha', opacity);
        h.Annotation.LegendInformation.IconDisplayStyle = 'off';
    end
    
    box on;
    fn_fig = sprintf('%s/%s_all', figures_path, target);
    oqs_save_fig(gcf, fn_fig)
    saveas(gcf, sprintf('%s.png', fn_fig));
end
