function save_data(config, save_config)

if strcmp(config.method, 'manova')
    target_str = '';
    types_str = '';
    for i = 1:length(config.attribute_target)
        target_str = sprintf('%s_%s', target_str, config.attribute_target{i});
    end
    target_str = strip(target_str,'left','_');
    for i = 1:length(config.attributes_types)
        types_str = sprintf('%s_%s', types_str, config.attributes_types{i});
    end
    types_str = strip(types_str,'left','_');
    suffix = sprintf('method(%s)_target(%s)_exog(%s)', ...
        config.method, ...
        target_str, ...
        types_str);
else
    suffix = sprintf('method(%s)', ...
        config.method);
end

path = sprintf('%s/%s', ...
    config.up, ...
    get_result_path(save_config));
mkdir(path)
fn = sprintf('%s/%s.xlsx', ...
    path, ...
    suffix);

names = config.names;
data = config.data;

d = vertcat('names', names);
for metrics_id = 1:size(data, 2)
    d = horzcat(d, vertcat(config.attribute_target{metrics_id}, num2cell(data(:,metrics_id))));
end

xlswrite(fn, d);

end