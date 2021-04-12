clear all;

part = 'v2';
path = 'E:/YandexDisk/Work/pydnameth/unn_epic';
figures_path = sprintf('E:/YandexDisk/Work/pydnameth/unn_epic/figures/features/venn/part(%s)', part);
if ~exist(figures_path, 'dir')
    mkdir(figures_path)
end

list1 = importdata('vennList1.txt');
list2 = importdata('vennList2.txt');
list3 = importdata('vennList3.txt');
names = {'Associated with CKD', 'Associated with Age (Control)', 'Associated with Age Acceleration (Disease)'};

fig = plotVenn3({list1, list2, list3}, names, 50, 20);
fn_fig = sprintf('%s/%s', figures_path, strjoin(names, '_'));
oqs_save_fig(gcf, fn_fig)

