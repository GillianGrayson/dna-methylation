clear all;

part = 'wo_noIntensity_detP_H17+_negDNAmPhenoAge';

group_feature = 'Group';
groups = {'Control', 'Disease'}';
colors = {[0 1 0], [1 0 1]}';

opacity = 0.65;
fontSizeX = 20;
fontSizeY = 10;

path = 'E:/YandexDisk/Work/pydnameth/unn_epic';
figures_path = sprintf('E:/YandexDisk/Work/pydnameth/unn_epic/figures/features/single_association/part(%s)', part);
if ~exist(figures_path, 'dir')
    mkdir(figures_path)
end

fn =  sprintf('%s/all_data/result/single_association.xlsx', path);
res_tbl = readtable(fn, 'ReadRowNames', true);

metrics = res_tbl.Properties.VariableNames';

for m_id = 1 : size(metrics, 1)
    m = string(metrics(m_id));
    
    if contains(m, '_C')
        color = colors{1};
    elseif contains(m, '_T')
        color = colors{2};
    else
        color = 'red';
    end
    
    if contains(m, 'p_value')
        res_tbl = sortrows(res_tbl, m, 'descend');
        values = -log10(res_tbl.(m));
        if strcmp(m, 'kw_p_value')
            xlab = '$-\log_{10}($Kruskal-Wallis p-value$)$';
        elseif strcmp(m, 'pb_p_value')
            xlab = '$-\log_{10}($Point-Biserial p-value$)$';
        else
            spl = split(m, '_');
            group = spl(4);
            target = spl(1);
            xlab = sprintf('$-log_{10}($%s p-value for %s$)$', target, group);
        end
    elseif contains(m, 'R2')
        res_tbl = sortrows(res_tbl, m, 'ascend');
        values = res_tbl.(m);
        spl = split(m, '_');
        group = spl(3);
        target = spl(1);
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
    ax.YAxis.FontSize = fontSizeY;
    set(gca, 'TickLabelInterpreter', 'none')
    xlabel(xlab, 'Interpreter', 'latex');
    ax.XAxis.FontSize = fontSizeX;
    grid on;

    fn_fig = sprintf('%s/%s', figures_path,  m);
    oqs_save_fig(fig, fn_fig)
    saveas(gcf, sprintf('%s.png', fn_fig));
    
    close all;
end

