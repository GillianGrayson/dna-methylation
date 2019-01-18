function [passed_names, metrics_labels, metrics_map] = base_condition(config)
if strcmp(config.gender, 'vs')
    [names, data_1, data_2] = get_specific_data(config);
    
    if config.exp_id == 1
        
        if strcmp(config.method, 'linreg')
            
            sigma = 3;
            slopes_1 = data_1(:, 3);
            slopes_1_std = data_1(:, 5);
            slopes_2 = data_2(:, 3);
            slopes_2_std = data_2(:, 5);
            metrics_labels = ["slope_f", "slope_m"];
            passed_names = [];
            metrics_map = containers.Map();
            for id = 1:size(names)
                if slopes_1(id) < sigma * slopes_1_std(id) && slopes_2(id) < sigma * slopes_2_std(id)
                    passed_names = vertcat(passed_names, names(id));
                    metrics_map(string(names(id))) = [slopes_1(id), slopes_2(id)];
                end
            end
            
        elseif strcmp(config.method, 'anova')
            
            p_vals_1 = data_1(:, 1);
            p_vals_2 = data_2(:, 1);
            metrics_labels = ["pvals_f", "pvals_m"];
            passed_names = [];
            metrics_map = containers.Map();
            for id = 1:size(names)
                passed_names = vertcat(passed_names, names(id));
                metrics_map(string(names(id))) = [p_vals_1(id), p_vals_2(id)];
            end
            
        end
        
    elseif config.exp_id == 2
        
        if strcmp(config.method, 'linreg')
            
            slope_lim = 0.002;
            slopes_1 = data_1(:, 3);
            slopes_2 = data_2(:, 3);
            slope_pvals_1 = data_1(:, 7);
            slope_pvals_2 = data_2(:, 7);
            metrics_labels = ["slope_f", "slope_m", "slope_pvals_f", "slope_pvals_m"];
            passed_names = [];
            metrics_map = containers.Map();
            for id = 1:size(names)
                passed_names = vertcat(passed_names, names(id));
                metrics_map(string(names(id))) = [slopes_1(id), slopes_2(id), slope_pvals_1(id), slope_pvals_2(id)];
            end
            
        end
        
    elseif config.exp_id == 3
        
        if strcmp(config.method, 'linreg')
            
            slope_lim = 0.002;
            slopes_1 = data_1(:, 3);
            slopes_2 = data_2(:, 3);
            slope_pvals_1 = data_1(:, 7);
            slope_pvals_2 = data_2(:, 7);
            metrics_labels = ["slope_f", "slope_m", "slope_pvals_f", "slope_pvals_m"];
            passed_names = [];
            metrics_map = containers.Map();
            for id = 1:size(names)
                if abs(slopes_1(id)) > slope_lim || abs(slopes_2(id)) > slope_lim
                    passed_names = vertcat(passed_names, names(id));
                    metrics_map(string(names(id))) = [slopes_1(id), slopes_2(id), slope_pvals_1(id), slope_pvals_2(id)];
                end
            end
            
        end
        
    elseif config.exp_id == 4
        
        if strcmp(config.method, 'linreg')
            
            slope_lim = 0.002;
            slopes_1 = data_1(:, 3);
            slopes_2 = data_2(:, 3);
            slope_pvals_1 = data_1(:, 7);
            slope_pvals_2 = data_2(:, 7);
            metrics_labels = ["slope_f", "slope_m", "slope_pvals_f", "slope_pvals_m"];
            passed_names = [];
            metrics_map = containers.Map();
            for id = 1:size(names)
                if abs(slopes_1(id)) > slope_lim || abs(slopes_2(id)) > slope_lim
                    passed_names = vertcat(passed_names, names(id));
                    metrics_map(string(names(id))) = [slopes_1(id), slopes_2(id), slope_pvals_1(id), slope_pvals_2(id)];
                end
            end
            
        end
        
    elseif config.exp_id == 5
        
        if strcmp(config.method, 'linreg')
            
            sigma = 3;
            slopes_1 = data_1(:, 3);
            slopes_1_std = data_1(:, 5);
            slopes_2 = data_2(:, 3);
            slopes_2_std = data_2(:, 5);
            metrics_labels = ["slope_f", "slope_m"];
            passed_names = strings(size(names, 1), 1);
            num_names = 1;
            metrics_map = containers.Map();
            for id = 1:size(names)
                passed_names(num_names) = names(id);
                metrics_map(string(names(id))) = [slopes_1(id), slopes_2(id)];
                num_names = num_names + 1;
            end
            num_names = num_names - 1;
            
            passed_names = passed_names(1:num_names, :);
            
        end
        
    elseif config.exp_id == 6
        
        if strcmp(config.method, 'variance_linreg')
            
            slopes_1 = data_1(:, 3);
            slopes_2 = data_2(:, 3);
            slope_var_1 = data_1(:, 10);
            slope_var_2 = data_2(:, 10);
            metrics_labels = ["slope_f", "slope_m", "slope_var_f", "slope_var_m"];
            passed_names = strings(size(names, 1), 1);
            num_names = 1;
            metrics_map = containers.Map();
            for id = 1:size(names)
                passed_names(num_names) = names(id);
                metrics_map(string(names(id))) = [slopes_1(id), slopes_2(id), slope_var_1(id), slope_var_2(id)];
                num_names = num_names + 1;
            end
            num_names = num_names - 1;
            passed_names = passed_names(1:num_names, :);
        end
    elseif config.exp_id == 7
        
        if strcmp(config.method, 'variance_linreg')
            
            allowed_slopes_var_diff = 0.0005;
            slopes_1 = data_1(:, 3);
            slopes_2 = data_2(:, 3);
            slope_var_1 = data_1(:, 10);
            slope_var_2 = data_2(:, 10);
            metrics_labels = ["slope_f", "slope_m", "slope_var_f", "slope_var_m", "slope_var_diff"];
            passed_names = strings(size(names, 1), 1);
            num_names = 1;
            metrics_map = containers.Map();
            for id = 1:size(names)
                if abs(slope_var_1(id)) > allowed_slopes_var_diff || abs(slope_var_2(id)) > allowed_slopes_var_diff
                    slope_var_diff = abs(slope_var_1(id) - slope_var_2(id));
                    passed_names(num_names) = names(id);
                    metrics_map(string(names(id))) = [slopes_1(id), slopes_2(id), slope_var_1(id), slope_var_2(id), slope_var_diff];
                    num_names = num_names + 1;
                end
            end
            num_names = num_names - 1;
            passed_names = passed_names(1:num_names, :);
        end
    end
    
