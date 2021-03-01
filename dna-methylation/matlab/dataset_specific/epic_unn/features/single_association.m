clear all;

part = 'wo_noIntensity_detP_H17+_negDNAmPhenoAge_missGDF15';

feature_type = 'cytokines';

group_feature = 'Group';
groups = {'Control', 'Disease'}';
colors = {[0 1 0], [1 0 1]}';

opacity = 0.65;
fontSizeX = 20;
fontSizeY = 24;

path = 'E:/YandexDisk/Work/pydnameth/unn_epic';
figures_path = sprintf('E:/YandexDisk/Work/pydnameth/unn_epic/figures/features/single_association/part(%s)', part);
if ~exist(figures_path, 'dir')
    mkdir(figures_path)
end

fn =  sprintf('%s/all_data/result/part(%s)/%s.xlsx', path, part, feature_type);
res_tbl = readtable(fn, 'ReadRowNames', true);

metrics = res_tbl.Properties.VariableNames';

for m_id = 1 : size(metrics, 1)
    m = string(metrics(m_id));
    
    spl = split(m, '_');
    
    if strcmp(spl(end), 'C')
        color = colors{1};
    elseif strcmp(spl(end), 'T')
        color = colors{2};
        continue;
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
            tmp = spl(end);
            if strcmp(tmp, 'C')
                group = 'Control';
            elseif strcmp(tmp, 'T')
                group = 'Disease';
            end
            if contains(m, 'CKD')
                target = strcat('Immuno', spl(2));
            else
                target = spl(1);
            end
            xlab = sprintf('$-log_{10}($%s p-value for %s$)$', target, group);
        end
    elseif contains(m, 'R2')
        continue;
        res_tbl = sortrows(res_tbl, m, 'ascend');
        values = res_tbl.(m);
        spl = split(m, '_');
        group = spl(3);
        target = spl(1);
        target = replace(target, 'CKD', 'Immuno');
        xlab = sprintf('%s-Association $R^2$ for %s', target, group);
    end
    names = res_tbl.Properties.RowNames;
    
    fig = figure;
    propertyeditor('on');

    barh(values, 'FaceColor', color);
    yticks(linspace(1, size(values, 1), size(values, 1)))
    ylim([0.5, size(values, 1) + 0.5])
    hold all;
    if contains(m, 'p_value')
        h = plot([-log10(0.05), -log10(0.05)], [0, size(values, 1) + 1], ':', 'Color', 'black', 'LineWidth', 4);
        h.Annotation.LegendInformation.IconDisplayStyle = 'off';
    end
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

