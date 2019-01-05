function plot_target_hist(config)

indexes = get_attributes_indexes(config);
ages = get_ages(config);

ages_passed = zeros(size(indexes, 1), 1);
for id = 1:size(indexes, 1)
    index = indexes(id);
    ages_passed(id) = ages(index);
end

num_objects = size(ages_passed, 1)

edges = min(ages_passed) - 0.5 : 1 : max(ages_passed) + 0.5;

h = histogram(ages_passed, 'BinEdges', edges, 'FaceColor', config.color, 'EdgeAlpha', config.edge_alpha, 'DisplayName', sprintf('%s', config.gender));
title(sprintf('%s', config.data_base), 'Interpreter', 'latex');
set(gca, 'FontSize', 30);
xlabel('$age$', 'Interpreter', 'latex');
set(gca, 'FontSize', 30);
ylabel('$count$', 'Interpreter', 'latex');
hold all;

end