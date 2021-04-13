clear all;

part = 'v2';

globalFontSize = 30;
legendFontSize = 18;
legend_location = 'NorthWest';

path = 'E:/YandexDisk/Work/pydnameth/unn_epic';
figures_path = sprintf('E:/YandexDisk/Work/pydnameth/unn_epic/figures/features/before_after/part(%s)', part);
if ~exist(figures_path, 'dir')
    mkdir(figures_path)
end
fn = sprintf('%s/all_data/raw/before_after_dialysis.xlsx', path);
opts = detectImportOptions(fn);
tbl = readtable(fn, opts);

y_features = importdata('before_after/y_features.txt');
y_labels = importdata('before_after/y_labels.txt');

statuses = {'Before', 'After'}';
subjects = unique(tbl.('ID'));
colors = distinguishable_colors(size(subjects, 1));

for f_id = 1:size(y_features, 1)
    fig = figure;
    propertyeditor('on');
    
    for s_id = 1:size(subjects, 1)
        x1 = 1;
        x2 = 2;
        y1 = tbl{(strcmp(tbl.('DialysisStatus'), 'Before') & strcmp(tbl.('ID'), subjects{s_id})), y_features{f_id}};
        y2 = tbl{(strcmp(tbl.('DialysisStatus'), 'After') & strcmp(tbl.('ID'), subjects{s_id})), y_features{f_id}};
        h = plot([x1, x2], [y1, y2], 'LineStyle', '-', 'Marker', 'o', 'LineWidth', 3, 'MarkerSize', 30, 'Color', colors(s_id, :), 'MarkerFaceColor', 'white');
        legend(h, subjects{s_id});
        hold all;
    end
    
    set(gca, 'FontSize', globalFontSize);
    xlabel('', 'Interpreter', 'latex');
    ylabel(y_labels{f_id}, 'Interpreter', 'latex');
    set(gca, 'FontSize', globalFontSize);
    ax = gca;
    xticks([1 2]);
    xticklabels(statuses);
    ax.XAxis.FontSize = globalFontSize;
    ax.YAxis.FontSize = globalFontSize;
	set(ax,'TickLabelInterpreter','Latex');
    legend(gca,'off');
    legend('Location', legend_location, 'NumColumns', 1, 'Interpreter', 'latex');
    legend('FontSize', legendFontSize);
    xlim([0.7, 2.3]);
    yShift = max(tbl.(y_features{f_id})) - min(tbl.(y_features{f_id}));
    ylim([min(tbl.(y_features{f_id})) - yShift * 0.15, max(tbl.(y_features{f_id})) + yShift * 0.15]);
    
    
    fn_fig = sprintf('%s/%s', figures_path, y_features{f_id});
    oqs_save_fig(gcf, fn_fig)
end

