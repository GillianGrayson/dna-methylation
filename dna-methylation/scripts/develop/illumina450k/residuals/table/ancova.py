import pydnameth as pdm
from scripts.develop.routines import *


data = pdm.Data(
    path='',
    base='EPIC'
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

target = get_target(data.base)
observables_list = get_observables_list(data.base)
data_params = get_data_params(data.base)
data_params['cells'] = ['Bcell', 'CD4T', 'CD8T', 'Gran', 'NK']

attributes = pdm.Attributes(
    target=target,
    observables=observables,
    cells=cells
)

pdm.residuals_table_ancova(
    data=data,
    annotations=annotations,
    attributes=attributes,
    observables_list=observables_list,
    data_params=data_params
)