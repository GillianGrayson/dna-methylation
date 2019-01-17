function metrics_id = get_metrics_id(config)
metrics_id = 1;

if strcmp(config.method, 'linreg')
    metrics_id = 1;
        
elseif strcmp(config.method, 'manova')
    metrics_id = 1;
    
elseif strcmp(config.method, 'variance_linreg')
    metrics_id = 8;
    
elseif strcmp(config.method, 'moment')
    if config.metrics_rank == 1
        metrics_id = 1;
    elseif config.metrics_rank == 2
        metrics_id = 2;
    end    

end
end