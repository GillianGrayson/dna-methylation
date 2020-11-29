clear all;

markers_type = 'MULTIPLEX_20_11_2020_xtd';

norm = 'fun';
part = 'wo_noIntensity_detP';
targets = {'Age', 'DNAmAge', 'DNAmAgeHannum', 'DNAmPhenoAge', 'DNAmGrimAge'};

groups = {'C', 'T'}';
colors = {[0 1 0], [1 0 1]}';

opacity = 0.65;

path = 'E:/YandexDisk/Work/pydnameth/unn_epic';
figures_path = sprintf('E:/YandexDisk/Work/pydnameth/unn_epic/figures/markers/norm(%s)_part(%s)/%s', norm, part, markers_type);
if ~exist(figures_path, 'dir')
    mkdir(figures_path)
end

fn = sprintf('%s/horvath/data/betas_horvath_calculator_norm_%s_part_%s.output.csv', path, norm, part);
opts = detectImportOptions(fn);
opts = setvartype(opts, {'Sample_Group'}, 'string');
obs = readtable(fn, opts);
obs.Properties.RowNames = obs.('ID');


fn = sprintf('%s/markers/%s.xlsx', path, markers_type);
mrkrs = readtable(fn);
mrkrs.Properties.RowNames = mrkrs.('ID');

tbl_full = innerjoin(obs, mrkrs, 'Keys','ID');
tbl_full = sortrows(tbl_full, 'Sample_Group');

obs(:, 'ID') = [];
mrkrs(:, 'ID') = [];
vars = mrkrs.Properties.VariableNames';
num_vars = size(vars, 1);

res_tbl = table;
res_tbl.('markers') = vars;
res_tbl.('kw_p_value') = zeros(num_vars, 1);
for a = targets
    res_tbl.(sprintf('C_%s_R2', string(a))) = zeros(num_vars, 1);
    res_tbl.(sprintf('C_%s_p_value', string(a))) = zeros(num_vars, 1);
    res_tbl.(sprintf('T_%s_R2', string(a))) = zeros(num_vars, 1);
    res_tbl.(sprintf('T_%s_p_value', string(a))) = zeros(num_vars, 1);
end
res_tbl.Properties.RowNames = res_tbl.('markers');
res_tbl(:, 'markers') = [];

tbl_control = tbl_full(tbl_full.('Sample_Group') == 'C', :);
tbl_treatment = tbl_full(tbl_full.('Sample_Group') == 'T', :);

for v_id = 1 : num_vars
    var = vars{v_id};
    
    figures_path_local = sprintf('%s/%s', figures_path, var);
    if ~exist(figures_path_local, 'dir')
        mkdir(figures_path_local)
    end
    
    test_data = {};
    for g_id = 1:size(groups, 1)
        group = groups{g_id};
        test_data{g_id} = tbl_full{tbl_full.('Sample_Group') == group, var};
    end
    
    p = kruskalwallis(tbl_full.(var), tbl_full.('Sample_Group'), 'on');
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
    ylabel(var, 'Interpreter', 'none')
    xlabel('Group', 'Interpreter', 'none')
    str = sprintf('Kruskal-Wallis p-value: %0.2e', p);
    title(str, 'FontSize', 20, 'FontWeight', 'normal');
    hold all;
    for g_id = 1:size(groups, 1)
        h = scatter(g_id * ones(size(test_data{g_id}, 1), 1).*(1+(rand(size(test_data{g_id}))-0.5)/10), test_data{g_id}, 100, 'o', 'LineWidth',  1, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', colors{g_id}, 'MarkerEdgeAlpha', opacity, 'MarkerFaceAlpha', opacity);
        h.Annotation.LegendInformation.IconDisplayStyle = 'off';
    end
    box on;
    fn_fig = sprintf('%s/box', figures_path_local);
    oqs_save_fig(gcf, fn_fig)
    saveas(gcf, sprintf('%s.png', fn_fig));
    res_tbl{var, 'kw_p_value'} = p;
    
    for a = targets
        
        a = string(a);
        
        fig = figure;
        propertyeditor('on');
        grid on;
        
        h = scatter(tbl_control.(a), tbl_control.(var), 250, 'o', 'LineWidth',  1, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', colors{1}, 'MarkerEdgeAlpha', opacity, 'MarkerFaceAlpha', opacity);
        legend(h, 'C')
        hold all;
        h = scatter(tbl_treatment.(a), tbl_treatment.(var), 250, 'o', 'LineWidth',  1, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', colors{2}, 'MarkerEdgeAlpha', opacity, 'MarkerFaceAlpha', opacity);
        legend(h, 'T')
        hold all;
        
        formula = sprintf('%s~%s', var, a);
        lm = fitlm(tbl_control, formula);
        coeffs = lm.Coefficients;
        x_fit = [0; 100];
        y_fit = coeffs{'(Intercept)','Estimate'} + x_fit * coeffs{a,'Estimate'};
        h = plot(x_fit, y_fit, 'LineWidth', 2, 'Color', colors{1});
        h.Annotation.LegendInformation.IconDisplayStyle = 'off';
        res_tbl{var, sprintf('C_%s_R2', a)} = lm.Rsquared.Ordinary;
        res_tbl{var, sprintf('C_%s_p_value', a)} = coeffs{a,'pValue'};
        
        formula = sprintf('%s~%s', var, a);
        lm = fitlm(tbl_treatment, formula);
        coeffs = lm.Coefficients;
        x_fit = [0; 100];
        y_fit = coeffs{'(Intercept)','Estimate'} + x_fit * coeffs{a,'Estimate'};
        h = plot(x_fit, y_fit, 'LineWidth', 2, 'Color', colors{2});
        h.Annotation.LegendInformation.IconDisplayStyle = 'off';
        res_tbl{var, sprintf('T_%s_R2', a)} = lm.Rsquared.Ordinary;
        res_tbl{var, sprintf('T_%s_p_value', a)} = coeffs{a,'pValue'};
        
        hold all;
        set(gca, 'FontSize', 40);
        xlabel(a, 'Interpreter', 'latex');
        set(gca, 'FontSize', 40);
        ylabel(var, 'Interpreter', 'none');
        legend(gca,'off');
        legend('Location','Southeast','NumColumns',1)
        box on;
        title(sprintf('R^2(C):%0.4f    R^2(T):%0.4f', res_tbl{var, sprintf('C_%s_R2', a)}, res_tbl{var, sprintf('T_%s_R2', a)}), 'FontSize', 20, 'FontWeight', 'normal');
        fn_fig = sprintf('%s/%s', figures_path_local, a);
        oqs_save_fig(fig, fn_fig)
        saveas(fig, sprintf('%s.png', fn_fig));
        
        close all;
    end
end

fn_save =  sprintf('%s/markers/%s_results.xlsx', path, markers_type);
writetable(res_tbl, fn_save, 'Sheet', 1, 'WriteRowNames', true);