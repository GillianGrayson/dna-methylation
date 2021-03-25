import pydnameth as pdm
from scripts.develop.routines import *

f = open('cpgs.txt', 'r')
items = f.read().splitlines()
reverses = ['no'] * len(items)
x_ranges = ['auto'] * len(items)
y_ranges = ['auto'] * len(items)

data = pdm.Data(
    base='unn_epic'
)

annotations = pdm.Annotations(
    name='annotations',
    type='850k',
    exclude='none',
    select_dict={}
)

observables = pdm.Observables(
    name='observables_part(v1)',
    types={'COVID': ['no', 'before'],
           'Sample_Chronology': [0, 1]}
)

cells = pdm.Cells(
    name='cell_counts_part(v1)',
    types='any'
)

target = get_target(data.base)
#observables_list = get_observables_list(data.base)
observables_list = [
    {'Group': 'Control'},
    {'Group': 'Disease'}
]
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
    data_params=data_params,
    method_params={
        'items': items,
        'reverses': reverses,
        'x_ranges': x_ranges,
        'y_ranges': y_ranges,
        'line': 'no',
        'fit': 'yes',
        'semi_window': 4,
        'box_b': 'Q1',
        'box_t': 'Q99',
        'legend_size': 1,
        'add': 'none'
    }
)
