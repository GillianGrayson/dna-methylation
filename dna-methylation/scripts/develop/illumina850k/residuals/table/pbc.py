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
    name='observables_part(final)',
    types={}
)

cells = pdm.Cells(
    name='cell_counts',
    types='any'
)

target = 'Sample_Group'
attributes = pdm.Attributes(
    target=target,
    observables=observables,
    cells=cells
)

#data_params = get_data_params(data.base)
data_params = {
    'norm': 'fun',
    'part': 'final',
}
data_params['cells'] = ['Bcell', 'CD4T', 'CD8T', 'Neu', 'NK']

pdm.residuals_table_pbc(
    data=data,
    annotations=annotations,
    attributes=attributes,
    data_params=data_params,
)