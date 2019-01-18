function plot_variance_linreg_delta(config, cpg)

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
intercepts_std_var = top_data.data(:, 11);
slopes_std_var = top_data.data(:, 12);

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

slope = slopes(cpg_id);
intercept = intercepts(cpg_id);
diffs_data = size(indexes, 1);
for id = 1:size(indexes, 1)
    curr_x = ages_passed(id);
    curr_y = cpg_data_passed(id);
    pred_y = slope * curr_x + intercept;
    diffs_data(id) = abs(pred_y - curr_y);
end

sigma = 3;

slope_var = slopes_var(cpg_id);
intercept_var = intercepts_var(cpg_id);
intercept_std_var = intercepts_std_var(cpg_id);
slope_std_var = slopes_std_var(cpg_id);

x_lin = [min(ages), max(ages)];
y_lin = [slope_var * x_lin(1) + intercept_var, slope_var * x_lin(2) + intercept_var];

slope_minus_var = slope_var - sigma * slope_std_var;
intercept_minus_var = intercept_var - sigma * intercept_std_var;

slope_plus_var = slope_var + sigma * slope_std_var;
intercept_plus_var = intercept_var + sigma * intercept_std_var;

intercept_up_var = intercept_var + ((slope_plus_var * x_lin(2) + intercept_plus_var) - (slope_var * x_lin(2) + intercept_var));
slope_up_var = slope_var;

intercept_down_var = intercept_var + ((slope_minus_var * x_lin(2) + intercept_minus_var) - (slope_var * x_lin(2) + intercept_var));
slope_down_var = slope_var;

y_up_var = [slope_up_var * x_lin(1) + intercept_up_var, slope_up_var * x_lin(2) + intercept_up_var];
y_down_var = [slope_down_var * x_lin(1) + intercept_down_var, slope_down_var * x_lin(2) + intercept_down_var];

plot_data.scatter_x = ages_passed;
plot_data.scatter_y = diffs_data;
plot_data.line_x = x_lin;
plot_data.line_y = y_lin;
plot_data.line_y_down = y_down_var;
plot_data.line_y_up = y_up_var;
plot_data.line_name = sprintf('%s: %s', cpg, config.gender);
plot_data.color = config.color;
plot_data.is_plot_regions = config.is_plot_regions;

plot_variance_linreg(plot_data)

end