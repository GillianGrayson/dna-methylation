function fig = plot_gtex_expDiff(genes, gtex, datasets)

colors = distinguishable_colors(7);

group = cell(size(genes{1}, 1), 1);
group(:) = {datasets{1}};
A = table(genes{1}, group, 'VariableNames', {'Description', 'Group'});

group = cell(size(genes{2}, 1), 1);
group(:) = {datasets{2}};
B = table(genes{2}, group, 'VariableNames', {'Description', 'Group'});

group = cell(size(genes{3}, 1), 1);
group(:) = {datasets{3}};
C = table(genes{3}, group, 'VariableNames', {'Description', 'Group'});

Ax = table(setdiff(genes{1}, union(genes{2}, genes{3})), 'VariableNames', {'Description'});
Bx = table(setdiff(genes{2}, union(genes{1}, genes{3})), 'VariableNames', {'Description'});
Cx = table(setdiff(genes{3}, union(genes{1}, genes{2})), 'VariableNames', {'Description'});
ABx = table(setdiff(intersect(genes{1}, genes{2}), genes{3}), 'VariableNames', {'Description'});
ACx = table(setdiff(intersect(genes{1}, genes{3}), genes{2}), 'VariableNames', {'Description'});
BCx = table(setdiff(intersect(genes{2}, genes{3}), genes{1}), 'VariableNames', {'Description'});
ABCx = table(intersect(intersect(genes{1}, genes{2}), genes{3}), 'VariableNames', {'Description'});

A_tbl = innerjoin(A, gtex, 'Keys','Description');
B_tbl = innerjoin(B, gtex, 'Keys','Description');
C_tbl = innerjoin(C, gtex, 'Keys','Description');
Ax_tbl = innerjoin(Ax, gtex, 'Keys','Description');
Bx_tbl = innerjoin(Bx, gtex, 'Keys','Description');
Cx_tbl = innerjoin(Cx, gtex, 'Keys','Description');
ABx_tbl = innerjoin(ABx, gtex, 'Keys','Description');
ACx_tbl = innerjoin(ACx, gtex, 'Keys','Description');
BCx_tbl = innerjoin(BCx, gtex, 'Keys','Description');
ABCx_tbl = innerjoin(ABCx, gtex, 'Keys','Description');

metrics = gtex.Properties.VariableNames(3:end)';
pvalues_KW = zeros(size(metrics, 1), 1);
pvalues_ANOVA = zeros(size(metrics, 1), 1);
groups = vertcat(A_tbl.('Group'), B_tbl.('Group'), C_tbl.('Group'));
for m_id = 1 : size(metrics, 1)
    metric = metrics{m_id};
    xs = vertcat(A_tbl.(metric), B_tbl.(metric), C_tbl.(metric));
    minX = min(xs(xs > 0));
    logXs = log10(xs + 0.1 * minX);
    
    pvalues_KW(m_id) = kruskalwallis(logXs, groups, 'off');
    pvalues_ANOVA(m_id) = anova1(logXs, groups, 'off');
end

ololo = 1;


 p = kruskalwallis(agediff, mod_status, 'on');
    grid on;
    propertyeditor('on')
    set(gca, 'FontSize', 40);
    a = get(get(gca,'children'),'children');
    t = get(a,'tag');
    idx = strcmpi(t,'box');
    boxes = a(idx);
    set(a,'linewidth',3);
    idx = strcmpi(t,'Outliers');
    outliers = a(idx);
    set(outliers,'visible','off')
    dim = [.165 .13 .3 .3];
    ylabel('AccelerationDiff')
    str = sprintf('Kruskal-Wallis p-value: %0.2e', p);
    tb = annotation('textbox', dim, 'String', str, 'verticalalignment', 'Bottom', 'FitBoxToText', 'on', 'FontSize', 24);
    hold all;



end