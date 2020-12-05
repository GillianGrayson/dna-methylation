import pydnameth as pdm
from scripts.develop.routines import *


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

target = 'age'
attributes = pdm.Attributes(
    target=target,
    observables=observables,
    cells=cells
)

data_params = {
}

method_params = {
    'formula': 'cpg ~ gender*age + Bcell + CD4T + CD8T + Gran + NK',
}

pdm.betas_table_formula_new(
    data=data,
    annotations=annotations,
    attributes=attributes,
    data_params=data_params,
    method_params=method_params,
)