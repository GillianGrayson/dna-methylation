clear all;

cell_types = {'Bcell', 'CD4T', 'CD8T', 'Gran', 'NK'}';
cell_types = {'Bcell', 'CD4T', 'CD8T', 'Neu', 'NK'}';

path = 'E:/YandexDisk/Work/pydnameth/unn_epic';
figures_path = 'E:/YandexDisk/Work/pydnameth/unn_epic/figures/cells';

norm = 'x';
part = 'x';

%fn = sprintf('%s/horvath/data/betas_horvath_calculator_norm_%s_part_%s.output.csv', path, norm, part);
fn = sprintf('%s/cell_counts.csv', path);

obs = readtable(fn);

colors = distinguishable_colors(size(cell_types, 1));

fig = figure;
for ct_id = 1:size(cell_types, 1)
    cell = obs.(cell_types{ct_id});
    
    color = colors(ct_id, :);
    
    pdf.x_num_bins = 201;
    pdf.x_label = 'Cells';
    pdf.x_bin_s = 0;
    pdf.x_bin_f = 1;
    pdf = oqs_pdf_1d_setup(pdf);
    pdf = oqs_pdf_1d_update(pdf, cell);
    pdf = oqs_pdf_1d_release(pdf);
    hline = plot(pdf.x_bin_centers, pdf.pdf, 'LineWidth', 2, 'Color', color);
    legend(hline, sprintf('%s', cell_types{ct_id}))
    set(gca, 'FontSize', 30);
    xlabel(pdf.x_label, 'Interpreter', 'latex');
    set(gca, 'FontSize', 30);
    ylabel('PDF', 'Interpreter', 'latex');
    hold all;
end
propertyeditor('on')

legend(gca,'off');
legend('Location','best','NumColumns',1)

fn_fig = sprintf('%s/cells_norm(%s)_part(%s)', figures_path, norm, part);
oqs_save_fig(fig, fn_fig)



