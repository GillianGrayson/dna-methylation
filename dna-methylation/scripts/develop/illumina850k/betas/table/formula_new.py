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
    select_dict={
        'CHR': ['-X', '-Y']
    }
)

observables = pdm.Observables(
    name='observables_part(wo_noIntensity_detP)',
    types={}
)

cells = pdm.Cells(
    name='cell_counts_part(wo_noIntensity_detP)',
    types='any'
)

target = 'Sample_Group'
attributes = pdm.Attributes(
    target=target,
    observables=observables,
    cells=cells
)

data_params = {
    'norm': 'fun',
    'part': 'wo_noIntensity_detP',
}

method_params = {
    'formula': 'cpg ~ C(Sample_Group) + C(Sex) + Age + Bcell + CD4T + CD8T + Neu + NK',
}

pdm.betas_table_formula_new(
    data=data,
    annotations=annotations,
    attributes=attributes,
    data_params=data_params,
    method_params=method_params,
)