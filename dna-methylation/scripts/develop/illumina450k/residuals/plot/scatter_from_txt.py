import pydnameth as pdm
from scripts.develop.routines import *


f = open('cpgs.txt', 'r')
items = f.read().splitlines()
reverses = ['no'] * len(items)
x_ranges = ['auto'] * len(items)
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
data_params['cells'] = ['Bcell', 'CD4T', 'CD8T', 'Gran', 'NK']

attributes = pdm.Attributes(
    target='age',
    observables=observables,
    cells=cells
)

pdm.residuals_plot_scatter(
    data=data,
    annotations=annotations,
    attributes=attributes,
    observables_list=observables_list,
    data_params=data_params,
    method_params={
        'items': items,
        'reverses': reverses,
        'x_ranges': x_ranges,
        'y_ranges': y_ranges,
        'line': 'no',
        'fit': 'yes',
        'semi_window': 6,
        'box_b': 'Q1',
        'box_t': 'Q99',
        'legend_size': 1,
        'add': 'none'
    }
)