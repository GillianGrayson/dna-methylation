import pydnameth as pdm
from scripts.develop.routines import *


data = pdm.Data(
    path='',
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

target = 'Group'
attributes = pdm.Attributes(
    target=target,
    observables=observables,
    cells=cells
)

method_params = {
    'observables': ['Sample_Group'],
}

data_params = {
    'part': 'v1',
    'config': '0.01_0.10_0.10',
    'norm': 'fun'
}
data_params['cells'] = ['Bcell', 'CD4T', 'CD8T', 'Neu', 'NK']

pdm.residuals_table_formula(
    data=data,
    annotations=annotations,
    attributes=attributes,
    data_params=data_params,
    method_params=method_params,
)