function order = get_specific_order(config)
    [tmp, order] = sort(config.metrics_diff(:, config.metrics_diff_id), config.metrics_diff_direction);
end