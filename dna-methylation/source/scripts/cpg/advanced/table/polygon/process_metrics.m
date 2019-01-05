function metrics = process_metrics(target_metrics, config)
metrics = target_metrics;
if strcmp(config.method, 'manova')
    metrics = -log10(target_metrics);
elseif strcmp(config.method, 'linreg')
    if config.metrics_rank == 2
        metrics = -log10(target_metrics);
    end
end
end
