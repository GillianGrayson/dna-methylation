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

fn =  sprintf('%s/markers/%s_results.xlsx', path, markers_type);
res_tbl = readtable(fn, 'ReadRowNames', true);

metrics = res_tbl.Properties.VariableNames';

for m_id = 1 : size(metrics, 1)
    m = string(metrics(m_id));
    
    if contains(m, 'C_')
        color = colors{1};
    elseif contains(m, 'T_')
        color = colors{2};
    else
        color = 'red';
    end
    
    if contains(m, 'p_value')
        res_tbl = sortrows(res_tbl, m, 'descend');
        values = -log10(res_tbl.(m));
        if strcmp(m, 'kw_p_value')
            xlab = '$-\log_{10}($Kruskal-Wallis p-value$)$';
        else
            spl = split(m, '_');
            group = spl(1);
            target = spl(2);
            xlab = sprintf('$-log_{10}($%s p-value for %s$)$', target, group);
        end
    else
        res_tbl = sortrows(res_tbl, m, 'ascend');
        values = res_tbl.(m);
        
        spl = split(m, '_');
        group = spl(1);
        target = spl(2);
        xlab = sprintf('%s-Association $R^2$ for %s', target, group);
    end
    names = res_tbl.Properties.RowNames;
    
    fig = figure;
    propertyeditor('on');

    barh(values, 'FaceColor', color);
    yticks(linspace(1, size(values, 1), size(values, 1)))
    ylim([0.5, size(values, 1) + 0.5])
    set(gca, 'yTickLabel', names);
    ax = gca;
    if size(values, 1) < 10
        ax.YAxis.FontSize = 30;
    else
    	ax.YAxis.FontSize = 4;
    end
    set(gca, 'TickLabelInterpreter', 'none')
    xlabel(xlab, 'Interpreter', 'latex');
    ax.XAxis.FontSize = 30;
    grid on;

    fn_fig = sprintf('%s/%s', figures_path,  m);
    oqs_save_fig(fig, fn_fig)
    saveas(gcf, sprintf('%s.png', fn_fig));
    
    close all;
end

