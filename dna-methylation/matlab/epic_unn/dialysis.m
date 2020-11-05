clear all;

path = 'E:/YandexDisk/Work/pydnameth/unn_epic/horvath';
figures_path = 'E:/YandexDisk/Work/pydnameth/unn_epic/horvath/figures';
fn = sprintf('%s/data/betas_horvath_calculator_norm_fun.output.csv', path);
obs = readtable(fn);

status = obs.Sample_Group;
agediff = obs.AgeAccelerationDiff;
age = obs.Age;
age_dnam = obs.DNAmAge;
dial = obs.dialysis;

dialysis_xs = [];
dialysis_ys = [];

for id = 1 : size(age, 1)
    
    if string(dial{id}) ~= '-'
        dialysis_xs = vertcat(dialysis_xs, str2double(dial(id)));
        dialysis_ys = vertcat(dialysis_ys, agediff(id));
    end
    
end

fig = figure;
h = plot(dialysis_xs, dialysis_ys, 'o', 'MarkerSize', 15, 'Color', 'b', 'LineWidth', 2);
h.Color(4) = 0.5;
legend(h, 'Dialysis')
hold all;
set(gca, 'FontSize', 40);
xlabel('Time on dialysis', 'Interpreter', 'latex');
set(gca, 'FontSize', 40);
ylabel('AgeAccelerationDiff', 'Interpreter', 'latex');
fn_fig = sprintf('%s/dialysis_AgeAccelerationDiff', figures_path);
oqs_save_fig(fig, fn_fig)
