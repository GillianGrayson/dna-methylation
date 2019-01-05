function [metrics_diff, metrics_diff_labels] = get_specific_polygons(config_base, config_advanced)

if strcmp(config_base.method, 'linreg')
    
    sigma = str2double(config_advanced.params('sigma'));
    
    ages = get_ages(config_base);
    
    names = config_base.names;
    
    intercepts_1 = config_base.data_1(:, 2);
    slopes_1 = config_base.data_1(:, 3);
    intercepts_std_1 = config_base.data_1(:, 4);
    slopes_std_1 = config_base.data_1(:, 5);
    
    intercepts_2 = config_base.data_2(:, 2);
    slopes_2 = config_base.data_2(:, 3);
    intercepts_std_2 = config_base.data_2(:, 4);
    slopes_std_2 = config_base.data_2(:, 5);
    
    x = [min(ages), max(ages), max(ages), min(ages)];
    
    areas = zeros(size(names, 1), 1);
    areas_normed = zeros(size(names, 1), 1);
    variance_diff = zeros(size(names, 1), 1);
    slope_intersection = zeros(size(names, 1), 1);
    
    for id = 1 : size(names, 1)  
        intercept_minus_1 = intercepts_1(id) - sigma * intercepts_std_1(id);
        slope_minus_1 = slopes_1(id) - sigma * slopes_std_1(id);
        intercept_plus_1 = intercepts_1(id) + sigma * intercepts_std_1(id);
        slope_plus_1 = slopes_1(id) + sigma * slopes_std_1(id);
        
        intercept_up_1 = intercepts_1(id) + ((slope_plus_1 * x(2) + intercept_plus_1) - (slopes_1(id) * x(2) + intercepts_1(id)));
        intercept_down_1 = intercepts_1(id) + ((slope_minus_1 * x(2) + intercept_minus_1) - (slopes_1(id) * x(2) + intercepts_1(id)));
        
        y1 = [slopes_1(id) * x(1) + intercept_down_1, ...
            slopes_1(id) * x(2) + intercept_down_1, ...
            slopes_1(id) * x(3) + intercept_up_1, ...
            slopes_1(id) * x(4) + intercept_up_1];
        
        intercept_minus_2 = intercepts_2(id) - sigma * intercepts_std_2(id);
        slope_minus_2 = slopes_2(id) - sigma * slopes_std_2(id);
        intercept_plus_2 = intercepts_2(id) + sigma * intercepts_std_2(id);
        slope_plus_2 = slopes_2(id) + sigma * slopes_std_2(id);
        
        intercept_up_2 = intercepts_2(id) + ((slope_plus_2 * x(2) + intercept_plus_2) - (slopes_2(id) * x(2) + intercepts_2(id)));
        intercept_down_2 = intercepts_2(id) + ((slope_minus_2 * x(2) + intercept_minus_2) - (slopes_2(id) * x(2) + intercepts_2(id)));
        
        y2 = [slopes_2(id) * x(1) + intercept_down_2, ...
            slopes_2(id) * x(2) + intercept_down_2, ...
            slopes_2(id) * x(3) + intercept_up_2, ...
            slopes_2(id) * x(4) + intercept_up_2];
        
        pgon_1 = polyshape(x, y1);
        area_pgon_1 = polyarea(x, y1);
        pgon_2 = polyshape(x, y2);
        area_pgon_2 = polyarea(x, y2);
        
        pgon_intersect = intersect(pgon_1, pgon_2);
        
        areas(id) = polyarea(pgon_intersect.Vertices(:, 1), pgon_intersect.Vertices(:, 2));
        areas_normed(id) = areas(id) / (area_pgon_1 + area_pgon_2 - areas(id));
        
        variance_1 = y1(4) - y1(1);
        variance_2 = y2(4) - y2(1);
        variance_diff(id) = max(variance_1, variance_2) / min(variance_1, variance_2);
        
        pgon_slope_1_x = [slope_minus_1, slope_plus_1, slope_plus_1, slope_minus_1];
        pgon_slope_1_y = [0.0, 0.0, 1.0, 1.0];
        pgon_slope_1 = polyshape(pgon_slope_1_x, pgon_slope_1_y);
        
        pgon_slope_2_x = [slope_minus_2, slope_plus_2, slope_plus_2, slope_minus_2];
        pgon_slope_2_y = [0.0, 0.0, 1.0, 1.0];
        pgon_slope_2 = polyshape(pgon_slope_2_x, pgon_slope_2_y);
        
        pgon_slope_intersect = intersect(pgon_slope_1, pgon_slope_2);
        pgon_slope_union = union(pgon_slope_1, pgon_slope_2);
        
        area_intersection = polyarea(pgon_slope_intersect.Vertices(:, 1), pgon_slope_intersect.Vertices(:, 2));
        area_union = polyarea(pgon_slope_union.Vertices(:, 1), pgon_slope_union.Vertices(:, 2));
        
        if area_intersection < 1e-8
            slope_intersection(id) = 0.0;
        else
            slope_intersection(id) = area_intersection / area_union;
        end
        
        if mod(id, 1000) == 0
            id = id
        end
        
    end
    
    metrics_diff = horzcat(areas, areas_normed, variance_diff, slope_intersection);
    metrics_diff_labels = ["poly_area_abs", "poly_area_rel", "variance_ratio", "slope_interval_rel"];

