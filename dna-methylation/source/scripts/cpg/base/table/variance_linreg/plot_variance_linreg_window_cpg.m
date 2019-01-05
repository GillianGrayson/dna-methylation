function plot_variance_linreg_window_cpg(config, cpg)

fn = sprintf('%s/%s/%s.xlsx', ...
    config.up, ...
    get_result_path(config), ...
    config.name);

top_data = importdata(fn);

cpgs = string(top_data.textdata);

intercepts = top_data.data(:, 2);
slopes = top_data.data(:, 3);

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

ages_set = unique(ages_passed);
x_data = size(ages_set - 2 * config.window, 1);
y_data = size(ages_set - 2 * config.window, 1);

for age_id = (1+config.window):(size(ages_set, 1)-config.window)
    curr_x = ages_set(age_id);
    curr_y = 0;
    window_count = 0;
    for id = 1:size(indexes, 1)
        if ismember(ages_passed(id), ages_set(age_id - config.window : age_id + config.window))
            curr_y = curr_y + diffs_data(id);
            window_count = window_count + 1;
        end
    end
    curr_y = curr_y / window_count;
    x_data(age_id - config.window) = curr_x;
    y_data(age_id - config.window) = curr_y;
end

plot_data.scatter_x = ages_passed;
plot_data.scatter_y = diffs_data;
plot_data.line_x = x_data;
plot_data.line_y = y_data;
plot_data.line_name = sprintf('%s: %s', cpg, config.gender);
plot_data.color = config.color;
plot_data.is_plot_regions = config.is_plot_regions;

plot_variance_linreg_window(plot_data)

end

