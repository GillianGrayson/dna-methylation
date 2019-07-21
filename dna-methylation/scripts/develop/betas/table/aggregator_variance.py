import pydnameth as pdm
from scripts.develop.routines import *


data = pdm.Data(
    path='',
    base='GSE87571_TEST'
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

attributes = pdm.Attributes(
    target=target,
    observables=observables,
    cells=cells
)

pdm.betas_table_aggregator_variance(
    data=data,
    annotations=annotations,
    attributes=attributes,
    observables_list=observables_list,
    data_params=data_params
)