elseif strcmp(config_base.method, 'variance_linreg')
    
    sigma = str2double(config_advanced.params('sigma'));
    
    ages = get_ages(config_base);
    
    names = config_base.names;
    
    intercepts_1 = config_base.data_1(:, 2);
    slopes_1 = config_base.data_1(:, 3);
    intercepts_std_1 = config_base.data_1(:, 4);
    slopes_std_1 = config_base.data_1(:, 5);
    
    intercepts_2 = config_base.data_2(:, 2);
    slopes_2 = config_base.data_2(:, 3);
    intercepts_std_2 = config_base.data_2(:, 4);
    slopes_std_2 = config_base.data_2(:, 5);
    
    intercepts_var_1 = config_base.data_1(:, 9);
    slopes_var_1 = config_base.data_1(:, 10);
    intercepts_std_var_1 = config_base.data_1(:, 11);
    slopes_std_var_1 = config_base.data_1(:, 12);
    
    intercepts_var_2 = config_base.data_2(:, 9);
    slopes_var_2 = config_base.data_2(:, 10);
    intercepts_std_var_2 = config_base.data_2(:, 11);
    slopes_std_var_2 = config_base.data_2(:, 12);
    
    x = [min(ages), max(ages), max(ages), min(ages)];
    
    areas = zeros(size(names, 1), 1);
    areas_normed = zeros(size(names, 1), 1);
    variance_diff = zeros(size(names, 1), 1);
    slope_intersection = zeros(size(names, 1), 1);
    
    areas_var = zeros(size(names, 1), 1);
    areas_normed_var = zeros(size(names, 1), 1);
    variance_diff_var = zeros(size(names, 1), 1);
    slope_intersection_var = zeros(size(names, 1), 1);
    
    for id = 1 : size(names, 1)  
        intercept_minus_1 = intercepts_1(id) - sigma * intercepts_std_1(id);
        slope_minus_1 = slopes_1(id) - sigma * slopes_std_1(id);
        intercept_plus_1 = intercepts_1(id) + sigma * intercepts_std_1(id);
        slope_plus_1 = slopes_1(id) + sigma * slopes_std_1(id);
        
        intercept_up_1 = intercepts_1(id) + ((slope_plus_1 * x(2) + intercept_plus_1) - (slopes_1(id) * x(2) + intercepts_1(id)));
        intercept_down_1 = intercepts_1(id) + ((slope_minus_1 * x(2) + intercept_minus_1) - (slopes_1(id) * x(2) + intercepts_1(id)));
        
        y1 = [slopes_1(id) * x(1) + intercept_down_1, ...
            slopes_1(id) * x(2) + intercept_down_1, ...
            slopes_1(id) * x(3) + intercept_up_1, ...
            slopes_1(id) * x(4) + intercept_up_1];
        
        intercept_minus_2 = intercepts_2(id) - sigma * intercepts_std_2(id);
        slope_minus_2 = slopes_2(id) - sigma * slopes_std_2(id);
        intercept_plus_2 = intercepts_2(id) + sigma * intercepts_std_2(id);
        slope_plus_2 = slopes_2(id) + sigma * slopes_std_2(id);
        
        intercept_up_2 = intercepts_2(id) + ((slope_plus_2 * x(2) + intercept_plus_2) - (slopes_2(id) * x(2) + intercepts_2(id)));
        intercept_down_2 = intercepts_2(id) + ((slope_minus_2 * x(2) + intercept_minus_2) - (slopes_2(id) * x(2) + intercepts_2(id)));
        
        y2 = [slopes_2(id) * x(1) + intercept_down_2, ...
            slopes_2(id) * x(2) + intercept_down_2, ...
            slopes_2(id) * x(3) + intercept_up_2, ...
            slopes_2(id) * x(4) + intercept_up_2];
        
        pgon_1 = polyshape(x, y1);
        area_pgon_1 = polyarea(x, y1);
        pgon_2 = polyshape(x, y2);
        area_pgon_2 = polyarea(x, y2);
        
        pgon_intersect = intersect(pgon_1, pgon_2);
        
        areas(id) = polyarea(pgon_intersect.Vertices(:, 1), pgon_intersect.Vertices(:, 2));
        areas_normed(id) = areas(id) / (area_pgon_1 + area_pgon_2 - areas(id));
        
        variance_1 = y1(4) - y1(1);
        variance_2 = y2(4) - y2(1);
        variance_diff(id) = max(variance_1, variance_2) / min(variance_1, variance_2);
        
        pgon_slope_1_x = [slope_minus_1, slope_plus_1, slope_plus_1, slope_minus_1];
        pgon_slope_1_y = [0.0, 0.0, 1.0, 1.0];
        pgon_slope_1 = polyshape(pgon_slope_1_x, pgon_slope_1_y);
        
        pgon_slope_2_x = [slope_minus_2, slope_plus_2, slope_plus_2, slope_minus_2];
        pgon_slope_2_y = [0.0, 0.0, 1.0, 1.0];
        pgon_slope_2 = polyshape(pgon_slope_2_x, pgon_slope_2_y);
        
        pgon_slope_intersect = intersect(pgon_slope_1, pgon_slope_2);
        pgon_slope_union = union(pgon_slope_1, pgon_slope_2);
        
        area_intersection = polyarea(pgon_slope_intersect.Vertices(:, 1), pgon_slope_intersect.Vertices(:, 2));
        area_union = polyarea(pgon_slope_union.Vertices(:, 1), pgon_slope_union.Vertices(:, 2));
        
        if area_intersection < 1e-8
            slope_intersection(id) = 0.0;
        else
            slope_intersection(id) = area_intersection / area_union;
        end
        
        intercept_minus_var_1 = intercepts_var_1(id) - sigma * intercepts_std_var_1(id);
        slope_minus_var_1 = slopes_var_1(id) - sigma * slopes_std_var_1(id);
        intercept_plus_var_1 = intercepts_var_1(id) + sigma * intercepts_std_var_1(id);
        slope_plus_var_1 = slopes_var_1(id) + sigma * slopes_std_var_1(id);
        
        intercept_up_var_1 = intercepts_var_1(id) + ((slope_plus_var_1 * x(2) + intercept_plus_var_1) - (slopes_var_1(id) * x(2) + intercepts_var_1(id)));
        intercept_down_var_1 = intercepts_var_1(id) + ((slope_minus_var_1 * x(2) + intercept_minus_var_1) - (slopes_var_1(id) * x(2) + intercepts_var_1(id)));
        
        y1_var = [slopes_var_1(id) * x(1) + intercept_down_var_1, ...
            slopes_var_1(id) * x(2) + intercept_down_var_1, ...
            slopes_var_1(id) * x(3) + intercept_up_var_1, ...
            slopes_var_1(id) * x(4) + intercept_up_var_1];
        
        intercept_minus_var_2 = intercepts_var_2(id) - sigma * intercepts_std_var_2(id);
        slope_minus_var_2 = slopes_var_2(id) - sigma * slopes_std_var_2(id);
        intercept_plus_var_2 = intercepts_var_2(id) + sigma * intercepts_std_var_2(id);
        slope_plus_var_2 = slopes_var_2(id) + sigma * slopes_std_var_2(id);
        
        intercept_up_var_2 = intercepts_var_2(id) + ((slope_plus_var_2 * x(2) + intercept_plus_var_2) - (slopes_var_2(id) * x(2) + intercepts_var_2(id)));
        intercept_down_var_2 = intercepts_var_2(id) + ((slope_minus_var_2 * x(2) + intercept_minus_var_2) - (slopes_var_2(id) * x(2) + intercepts_var_2(id)));
        
        y2_var = [slopes_var_2(id) * x(1) + intercept_down_var_2, ...
            slopes_var_2(id) * x(2) + intercept_down_var_2, ...
            slopes_var_2(id) * x(3) + intercept_up_var_2, ...
            slopes_var_2(id) * x(4) + intercept_up_var_2];
        
        pgon_var_1 = polyshape(x, y1_var);
        area_pgon_var_1 = polyarea(x, y1_var);
        pgon_var_2 = polyshape(x, y2_var);
        area_pgon_var_2 = polyarea(x, y2_var);
        
        pgon_intersect_var = intersect(pgon_var_1, pgon_var_2);
        
        areas_var(id) = polyarea(pgon_intersect_var.Vertices(:, 1), pgon_intersect_var.Vertices(:, 2));
        areas_normed_var(id) = areas_var(id) / (area_pgon_var_1 + area_pgon_var_2 - areas_var(id));
        
        variance_var_1 = y1_var(4) - y1_var(1);
        variance_var_2 = y2_var(4) - y2_var(1);
        variance_diff_var(id) = max(variance_var_1, variance_var_2) / min(variance_var_1, variance_var_2);
        
        pgon_slope_var_1_x = [slope_minus_var_1, slope_plus_var_1, slope_plus_var_1, slope_minus_var_1];
        pgon_slope_var_1_y = [0.0, 0.0, 1.0, 1.0];
        pgon_slope_var_1 = polyshape(pgon_slope_var_1_x, pgon_slope_var_1_y);
        
        pgon_slope_var_2_x = [slope_minus_var_2, slope_plus_var_2, slope_plus_var_2, slope_minus_var_2];
        pgon_slope_var_2_y = [0.0, 0.0, 1.0, 1.0];
        pgon_slope_var_2 = polyshape(pgon_slope_var_2_x, pgon_slope_var_2_y);
        
        pgon_slope_intersect_var = intersect(pgon_slope_var_1, pgon_slope_var_2);
        pgon_slope_union_var = union(pgon_slope_var_1, pgon_slope_var_2);
        
        area_intersection_var = polyarea(pgon_slope_intersect_var.Vertices(:, 1), pgon_slope_intersect_var.Vertices(:, 2));
        area_union_var = polyarea(pgon_slope_union_var.Vertices(:, 1), pgon_slope_union_var.Vertices(:, 2));
        
        if area_intersection_var < 1e-8
            slope_intersection_var(id) = 0.0;
        else
            slope_intersection_var(id) = area_intersection_var / area_union_var;
        end
        
        if mod(id, 1000) == 0
            id = id
        end
        
    end
    
    metrics_diff = horzcat(areas, areas_normed, variance_diff, slope_intersection, areas_var, areas_normed_var, variance_diff_var, slope_intersection_var);
    metrics_diff_labels = ["poly_area_abs", "poly_area_rel", "variance_ratio", "slope_interval_rel", "poly_area_abs_var", "poly_area_rel_var", "variance_ratio_var", "slope_interval_rel_var"];    
    
else
    
    metrics_diff = zeros(size(config_base.names, 1), 1);
    for gene_id = 1:size(config_base.names, 1)
        metrics_diff(gene_id) = abs(config_base.metrics_1(gene_id) - config_base.metrics_2(gene_id));
    end
    metrics_diff_labels = ["metric"];

end