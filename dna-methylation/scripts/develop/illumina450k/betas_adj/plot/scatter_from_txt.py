import pydnameth as pdm
from scripts.develop.routines import *

f = open('cpgs.txt', 'r')
items = f.read().splitlines()
x_ranges = [[5, 105]] * len(items)
y_ranges = ['auto'] * len(items)


data = pdm.Data(
    path='',
    base='GSE87571'
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
    name='cells_horvath_calculator',
    types='any'
)

observables_list = get_observables_list(data.base)

data_params = get_data_params(data.base)
#data_params['observables'] = ['gender']
data_params['cells'] = ['CD8T', 'CD4T', 'NK', 'Bcell', 'Gran']

attributes = pdm.Attributes(
    target='age',
    observables=observables,
    cells=cells
)

pdm.betas_adj_plot_scatter(
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
        'fit': 'none',
        'semi_window': 8,
        'box_b': 'Q5',
        'box_t': 'Q95',
        'legend_size': 2,
        'add': 'none'
    }
)