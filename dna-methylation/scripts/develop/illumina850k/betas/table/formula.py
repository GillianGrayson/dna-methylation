import pydnameth as pdm
from scripts.develop.routines import *


data = pdm.Data(
    path='',
    base='unn_epic'
)

annotations = pdm.Annotations(
    name='annotations',
    type='850k',
    exclude='bad_cpgs_from_ChAMP',
    select_dict={
        'CHR': ['-X', '-Y']
    }
)

observables = pdm.Observables(
    name='observables',
    types={}
)

cells = pdm.Cells(
    name='cell_counts',
    types='any'
)

target = get_target(data.base)
attributes = pdm.Attributes(
    target=target,
    observables=observables,
    cells=cells
)

method_params = {
    'observables': ['Sample_Group'],
}

data_params = get_data_params(data.base)

pdm.betas_table_formula(
    data=data,
    annotations=annotations,
    attributes=attributes,
    data_params=data_params,
    method_params=method_params,
)