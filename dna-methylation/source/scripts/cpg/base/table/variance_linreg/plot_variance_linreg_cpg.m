function plot_variance_linreg_cpg(config, cpg)

fn = sprintf('%s/%s/%s.xlsx', ...
    config.up, ...
    get_result_path(config), ...
    config.name);

top_data = importdata(fn);

cpgs = string(top_data.textdata);

intercepts = top_data.data(:, 2);
slopes = top_data.data(:, 3);

intercepts_var = top_data.data(:, 9);
slopes_var = top_data.data(:, 10);

indexes = get_attributes_indexes(config);
ages = get_ages(config);

ages_passed = zeros(size(indexes, 1), 1);
for id = 1:size(indexes, 1)
    index = indexes(id);
    ages_passed(id) = ages(index);
end

fn = sprintf('%s/%s/cpg_beta.txt', config.up, config.data_base);
fid = fopen(fn);
data = textscan(fid, '%s %*[^\n]','HeaderLines',1);
frewind(fid)
all_cpgs = data{1};
idx = find(string(all_cpgs)==string(cpg))
target_row = textscan(fid,'%s',1,'delimiter','\n', 'headerlines', idx-1);
tline = strsplit(fgetl(fid), '\t');
curr_cpg = string(tline(1));
cpg_data = str2double(tline(2:end))';
fclose(fid);

cpg_data_passed = size(indexes, 1);
for id = 1:size(indexes, 1)
    cpg_data_passed(id) = cpg_data(indexes(id));
end

cpg_id = find(cpgs==cpg);

sigma = 3;

slope = slopes(cpg_id);
intercept = intercepts(cpg_id);
slope_var = slopes_var(cpg_id);
intercept_var = intercepts_var(cpg_id);

x_lin = [min(ages), max(ages)];
y_lin = [slope * x_lin(1) + intercept, slope * x_lin(2) + intercept];

y1_diff = slope_var * x_lin(1) + intercept_var;
y2_diff = slope_var * x_lin(2) + intercept_var;

y_up = [y_lin(1) + y1_diff, y_lin(2) + y2_diff];
y_down = [y_lin(1) - y1_diff, y_lin(2) - y2_diff];

plot_data.scatter_x = ages_passed;
plot_data.scatter_y = cpg_data_passed;
plot_data.line_x = x_lin;
plot_data.line_y = y_lin;
plot_data.line_y_down = y_down;
plot_data.line_y_up = y_up;
plot_data.line_name = sprintf('%s: %s', cpg, config.gender);
plot_data.color = config.color;
plot_data.is_plot_regions = config.is_plot_regions;

plot_linreg(plot_data)

end