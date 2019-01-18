function [passed_names, metrics_labels, metrics_map] = advanced_condition(config_base, config_advanced)

name = config_advanced.name;
path = sprintf('%s/%s', ...
    config_advanced.up, ...
    get_result_path(config_advanced));
fn = sprintf('%s/%s.xlsx', ...
    path, ...
    name);

[num,txt,raw] = xlsread(fn);

if config_advanced.exp_id == 1
    
    if strcmp(config_base.method, 'linreg')
        
        names = raw(2:end, 1);
        area_intersection_rel = cell2mat(raw(2:end, 3));
        metrics_labels = [raw(1, 3)];
        passed_names = [];
        metrics_map = containers.Map();
        for id = 1:size(names)
            if area_intersection_rel(id) < 0.5
                passed_names = vertcat(passed_names, names(id));
                metrics_map(string(names(id))) = area_intersection_rel(id);
            end
        end
        
    end
    
elseif config_advanced.exp_id == 2
    
    if strcmp(config_base.method, 'linreg')
        
        names = raw(2:end, 1);
        slope_intersection = cell2mat(raw(2:end, 5));
        metrics_labels = [raw(1, 5)];
        passed_names = [];
        metrics_map = containers.Map();
        for id = 1:size(names)
            if slope_intersection(id) < 0.5
                passed_names = vertcat(passed_names, names(id));
                metrics_map(string(names(id))) = slope_intersection(id);
            end
        end
        
    end
    
elseif config_advanced.exp_id == 3
    
    if strcmp(config_base.method, 'linreg')
        
        names = raw(2:end, 1);
        area_intersection_rel = cell2mat(raw(2:end, 3));
        slope_intersection = cell2mat(raw(2:end, 5));
        metrics_labels = [raw(1, 3), raw(1, 5)];
        passed_names = [];
        metrics_map = containers.Map();
        for id = 1:size(names)
            if area_intersection_rel(id) < 0.5 && slope_intersection(id) < 0.5
                passed_names = vertcat(passed_names, names(id));
                metrics_map(string(names(id))) = [area_intersection_rel(id), slope_intersection(id)];
            end
        end
        
    end
    
elseif config_advanced.exp_id == 4
    
    if strcmp(config_base.method, 'linreg')
        
        names = raw(2:end, 1);
        area_intersection_rel = cell2mat(raw(2:end, 3));
        metrics_labels = [raw(1, 3)];
        passed_names = [];
        metrics_map = containers.Map();
        for id = 1:size(names)
            if area_intersection_rel(id) < 0.5
                passed_names = vertcat(passed_names, names(id));
                metrics_map(string(names(id))) = area_intersection_rel(id);
            end
        end
        
    end
    
elseif config_advanced.exp_id == 5
    
    if strcmp(config_base.method, 'linreg')
        
        names = raw(2:end, 1);
        area_intersection_rel = cell2mat(raw(2:end, 3));
        variance = cell2mat(raw(2:end, 4));
        metrics_labels = [raw(1, 3), raw(1, 4)];
        passed_names = strings(size(names, 1), 1);
        num_names = 1;
        metrics_map = containers.Map();
        for id = 1:size(names)
            if area_intersection_rel(id) < 0.5 && variance(id) > 3.0
                passed_names(num_names) = names(id);
                metrics_map(string(names(id))) = [area_intersection_rel(id), variance(id)];
                num_names = num_names + 1;
            end
        end
        num_names = num_names - 1;
        
        passed_names = passed_names(1:num_names, :);
        
    end
    
elseif config_advanced.exp_id == 6
    
    if strcmp(config_base.method, 'variance_linreg')
        names = raw(2:end, 1);
        slope_intersection = cell2mat(raw(2:end, 5));
        slope_intersection_var = cell2mat(raw(2:end, 9));
        metrics_labels = [raw(1, 5), raw(1, 9)];
        passed_names = strings(size(names, 1), 1);
        num_names = 1;
        metrics_map = containers.Map();
        for id = 1:size(names)
            passed_names(num_names) = names(id);
            metrics_map(string(names(id))) = [slope_intersection(id), slope_intersection_var(id)];
            num_names = num_names + 1;
        end
        num_names = num_names - 1;
        passed_names = passed_names(1:num_names, :);
    end
    
elseif config_advanced.exp_id == 7
    
    if strcmp(config_base.method, 'variance_linreg')
        names = raw(2:end, 1);
        variance = cell2mat(raw(2:end, 4));
        slope_intersection = cell2mat(raw(2:end, 5));
        slope_intersection_var = cell2mat(raw(2:end, 9));
        metrics_labels = [raw(1, 4), raw(1, 5), raw(1, 9)];
        passed_names = strings(size(names, 1), 1);
        num_names = 1;
        metrics_map = containers.Map();
        for id = 1:size(names)
            passed_names(num_names) = names(id);
            metrics_map(string(names(id))) = [variance(id), slope_intersection(id), slope_intersection_var(id)];
            num_names = num_names + 1;
        end
        num_names = num_names - 1;
        passed_names = passed_names(1:num_names, :);
    end

    
end

end

