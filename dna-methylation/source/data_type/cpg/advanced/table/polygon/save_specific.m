function save_specific(config_base, config_advanced)

name = config_advanced.name;
path = sprintf('%s/%s', ...
    config_advanced.up, ...
    get_result_path(config_advanced));
mkdir(path)
fn = sprintf('%s/%s.xlsx', ...
    path, ...
    name);

order = config_base.order;
names = config_base.names;
metrics_diff = config_base.metrics_diff;
metrics_diff_labels = config_base.metrics_diff_labels;

d = vertcat("names", string(names(order)));
for metrics_id = 1:size(metrics_diff, 2)
    d = horzcat(d, vertcat(metrics_diff_labels(metrics_id), string(metrics_diff(order, metrics_id))));
end

xlswrite(fn, d);

end