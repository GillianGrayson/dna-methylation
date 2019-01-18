function specific(config_base, config_advanced)

if strcmp(config_base.gender, 'any')
    [config_base.names, config_base.data] = get_data(config_base);
    save_data(config_base, config_advanced);
else
    [config_base.names, config_base.data_1, config_base.data_2] = get_specific_data(config_base);
    [config_base.metrics_1, config_base.metrics_2] = get_specific_metrics(config_base);
    [config_base.metrics_diff, config_base.metrics_diff_labels] = get_specific_polygons(config_base, config_advanced);
    
    num_names = size(config_base.names, 1)
    
    config_base.order = get_specific_order(config_base);
    
    save_specific(config_base, config_advanced);
end

end