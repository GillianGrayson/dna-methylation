function [metrics_1, metrics_2] = get_specific_metrics(config)

metrics_id = get_metrics_id(config);

metrics_1 = config.data_1(:, metrics_id);
metrics_1 = process_metrics(metrics_1, config);

metrics_2 = config.data_2(:, metrics_id);
metrics_2 = process_metrics(metrics_2, config);

end