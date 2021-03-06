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

cells = pdm.Cells(
    name='cells_horvath_calculator',
    types='any'
)

target = 'gender'
observables_list = [
    {'gender': 'any'},
]
data_params = get_data_params(data.base)


for obs in observables_list:

    observables = pdm.Observables(
        name='observables',
        types=obs
    )

    attributes = pdm.Attributes(
        target=target,
        observables=observables,
        cells=cells
    )

    pdm.betas_table_oma(
        data=data,
        annotations=annotations,
        attributes=attributes
    )