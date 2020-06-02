from paper.routines.data.human_plasma_proteome import *
from statsmodels.stats.multitest import multipletests


def metal_process(metal_type, pval_perc, path):

    fn = path + f'/{metal_type}.xlsx'
    data_dict = load_table_dict_xlsx(fn)

    reject, pvals_corr, alphacSidak, alphacBonf = multipletests(
        data_dict['P-value'],
        0.05,
        method='fdr_bh'
    )
    data_dict['p_value_fdr_bh'] = pvals_corr

    reject, pvals_corr, alphacSidak, alphacBonf = multipletests(
        data_dict['P-value'],
        0.05,
        method='bonferroni'
    )
    data_dict['p_value_fdr_bf'] = pvals_corr

    pvals = np.array(data_dict['p_value_fdr_bh'])
    pvals_percentile = np.percentile(pvals, pval_perc)
    print(f'{metal_type} percentile: {pvals_percentile}')
    print(f'{metal_type} less 0.05: {np.count_nonzero(pvals_corr < 0.05)}')
    print(f'{metal_type} less 0.001: {np.count_nonzero(pvals_corr < 0.001)}')

    pvals_mod = -np.log10(pvals[np.nonzero(pvals)])
    xs, ys = get_pdf_x_and_y(pvals_mod)

    color = cl.scales['8']['qual']['Set1'][0]
    coordinates = color[4:-1].split(',')
    color_border = 'rgba(' + ','.join(coordinates) + ',' + str(0.8) + ')'

    y_max = 1.15 * max(ys)
    plot_data = []
    scatter = go.Scatter(
        x=xs,
        y=ys,
        name=metal_type,
        mode='lines',
        line=dict(
            width=4,
            color=color_border
        ),
        showlegend=True
    )
    plot_data.append(scatter)

    scatter = go.Scatter(
        x=[-np.log10(pvals_percentile)] * 2,
        y=[0, y_max],
        mode='lines',
        line=dict(
            width=4,
            color=color_border,
            dash='dot'
        ),
        showlegend=False
    )
    plot_data.append(scatter)

    layout = get_layout('$-log_{10}({pvalue})$', 'Probability density function')

    fn = f'{path}/{metal_type}'
    figure = go.Figure(data=plot_data, layout=layout)
    figure.update_xaxes(range=[min(xs), 1.3 * max(xs)])
    figure.update_yaxes(range=[0, y_max])
    plotly.offline.plot(figure, filename=f'{fn}.html', auto_open=False, show_link=True)
    plotly.io.write_image(figure, f'{fn}.png')
    plotly.io.write_image(figure, f'{fn}.pdf')

    data_dict_filtered = dict.fromkeys(data_dict.keys())
    for key in data_dict_filtered:
        data_dict_filtered[key] = []

    for cpg_id in tqdm(range(0, len(data_dict['MarkerName'])), desc=f'{metal_type} processing'):

        pval = pvals[cpg_id]

        if pval < pvals_percentile:
            for key in data_dict:
                data_dict_filtered[key].append(data_dict[key][cpg_id])

    return data_dict_filtered