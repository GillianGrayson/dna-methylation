import pydnameth as pdm
import pandas as pd
import os.path
from scripts.develop.routines import *

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

data_bases = ['GSE87571_TEST']

for data_base in data_bases:

    data = pdm.Data(
        path='',
        base='GSE43414'
    )

    annotations = pdm.Annotations(
        name='annotations',
        type='450k',
        exclude='bad_cpgs',
        select_dict={
            'CHR': ['-X', '-Y']
        }
    )

    observables = pdm.Observables(
        name='observables',
        types={}
    )

    cells = pdm.Cells(
        name='cells',
        types='any'
    )

    target = get_target(data.base)
    observables_list = get_observables_list(data.base)
    data_params = get_data_params(data.base)

    attributes = pdm.Attributes(
        target=target,
        observables=observables,
        cells=cells
    )

    pdm.betas_plot_scatter(
        data=data,
        annotations=annotations,
        attributes=attributes,
        observables_list=observables_list,
        method_params={
            'items': items,
            'x_ranges': x_ranges,
            'y_ranges': y_ranges,
            'line': 'yes',
            'fit': 'yes',
            'semi_window': 8,
            'box_b': 'Q5',
            'box_t': 'Q95',
            'add': 'none',
            'legend_size': 1
        }
    )
