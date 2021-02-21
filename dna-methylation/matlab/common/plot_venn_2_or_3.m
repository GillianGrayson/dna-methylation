clear all;

datas{1} = importdata("E:\YandexDisk\Work\pydnameth\draft\2\figures\4\Age.txt");
datas{2} = importdata("E:\YandexDisk\Work\pydnameth\draft\2\figures\4\DNAmPhenoAge.txt");
datas{3} = importdata("E:\YandexDisk\Work\pydnameth\draft\2\figures\4\PhenoAge.txt");
names{1} = {'Age'};
names{2} = {'DNAmPhenoAge'};
names{3} = {'PhenoAge'};

areas = [...
    size(datas{1}, 1), ...
    size(datas{2}, 1), ...
    size(datas{3}, 1) ...
    ];
intersections = [ ...
    size(intersect(datas{1}, datas{2}), 1), ...
    size(intersect(datas{1}, datas{3}), 1), ...
    size(intersect(datas{2}, datas{3}), 1), ...
    size(intersect(intersect(datas{1}, datas{2}), datas{3}), 1), ...
    ];

fig = figure;
[H, S] = venn(areas, intersections, 'ErrMinMode', 'ChowRodgers', 'FaceAlpha', 0.3, 'EdgeColor', 'None', 'DisplayName', names);
axObjs = fig.Children;
circles = axObjs.Children;
area_pgons = {};
for p_id = 1:size(circles, 1)
    area_pgons{p_id} = polyshape(circles(p_id).Vertices(:, 1), circles(p_id).Vertices(:, 2));
end
close(fig);

colors = distinguishable_colors(7);
A = area_pgons{3};
B = area_pgons{2};
C = area_pgons{1};
Ax = subtract(A, union(B,C));
Bx = subtract(B, union(A,C));
Cx = subtract(C, union(A,B));
ABx = subtract(intersect(A, B), C);
ACx = subtract(intersect(A, C), B);
BCx = subtract(intersect(B, C), A);
ABCx = intersect(intersect(A, B), C);
pgons = {Ax; Bx; Cx; ABx; ACx; BCx; ABCx};

fig = figure;
for  p_id = 1:size(pgons, 1)
    h = plot(pgons{p_id}, 'FaceColor', colors(p_id, :), 'FaceAlpha', 0.3, 'EdgeColor', 'None');
    hold all;
    if p_id <= 3
        legend(h, names{p_id});
    else
        h.Annotation.LegendInformation.IconDisplayStyle = 'off';
    end 
end

for z_id = 1 : size(S.ZonePop, 2)
    label = sprintf('%d', S.ZonePop(z_id));
    x = S.ZoneCentroid(z_id, 1);
    y = S.ZoneCentroid(z_id, 2);
    text(x, y, label, 'FontSize', 16, 'Interpreter', 'latex')
end
propertyeditor on;
box on;
set(gca,'XTick',[], 'YTick', [])
legend(gca,'off');
legend('Location', 'NorthWest', 'NumColumns', 1, 'Interpreter', 'latex');
legend('FontSize', 30);
