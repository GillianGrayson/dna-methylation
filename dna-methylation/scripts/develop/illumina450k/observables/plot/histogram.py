import pydnameth as pdm
from scripts.develop.routines import *

data = pdm.Data(
    path='',
    base='liver'
)

annotations = pdm.Annotations(
    name='annotations',
    type='450k',
    exclude='bad_cpgs',
    select_dict={
        'CHR': ['-X', '-Y']
    }
)

cells = pdm.Cells(
    name='cells_horvath_calculator',
    types='any'
)

observables = pdm.Observables(
    name='observables',
    types={}
)

attributes = pdm.Attributes(
    target='age',
    observables=observables,
    cells=cells
)

observables_list = get_observables_list(data.base)
data_params = get_data_params(data.base)

pdm.observables_plot_histogram(
    data=data,
    annotations=annotations,
    attributes=attributes,
    observables_list=observables_list,
    method_params={
        'bin_size': 1.0,
        'opacity': 0.80,
        'barmode': 'overlay',
        'x_range': [5, 105],
        'legend_size': 1
    }
)