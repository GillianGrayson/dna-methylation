clear all;

num_best = 20;

type = 'ssaa';
datasets = ["GSE87571", "GSE74193", "liver"];
save_path = sprintf('E:/YandexDisk/Work/pydnameth/methylation_and_proteomic/limma/proteome/%s/', type);

column_ids = [56; 38; 15];

for dataset = datasets
    
    path = sprintf('E:/YandexDisk/Work/pydnameth/methylation_and_proteomic/limma/proteome/%s/%s/intersection_full', type, dataset);
    fn = sprintf('%s/%s_Proteomic_expression.xlsx', path, dataset);
    gtex = readtable(fn);
    
    xs = gtex.Properties.VariableNames(column_ids)';
    ys = table2array(gtex(:, 'Description'));
    cs = zeros(size(ys, 1), size(xs, 1));
    xs_labels = {}';
    for id = 1:size(xs, 1)
        col = str2double(table2array(gtex(:, xs{id})));
        cs(:, id) = col;
        xs_labels{id} = strrep(xs{id},'_','');
    end
    
    min_val = min(cs(~isinf(cs))) - 1;
    cs(isinf(cs)) = min_val;
    
    fig = figure;
    h = imagesc(cs);
    xticks(linspace(1, size(xs_labels, 2), size(xs_labels, 2)));
    xticklabels(xs_labels);
    yticks([]);
    yticklabels([]);
    set(gca, 'FontSize',30);
    xlabel('Tissues', 'Interpreter', 'latex');
    ylabel('Genes', 'Interpreter', 'latex');
    colormap jet;
    h = colorbar;
    title(h, '$\log_{10}$GTEx', 'FontSize', 33, 'interpreter','latex');
    set(gca,'YDir','normal');
    hold all;
    propertyeditor('on')
    fn_fig = sprintf('%s/heatmap', path);
    oqs_save_fig(fig, fn_fig)
    close(fig);
    
    for id_1 = 1 : size(xs, 1)
        for id_2 = 1 : size(xs, 1)
            
            if (id_1 ~= id_2)
            
                x_label = xs_labels{id_1};
                y_label = xs_labels{id_2};
                xs_scatter = cs(:, id_1);
                ys_scatter = cs(:, id_2);
                diffs = abs(xs_scatter - ys_scatter);
                [diffs_sorted, order] = sort(diffs, 'descend');

                xs_scatter = xs_scatter(order);
                ys_scatter = ys_scatter(order);

                fig = figure;
                h = plot([min_val,min_val], [min(cs,[],'all') - 0.5, max(cs,[],'all') + 0.5], 'r');
                legend(h, sprintf('No %s expression', x_label));
                hold all;
                h = plot([min(cs,[],'all') - 0.5, max(cs,[],'all') + 0.5], [min_val,min_val], 'b');
                legend(h, sprintf('No %s expression', y_label));
                hold all;

                diff_lim = 0;
                if num_best < size(order, 1)

                    colors = distinguishable_colors(num_best);

                    for order_id = 1:num_best
                        gene_id = order(order_id);
                        color = colors(order_id, :);
                        h = plot(xs_scatter(order_id), ys_scatter(order_id), 'o', 'MarkerSize', 10, 'Color', color, 'MarkerFaceColor', color);
                        legend(h, ys{gene_id});
                        hold all;
                    end

                    diff_lim = diffs_sorted(num_best);

                    xs_scatter_reg = xs_scatter(num_best + 1:end);
                    ys_scatter_reg = ys_scatter(num_best + 1:end);
                    h = plot(xs_scatter_reg, ys_scatter_reg, 'o', 'MarkerSize', 3, 'Color', 'k', 'MarkerFaceColor', 'k');
                    h.Annotation.LegendInformation.IconDisplayStyle = 'off';

                    xs_lim = [min(cs,[],'all') - 0.5, max(cs,[],'all') + 0.5];
                    ys_lim = [min(cs,[],'all') - 0.5, max(cs,[],'all') + 0.5];
                    y_u = ys_lim + diff_lim;
                    y_d = ys_lim - diff_lim;
                    h = plot(xs_lim, y_u, 'k', 'LineStyle', ':');
                    h.Annotation.LegendInformation.IconDisplayStyle = 'off';
                    h = plot(xs_lim, y_d, 'k', 'LineStyle', ':');
                    h.Annotation.LegendInformation.IconDisplayStyle = 'off';
                else

                    colors = distinguishable_colors(size(order, 1));

                    for order_id = 1:size(order, 1)
                        gene_id = order(order_id);
                        color = colors(order_id, :);
                        h = plot(xs_scatter(order_id), ys_scatter(order_id), 'o', 'MarkerSize', 7, 'Color', color, 'MarkerFaceColor', color);
                        legend(h, ys{gene_id});
                        hold all;
                    end

                end

                h = plot([min(cs,[],'all') - 0.5, max(cs,[],'all') + 0.5], [min(cs,[],'all') - 0.5, max(cs,[],'all') + 0.5], 'k');
                h.Annotation.LegendInformation.IconDisplayStyle = 'off';

                set(gca, 'FontSize',30);
                tmp_str = '$\log_{10}$GTEx';
                xlabel(sprintf('%s in %s', tmp_str, x_label), 'Interpreter', 'latex');
                ylabel(sprintf('%s in %s', tmp_str, y_label), 'Interpreter', 'latex');
                xlim([min(cs,[],'all') - 0.5, max(cs,[],'all') + 0.5]);
                ylim([min(cs,[],'all') - 0.5, max(cs,[],'all') + 0.5]);

                propertyeditor('on')
                fn_fig = sprintf('%s/x(%s)_y(%s)', path, x_label, y_label);
                oqs_save_fig(fig, fn_fig)
                close(fig);
            end
        end
    end
end
