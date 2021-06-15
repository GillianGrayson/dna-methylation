figures_path = sprintf('%s/figures/cpgs/dataType(%s)_part(%s)_config(%s)_norm(%s)', dataset_path, data_type, norm, config, part);
if ~exist(figures_path, 'dir')
    mkdir(figures_path)
end

continious = 'age';
xlims = [0; 100];

% Contour params ==========================================================
is_contour = 0;
num_bins = 8;
level = 1;
levels = [level level];
meshgrid_size = 50;
% =========================================================================

is_lin_fit = 0;

group_by = 'gender';
groups = {'F', 'M'}';
colors = {[1 0 0],[0 0 1]}';
opacity = 0.65;

keySet = {};
valueSet = {{}};
base_filter = true(height(obs), 1);
if size(keySet, 1) > 0
    fitering = containers.Map(keySet,valueSet);
    
    for k = keys(fitering)
        b = false(height(obs), 1);
        vals = fitering(k{1});
        column = obs.(k{1});
        for v_id = 1:size(vals, 2)
            if iscell(column)
                b = b | strcmp(column, vals{v_id});
            else
                b = b | (column == vals{v_id});
            end
        end
        base_filter = base_filter & b;
    end
end

cgs = ...
    { ...
    'cg27288829', ...
    }';

group_indeces = {};
for g_id = 1 : size(groups, 1)
    column = obs.(group_by);
    if iscell(column)
        group_indeces{g_id} = base_filter & strcmp(column, groups{g_id});
    else
        group_indeces{g_id} = base_filter & (column == groups{g_id});
    end
end

for cg_id = 1:size(cgs, 1)
    
    cg = cgs{cg_id};
    cg_data = betas{cg, :}';
    age_data = obs{:, continious}';
    
    min_x = min(age_data);
    max_x = max(age_data);
    shift_x = max_x - min_x;
    min_x = floor(min_x - 0.2 * shift_x);
    max_x = ceil(max_x + 0.2 * shift_x);
    
    min_y = min(cg_data);
    max_y = max(cg_data);
    shift_y = max_y - min_y;
    min_y = min_y - 0.2 * shift_y;
    max_y = max_y + 0.2 * shift_y;
    
    centers = {linspace(min_x, max_x, num_bins)', linspace(min_y, max_y, num_bins)'};
    
    if strcmp(chip, '850k')
        gene_raw = string(ann{cg, 'UCSC_RefGene_Name'});
    else
        gene_raw = string(ann{cg, 'UCSC_REFGENE_NAME'});
    end
    genes_list = unique(split(gene_raw, ';'));
    genes = strjoin(genes_list,';');

    fig = figure;
    propertyeditor('on');
    for g_id = 1 : size(groups, 1)
        
        ys = cg_data(group_indeces{g_id});
        xs = obs{group_indeces{g_id}, continious};
        color = colors{g_id};
        h = scatter(xs, ys, 100, 'o', 'LineWidth',  1, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', color, 'MarkerEdgeAlpha', opacity, 'MarkerFaceAlpha', opacity);
        leg = legend(h, sprintf('%s:%s', replace(group_by, {':', '*', '_'}, ' '), groups{g_id}));
        hold all;
        
        if is_contour == 1
            centers = {linspace(min_x, max_x, num_bins)', linspace(min_y, max_y, num_bins)'};          
            [hist_values, hist_axes] = hist3([xs, ys], 'Ctrs', centers);
            [xnew, ynew] = meshgrid(linspace(min_x, max_x, meshgrid_size)', linspace(min_y, max_y, meshgrid_size)');
            znew = interp2(hist_axes{1}, hist_axes{2}, hist_values', xnew, ynew, 'spline');
            [c, M] = contour(xnew, ynew, znew, levels, 'EdgeColor', color, 'LineWidth', 1);
            M.Annotation.LegendInformation.IconDisplayStyle = 'off';
            num_points = size(c, 2);
            start_point = 1;
            last_point = 2;
            while last_point < num_points
                curr_np = c(2, start_point);
                xc = c(1,start_point + 1 : start_point + curr_np);
                yc = c(2,start_point + 1 : start_point + curr_np);
                pgon = polyshape(xc, yc);
                hold all;
                pg = plot(pgon, 'FaceColor', color, 'FaceAlpha', 0.10);
                pg.Annotation.LegendInformation.IconDisplayStyle = 'off';
                start_point = start_point + curr_np + 1;
                last_point = start_point + 2;
            end
        end
        
        if is_lin_fit == 1
            T = table(xs, ys, 'VariableNames', {continious, 'cg'});
            lm = fitlm(T,sprintf('cg~%s', continious));
            coeffs = lm.Coefficients;
            x_fit = linspace(min_x, max_x, 2);
            y_fit = coeffs{'(Intercept)','Estimate'} + x_fit * coeffs{continious,'Estimate'};
            h = plot(x_fit, y_fit, 'LineWidth', 1, 'Color', color);
            h.Annotation.LegendInformation.IconDisplayStyle = 'off';   
        end
        
    end
    set(gca, 'FontSize', 40);
    xlabel(continious, 'Interpreter', 'latex');
    set(gca, 'FontSize', 40);
    ylabel('Methylation Level', 'Interpreter', 'latex');
    grid on;
    box on;
    legend(gca,'off');
    legend('Location','Northwest','NumColumns',1)
    legend('FontSize', 24);
    title(sprintf('%s(%s)', cg, genes), 'FontSize', 24, 'FontWeight', 'normal');
    axis auto;
    xlim([xlims(1), xlims(2)])
    
    fn_fig = sprintf('%s/%d_%s(%s)_linFit(%d)_contour(%d_%d_%d)', figures_path, cg_id, cg, genes, is_lin_fit, is_contour, num_bins, level);
    oqs_save_fig(fig, fn_fig)
    saveas(gcf, sprintf('%s.png', fn_fig));
    
end