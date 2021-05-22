clear all;

part = 'v2';

target = 'DNAmPhenoAgeAA';
label = 'DNAmPhenoAgeAA';
group_feature = 'Group';
groups = {'Control', 'ESRD'}';

highlight_ids = {}';
highlight_color = [0 0 0];

colors = {[0 1 0], [1 0 1]}';

opacity = 0.65;
globalFontSize = 36;
legendFontSize = 18;
legend_location = 'NorthEast';
%yLim = [-50, 1200];
yLim = 'auto';

path = 'E:/YandexDisk/Work/pydnameth/unn_epic';
figures_path = sprintf('E:/YandexDisk/Work/pydnameth/unn_epic/figures/features/boxplot_byGroup/part(%s)', part);
if ~exist(figures_path, 'dir')
    mkdir(figures_path)
end
fn = sprintf('%s/all_data/table_part(%s).xlsx', path, part);
opts = detectImportOptions(fn);
opts = setvartype(opts, {group_feature}, 'string');
tbl = readtable(fn, opts);

incKeys = {};
incVals = {{}};
decKeys = {};
decVals = {{}};
if size(incKeys, 1) > 0
    incMap = containers.Map(incKeys,incVals);
else
    incMap = containers.Map();
end
if size(decKeys, 1) > 0
    decMap = containers.Map(decKeys,decVals);
else
    decMap = containers.Map();
end
indexesFilt = get_filtered_indexes(tbl, incMap, decMap); 
tbl = tbl(indexesFilt, :);

status = tbl.(group_feature);
feature = strrep(target,'.','_');
features = tbl.(feature);

featuresByGroup = {};
scattersAux = {};
not_highlight_tbl = tbl(~ismember(tbl.('ID'), highlight_ids), :);
highlight_tbl = tbl(ismember(tbl.('ID'), highlight_ids), :);
for g_id = 1:size(groups, 1)
    vars = tbl{strcmp(tbl.(group_feature), groups{g_id}), feature};
    featuresByGroup{g_id} = vars;
    
    scattersAux{g_id} = {not_highlight_tbl{strcmp(not_highlight_tbl.(group_feature), groups{g_id}), feature}; highlight_tbl{strcmp(highlight_tbl.(group_feature), groups{g_id}), feature}};
end

features_ordered  = [];
mod_status = [];
for g_id = 1:size(groups, 1)
    features_ordered = vertcat(features_ordered, featuresByGroup{g_id});
    tmp = strings(size(featuresByGroup{g_id}, 1), 1);
    tmp(:) = groups{g_id};
    mod_status = vertcat(mod_status, tmp);
end

fig = figure;

subplot(1, 2, 2)
for g_id = 1:size(groups, 1)
    [f,xi] = ksdensity(featuresByGroup{g_id});
    
    
    
    pdf.x_num_bins = 101;
    shift = max(featuresByGroup{g_id}) - min(featuresByGroup{g_id});
    pdf.x_bin_s = min(featuresByGroup{g_id}) - 0.15 * shift;
    pdf.x_bin_f = max(featuresByGroup{g_id}) + 0.15 * shift;
    pdf = oqs_pdf_1d_setup(pdf);
    pdf = oqs_pdf_1d_update(pdf, featuresByGroup{g_id});
    pdf = oqs_pdf_1d_release(pdf);
    
    
    pdf.pdf = smooth(pdf.pdf, 20, 'loess');
    inc_count = sum(sum(pdf.pdf));
    pdf.pdf = pdf.pdf / (inc_count * pdf.x_bin_shift);
    pdf.norm = sum(sum(pdf.pdf)) * pdf.x_bin_shift;
    fprintf('pdf_norm = %0.16e\n', pdf.norm);
    
    
    hline = plot(pdf.pdf, pdf.x_bin_centers, 'LineWidth', 2, 'Color', colors{g_id});
    %hline = plot(f, xi, 'LineWidth', 2, 'Color', colors{g_id});
    legend(hline, sprintf('%s', groups{g_id}))
    set(gca, 'FontSize', globalFontSize);
    ylabel('')
    set(gca,'yticklabel',{[]})
    hold all;
