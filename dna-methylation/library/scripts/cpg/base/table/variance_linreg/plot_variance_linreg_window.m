function plot_variance_linreg_window(plot_data)

hold all;
h = scatter(plot_data.scatter_x, plot_data.scatter_y, 'MarkerEdgeColor', plot_data.color, 'SizeData', 100, 'MarkerFaceColor', 'w', 'MarkerFaceAlpha', 0.5);
set(get(get(h, 'Annotation'), 'LegendInformation'), 'IconDisplayStyle', 'off');

hold all;
h = plot(plot_data.line_x, plot_data.line_y, '-o', 'LineWidth', 3);
legend(h, plot_data.line_name);
set(h, 'Color', plot_data.color)
set(gca, 'FontSize', 30);
xlabel('age', 'Interpreter', 'latex');
set(gca, 'FontSize', 30);
ylabel('$|\delta|$', 'Interpreter', 'latex');
xlim([plot_data.line_x(1) - (plot_data.line_x(end) - plot_data.line_x(1)) * 0.1, plot_data.line_x(end) + (plot_data.line_x(end) - plot_data.line_x(1)) * 0.1])

box on;

end