elseif strcmp(config.gender, 'any')
    [names, data] = get_neutral_data(config);
    
    if config.exp_id == 3
        
        if strcmp(config.method, 'linreg')
            
            slopes = data(:, 3);
            slope_pvals = data(:, 7);
            metrics_labels = ["slope", "slope_pvals"];
            passed_names = strings(size(names, 1), 1);
            num_names = 0;
            metrics_map = containers.Map();
            for id = 1:size(names)
                num_names = num_names + 1;
                passed_names(num_names) = names(id);
                metrics_map(string(names(id))) = [slopes(id), slope_pvals(id)];
            end
            passed_names = passed_names(1:num_names, :);
            
        end
        
    elseif config.exp_id == 4
        
        if strcmp(config.method, 'linreg')
            
            slopes = data(:, 3);
            slope_pvals = data(:, 7);
            metrics_labels = ["slope", "slope_pvals"];
            passed_names = strings(size(names, 1), 1);
            num_names = 0;
            metrics_map = containers.Map();
            for id = 1:size(names)
                num_names = num_names + 1;
                passed_names(num_names) = names(id);
                metrics_map(string(names(id))) = [slopes(id), slope_pvals(id)];
            end
            passed_names = passed_names(1:num_names, :);

        end
    
    elseif config.exp_id == 6
        if strcmp(config.method, 'variance_linreg')
            slopes = data(:, 3);
            slopes_var = data(:, 10);
            metrics_labels = ["slope_any", "slope_var_any"];
            passed_names = strings(size(names, 1), 1);
            num_names = 1;
            metrics_map = containers.Map();
            for id = 1:size(names)
                passed_names(num_names) = names(id);
                metrics_map(string(names(id))) = [slopes(id), slopes_var(id)];
                num_names = num_names + 1;
            end
            num_names = num_names - 1;
            passed_names = passed_names(1:num_names, :);
        end
    end
end