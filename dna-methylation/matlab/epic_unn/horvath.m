clear all;

path = 'E:/YandexDisk/Work/pydnameth/unn_epic';

fn = sprintf('%s/betas_horvath_calculator_filtered_normallized.output.csv', path);
obs = readtable(fn);

status = obs.Sample_Group;
%agediff = obs.AgeAccelerationDiff;
age = obs.Age;
age_dnam = obs.DNAmAge;

c_xs = [];
c_ys = [];

t_xs = [];
t_ys = [];

for id = 1 : size(age, 1)
    
    if status{id} == 'C'
        c_xs = vertcat(c_xs, age(id));
        c_ys = vertcat(c_ys, age_dnam(id));
    else
        t_xs = vertcat(t_xs, age(id));
        t_ys = vertcat(t_ys, age_dnam(id));
    end
    
end

fig = figure;
h = plot(c_xs, c_ys, 'o', 'MarkerSize', 10, 'Color', 'b');
h.Color(4) = 0.5;
legend(h, 'Control')
hold all;
h = plot(t_xs, t_ys, 'o', 'MarkerSize', 10, 'Color', 'r');
h.Color(4) = 0.5;
legend(h, 'Treatment')
set(gca, 'FontSize', 40);
xlabel('Age', 'Interpreter', 'latex');
set(gca, 'FontSize', 40);
ylabel('DNAmAge', 'Interpreter', 'latex');
h = plot([0 100], [0 100], 'k');
h.Annotation.LegendInformation.IconDisplayStyle = 'off';
legend(h, 'Treatment')
