clear all;

figure;
var = 'RMSE';
var_id = 7;

geo = 'GSE40279';
fn = 'E:/YandexDisk/Work/pydnameth/GSE40279/betas/clock/linreg/96c5b6a23d8c52c98cf8e8bc369643b6/part(0.25)_runs(100)_size(100)_type(all).xlsx';
T = readtable(fn);
x = linspace(1, size(T, 1), size(T, 1))';
y = table2array(T(:, var_id));
hLine = plot(x, y, 'LineWidth', 2);
legend(hLine, geo)
set(gca, 'FontSize', 30);
xlabel('number of top-rank CpGs', 'Interpreter', 'latex');
set(gca, 'FontSize', 30);
ylabel(var, 'Interpreter', 'latex');
hold all;

geo = 'GSE87571';
fn = "E:\YandexDisk\Work\pydnameth\GSE87571\betas\clock\linreg\7ad3ee1fb1440ed0c8431fadebe9bf56\part(0.25)_runs(100)_size(100)_type(all).xlsx";
T = readtable(fn);
x = linspace(1, size(T, 1), size(T, 1))';
y = table2array(T(:, var_id));
hLine = plot(x, y, 'LineWidth', 2);
legend(hLine, geo)
set(gca, 'FontSize', 30);
xlabel('number of top-rank CpGs', 'Interpreter', 'latex');
set(gca, 'FontSize', 30);
ylabel(var, 'Interpreter', 'latex');
hold all;

geo = 'EPIC';
fn = "E:\YandexDisk\Work\pydnameth\EPIC\betas\clock\linreg\fb086b83f54c6e5ef6a7c3d4eb18e3d9\part(0.25)_runs(100)_size(100)_type(all).xlsx";
T = readtable(fn);
x = linspace(1, size(T, 1), size(T, 1))';
y = table2array(T(:, var_id));
hLine = plot(x, y, 'LineWidth', 2);
legend(hLine, geo)
set(gca, 'FontSize', 30);
xlabel('number of top-rank CpGs', 'Interpreter', 'latex');
set(gca, 'FontSize', 30);
ylabel(var, 'Interpreter', 'latex');
hold all;

geo = 'GSE55763';
fn = "E:\YandexDisk\Work\pydnameth\GSE55763\betas\clock\linreg\0f95d0c88851a535cd1798f272def71e\part(0.25)_runs(100)_size(100)_type(all).xlsx";
T = readtable(fn);
x = linspace(1, size(T, 1), size(T, 1))';
y = table2array(T(:, var_id));
hLine = plot(x, y, 'LineWidth', 2);
legend(hLine, geo)
set(gca, 'FontSize', 30);
xlabel('number of top-rank CpGs', 'Interpreter', 'latex');
set(gca, 'FontSize', 30);
ylabel(var, 'Interpreter', 'latex');
hold all;