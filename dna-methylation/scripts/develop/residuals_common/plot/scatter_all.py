import pydnameth as pdm
import pandas as pd
import os.path

fn = 'cpgs.xlsx'
table_dict = {}
if os.path.isfile(fn):
    df = pd.read_excel(fn)
    tmp_dict = df.to_dict()
    for key in tmp_dict:
        curr_dict = tmp_dict[key]
        table_dict[key] = list(curr_dict.values())

cpgs = table_dict['cpg']
y_begins = table_dict['begin']
y_ends = table_dict['end']

data_bases = ['GSE55763']

for cpg_id in range(0, len(cpgs)):
    cpg_list = [cpgs[cpg_id]]
    y_begin = y_begins[cpg_id]
    y_end = y_ends[cpg_id]

    for data_base in data_bases:

        data = pdm.Data(
            path='',
            base=data_base
        )

        annotations = pdm.Annotations(
            name='annotations',
            exclude='bad_cpgs',
            cross_reactive='any',
            snp='any',
            chr='NS',
            gene_region='any',
            geo='any',
            probe_class='any'
        )

        observables = pdm.Observables(
            name='observables',
            types={}
        )

        cells = pdm.Cells(
            name='cells',
            types='any'
        )

        attributes = pdm.Attributes(
            target='age',
            observables=observables,
            cells=cells
        )

        if data_base == 'GSE55763':
            observables_list = [
                {'gender': 'F', 'is_duplicate': '0'},
                {'gender': 'M', 'is_duplicate': '0'}
            ]

            data_params = {
                'cells': ['CD8T', 'CD4T', 'NK', 'Bcell', 'Gran']
            }
        else:
            observables_list = [
                {'gender': 'F'},
                {'gender': 'M'}
            ]

            data_params = {
                'cells': ['B', 'CD4T', 'NK', 'CD8T', 'Gran']
            }

        pdm.residuals_common_plot_scatter(
            data=data,
            annotations=annotations,
            attributes=attributes,
            observables_list=observables_list,
            cpg_list=cpg_list,
            data_params=data_params,
            method_params={
                'x_range': [5, 105],
                'y_range': [y_begin, y_end],
                'line': 'yes',
                'fit': 'no',
                'semi_window': 'none',
                'legend_size': 1
            }
        )