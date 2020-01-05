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

items = table_dict['i']
x_ranges = [[5, 105]] * len(items)
y_ranges = []
for index in range(0, len(items)):
    y_ranges.append([table_dict['begin'][index], table_dict['end'][index]])


data_bases = ['GSE87571']

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

    if data_base == 'GSE55763':
        observables_list = [
            {'gender': 'F', 'is_duplicate': '0', 'age': (35, 100)},
            {'gender': 'M', 'is_duplicate': '0', 'age': (35, 100)}
        ]

        data_params = {
            'cells': ['CD8T', 'CD4T', 'NK', 'Bcell', 'Gran']
        }

        cells = pdm.Cells(
            name='cells_horvath_calculator',
            types='any'
        )
    else:
        observables_list = [
            {'gender': 'F'},
            {'gender': 'M'}
        ]

        data_params = {
            'cells': ['CD8T', 'CD4T', 'NK', 'Bcell', 'Gran']
        }

        cells = pdm.Cells(
            name='cells_horvath_calculator',
            types='any'
        )

    attributes = pdm.Attributes(
        target='age',
        observables=observables,
        cells=cells
    )

    pdm.residuals_common_plot_scatter(
        data=data,
        annotations=annotations,
        attributes=attributes,
        observables_list=observables_list,
        data_params=data_params,
        method_params={
            'items': items,
            'x_ranges': x_ranges,
            'y_ranges': y_ranges,
            'line': 'yes',
            'fit': 'no',
            'semi_window': 'none',
            'legend_size': 1,
            'box_b': 'Q5',
            'box_t': 'Q95'
        }
    )
