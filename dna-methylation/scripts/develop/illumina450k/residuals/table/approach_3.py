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

observables = pdm.Observables(
    name='observables',
    types={}
)

attributes = pdm.Attributes(
    target='',
    observables=observables,
    cells=cells
)

target_common = 'gender'
data_params_common = get_data_params(data.base)
data_params_common['cells'] = ['CD8T', 'CD4T', 'NK', 'Bcell', 'Gran']
data_params_common['observables'] = ['age']

target_separated = 'age'
data_params_separated = get_data_params(data.base)
data_params_separated['cells'] = ['CD8T', 'CD4T', 'NK', 'Bcell', 'Gran']
data_params_separated['observables'] = ['gender']

observables_list = get_observables_list(data.base)

pdm.residuals_table_approach_3(
    data,
    annotations,
    attributes,
    observables_list,
    target_common,
    target_separated,
    data_params_common,
    data_params_separated
)
