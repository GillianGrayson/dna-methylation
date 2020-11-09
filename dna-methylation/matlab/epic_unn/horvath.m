clear all;

norm = 'BMIQ';
part = 'final';

path = 'E:/YandexDisk/Work/pydnameth/unn_epic/horvath';
figures_path = 'E:/YandexDisk/Work/pydnameth/unn_epic/figures/horvath';
fn = sprintf('%s/data/betas_horvath_calculator_norm_%s_part_%s.output.csv', path, norm, part);
obs = readtable(fn);

status = obs.Sample_Group;
agediff = obs.AgeAccelerationDiff;
age = obs.Age;
age_dnam = obs.DNAmAge;

c_xs = [];
c_ys = [];
c_diff = [];

t_xs = [];
t_ys = [];
t_diff = [];

for id = 1 : size(age, 1)
    
    if status{id} == 'C'
        c_xs = vertcat(c_xs, age(id));
        c_ys = vertcat(c_ys, age_dnam(id));
        c_diff = vertcat(c_diff, agediff(id));
    else
        t_xs = vertcat(t_xs, age(id));
        t_ys = vertcat(t_ys, age_dnam(id));
        t_diff = vertcat(t_diff, agediff(id));
    end
    
end



fig = figure;
propertyeditor('on');
h = scatter(c_xs, c_ys, 250, 'o', 'LineWidth',  1, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', 'green', 'MarkerEdgeAlpha', 0.5, 'MarkerFaceAlpha', 0.5);
legend(h, 'Control')
hold all;
h = scatter(t_xs, t_ys, 250, 'o', 'LineWidth',  1, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', 'red', 'MarkerEdgeAlpha', 0.5, 'MarkerFaceAlpha', 0.5);
legend(h, 'Treatment')
set(gca, 'FontSize', 40);
xlabel('Age', 'Interpreter', 'latex');
set(gca, 'FontSize', 40);
ylabel('DNAmAge', 'Interpreter', 'latex');
h = plot([0 100], [0 100], 'k');
h.Annotation.LegendInformation.IconDisplayStyle = 'off';
legend(gca,'off');
legend('Location','Southeast','NumColumns',1)
fn_fig = sprintf('%s/Age_DNAmAge_norm(%s)_part(%s)', figures_path, norm, part);
oqs_save_fig(fig, fn_fig)


% fn = sprintf('%s/control.csv', path);
% ctrl = readtable(fn);
% c_xs_l = [0 100];
% c_ys_l = c_xs_l * ctrl.coeffs(2) + ctrl.coeffs(1);
% fn = sprintf('%s/treatment.csv', path);
% ctrl = readtable(fn);
% t_xs_l = [0 100];
% t_ys_l = t_xs_l * ctrl.coeffs(2) + ctrl.coeffs(1);
% h = plot(c_xs_l, c_ys_l, 'Color', 'b');
% h.Annotation.LegendInformation.IconDisplayStyle = 'off';
% h = plot(t_xs_l, t_ys_l, 'Color', 'r');
% h.Annotation.LegendInformation.IconDisplayStyle = 'off';

p = kruskalwallis(agediff, status, 'on');
grid on;
propertyeditor('on')
set(gca, 'FontSize', 40);
ylim([-20 30])
a = get(get(gca,'children'),'children');   % Get the handles of all the objects
t = get(a,'tag');   % List the names of all the objects 
idx = strcmpi(t,'box');  % Find Box objects
boxes = a(idx);          % Get the children you need
set(a,'linewidth',3); % Set width
idx = strcmpi(t,'Outliers');
outliers = a(idx);
set(outliers,'visible','off')
dim = [.15 .13 .3 .3];
str = sprintf('Kruskal-Wallis p-value: %0.2e', p);
tb = annotation('textbox',dim,'String',str,'verticalalignment','Bottom' ,'FitBoxToText','on', 'FontSize', 24);
hold all;
h = scatter(1. * ones(size(c_diff, 1), 1).*(1+(rand(size(c_diff))-0.5)/10), c_diff, 100, 'o', 'LineWidth',  1, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', 'green', 'MarkerEdgeAlpha', 0.5, 'MarkerFaceAlpha', 0.5);
h.Annotation.LegendInformation.IconDisplayStyle = 'off';
hold all;
h = scatter(2. * ones(size(t_diff, 1), 1).*(1+(rand(size(c_diff))-0.5)/10), t_diff, 100, 'o', 'LineWidth',  1, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', 'red', 'MarkerEdgeAlpha', 0.5, 'MarkerFaceAlpha', 0.5);
h.Annotation.LegendInformation.IconDisplayStyle = 'off';


fn_fig = sprintf('%s/AgeAccelerationDiff_C_T_norm(%s)_part(%s)', figures_path, norm, part);
oqs_save_fig(gcf, fn_fig)