end
ylim(yLim);
yl = get(gca, 'YLim');
ylim(yl);
legend(gca,'off');
legend('Location', legend_location, 'NumColumns', 1, 'Interpreter', 'latex');
legend('FontSize', legendFontSize);
title('Density', 'FontSize', globalFontSize, 'FontWeight', 'normal', 'Interpreter', 'latex');
set(gca, 'TickLabelInterpreter', 'latex')
set(gca, 'Position', [0.705 0.09 0.28 0.835]);
xlim([0, inf]);
box on;
grid on;

subplot(1, 2, 1)
propertyeditor('on');
positions = 0.5 * linspace(1, size(groups, 1), size(groups, 1));
for g_id = 1:size(groups, 1)
    
    qs = quantile(featuresByGroup{g_id},[0.25 0.50 0.75]);
    fprintf('Q1 %s: %0.4e\n', groups{g_id}, qs(1));
    fprintf('Q2 %s: %0.4e\n', groups{g_id}, qs(2));
    fprintf('Q3 %s: %0.4e\n', groups{g_id}, qs(3));
    
    b = boxplot(featuresByGroup{g_id}, 'Notch', 'off', 'positions', positions(g_id), 'Colors', 'k');
    set(gca, 'FontSize', globalFontSize);
    all_items = handle(b);
    tags = get(all_items,'tag');
    idx = strcmpi(tags,'box');
    boxes = all_items(idx);
    set(all_items,'linewidth',3)
    idx = strcmpi(tags,'Outliers');
    outliers = all_items(idx);
    set(outliers, 'visible', 'off')
    hold all;
    for sc_id = 1:2
        vals = scattersAux{g_id}{sc_id};
        if size(vals, 1) > 0
            xs = positions(g_id) * ones(size(vals, 1), 1) + ((rand(size(vals))-0.5)/10);
            if sc_id == 1
                color = colors{g_id};
                h = scatter(xs, vals, 100, 'o', 'LineWidth',  1, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', color, 'MarkerEdgeAlpha', opacity, 'MarkerFaceAlpha', opacity);
            else
                color = highlight_color;
                h = scatter(xs, vals, 200, 'x', 'LineWidth',  4, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', color, 'MarkerEdgeAlpha', opacity, 'MarkerFaceAlpha', opacity);
            end
            h.Annotation.LegendInformation.IconDisplayStyle = 'off';
            hold all;
        end
    end
%     xs = positions(g_id) * ones(size(featuresByGroup{g_id}, 1), 1) + ((rand(size(featuresByGroup{g_id}))-0.5)/10);
%     h = scatter(xs, featuresByGroup{g_id}, 100, 'o', 'LineWidth',  1, 'MarkerEdgeColor', 'black', 'MarkerFaceColor', colors{g_id}, 'MarkerEdgeAlpha', opacity, 'MarkerFaceAlpha', opacity);
%     h.Annotation.LegendInformation.IconDisplayStyle = 'off';
%     hold all;
end
xticks(positions);
xticklabels(groups);
axis auto;
xlim([min(positions) - 0.3, max(positions) + 0.3])
set(gca, 'TickLabelInterpreter', 'latex')
ylabel(label, 'Interpreter', 'latex')
box on;
grid on;

pValueKW = kruskalwallis(features_ordered, mod_status, 'off');
if size(groups, 1) == 2
    pValue = ranksum(featuresByGroup{1}, featuresByGroup{2});
else
    pValue = pValueKW;
end
str = sprintf('p-value: %0.2e', pValue);
title(str, 'FontSize', globalFontSize, 'FontWeight', 'normal', 'Interpreter', 'latex');
set(gca, 'Position', [0.13 0.09 0.57 0.835]);
ylim(yl);
hold all;

fn_fig = sprintf('%s/%s_group(%s)', figures_path, target, group_feature);
oqs_save_fig(gcf, fn_fig)
