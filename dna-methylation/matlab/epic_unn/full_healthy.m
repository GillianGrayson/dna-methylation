clear all;

path = 'E:/YandexDisk/Work/pydnameth/unn_epic';
figures_path = 'E:/YandexDisk/Work/pydnameth/unn_epic/horvath/figures';
fn = sprintf('%s/betas_horvath_calculator_filtered_normallized.output.csv', path);
obs = readtable(fn);

status = obs.Sample_Group;
agediff = obs.AgeAccelerationDiff;
age = obs.Age;
age_dnam = obs.DNAmAge;
disease = obs.chronic_disease;

h_xs = [];
h_ys = [];
h_age_diff = [];

for id = 1 : size(age, 1)
    if string(disease{id}) == 'no'
        h_xs = vertcat(h_xs, age(id));
        h_ys = vertcat(h_ys, age_dnam(id));
        h_age_diff = vertcat(h_age_diff, agediff(id));
    end
end

fig = figure;
h = plot(h_xs, h_ys, 'o', 'MarkerSize', 10, 'Color', 'b');
legend(h, 'Healthy')
hold all;
set(gca, 'FontSize', 40);
xlabel('Age', 'Interpreter', 'latex');
set(gca, 'FontSize', 40);
ylabel('DNAmAge', 'Interpreter', 'latex');
h = plot([0 100], [0 100], 'k');
h.Annotation.LegendInformation.IconDisplayStyle = 'off';

fn_fig = sprintf('%s/healthy_Age_DNAmAge', figures_path);
oqs_save_fig(fig, fn_fig)

fig = figure;
boxplot(h_age_diff)
hold all;
set(gca, 'FontSize', 40);
xlabel('Heatlhy')
set(gca,'XTick',[]);
ylabel('AgeAccelerationDiff')
fn_fig = sprintf('%s/healthy_AgeAccelerationDiff', figures_path);
oqs_save_fig(fig, fn_fig)

