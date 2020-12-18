opacity = 0.65;
color = [1 0 0];
xlims = [0; 110];
ylims = [0; 110];
ylab = 'DNAmAge';

figures_path = sprintf('%s/figures/clock/dataType(%s)_norm(%s)_part(%s)', dataset_path, data_type, norm, part);
if ~exist(figures_path, 'dir')
    mkdir(figures_path)
end

load('epigenetic_clock.mat')

estimation = 'age';
cgs = importdata('epigenetic_clock.txt');

t = obs;
for cg_id = 1:size(cgs)
    cg = cgs{cg_id};
    cg_data = betas{cg, :}';
    t{:, cg} = cg_data;
end

yfit = predict(lm, t);
ae = abs(yfit - t.(estimation));
mae = mean(ae);

fig = figure;
h = scatter(t.(estimation), yfit, 250, 'o', 'LineWidth',  1, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', color, 'MarkerEdgeAlpha', opacity, 'MarkerFaceAlpha', opacity);
legend(h, sprintf('$MAE=%0.2f$', mae), 'Interpreter', 'latex');
hold all;
set(gca, 'FontSize', 40);
xlabel(estimation, 'Interpreter', 'latex');
set(gca, 'FontSize', 40);
ylabel(sprintf(ylab, estimation), 'Interpreter', 'latex');
bissectrice_s = min(xlims(1), ylims(1));
bissectrice_f = max(xlims(2), ylims(2));
hold all;
h = plot([bissectrice_s bissectrice_f], [bissectrice_s bissectrice_f], 'k');
h.Annotation.LegendInformation.IconDisplayStyle = 'off';
legend(gca,'off');
legend('Location', 'NorthWest', 'NumColumns', 1, 'Interpreter', 'latex');
legend('FontSize', 40);
xlim(xlims);
ylim(ylims);
title(dataset, 'FontSize', 40, 'FontWeight', 'normal', 'Interpreter', 'latex');
%title(sprintf('$R^2=%0.2f$%s$RMSE=%0.2f$%s$MAE=%0.2f$', R2, repmat('\ ',1,4), RMSE, repmat('\ ',1,4), mae), 'FontSize', 30, 'FontWeight', 'normal', 'Interpreter', 'latex');
propertyeditor on;
grid on;
box on;
fn_fig = sprintf('%s/%s', figures_path, estimation);
oqs_save_fig(fig, fn_fig)



