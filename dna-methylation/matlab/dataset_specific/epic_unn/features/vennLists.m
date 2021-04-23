clear all;

part = 'v2';
path = 'E:/YandexDisk/Work/pydnameth/unn_epic';
figures_path = sprintf('E:/YandexDisk/Work/pydnameth/unn_epic/figures/features/venn/part(%s)', part);
if ~exist(figures_path, 'dir')
    mkdir(figures_path)
end

list1 = importdata('vennLists/vennList1.txt');
list2 = importdata('vennLists/vennList2.txt');
list3 = importdata('vennLists/vennList3.txt');
names2 = {'Associated with CKD', 'Associated with Age (Control)'};
names3 = {'Associated with CKD', 'Associated with Age (Control)', 'Associated with Age Acceleration (Disease)'};

fig = plotVenn2({list1, list2}, names2, 50, 20);
fn_fig = sprintf('%s/%s', figures_path, strjoin(names2, '_'));
oqs_save_fig(gcf, fn_fig)

fig = plotVenn3({list1, list2, list3}, names3, 50, 20);
fn_fig = sprintf('%s/%s', figures_path, strjoin(names3, '_'));
oqs_save_fig(gcf, fn_fig)

