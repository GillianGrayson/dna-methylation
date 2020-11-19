clear all;

part = 'wo_noIntensity_detP';


path = 'E:/YandexDisk/Work/pydnameth/unn_epic/raw';
figures_path = 'E:/YandexDisk/Work/pydnameth/unn_epic/figures/failed';
if ~exist(figures_path, 'dir')
    mkdir(figures_path)
end

fn = sprintf('%s/failed_part(%s).csv', path, part);
data = readtable(fn);
x = data.('Sample');
y = data.(2);

fig1 = figure;
propertyeditor('on');


barh(y, 'FaceColor', 'red');
yticks(linspace(1, size(x, 1), size(x, 1)))
set(gca,'yTickLabel',x);
ax = gca;
ax.YAxis.FontSize = 4;
set(gca,'TickLabelInterpreter','none')
xlabel('Number of probes with detP>0.01', 'Interpreter','none');
ax.XAxis.FontSize = 20;
grid on;

fn_fig = sprintf('%s/failed_part(%s)', figures_path, part);
oqs_save_fig(fig1, fn_fig)
saveas(gcf, sprintf('%s.png', fn_fig));
