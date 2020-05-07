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

target_ss = 'gender'
target_ar = 'age'

data_params_ss = get_data_params(data.base)
if data.base == 'liver':
    data_params_ss['observables'] = ['age']
else:
    data_params_ss['cells'] = ['Bcell', 'CD4T', 'CD8T', 'Gran', 'NK']
    data_params_ss['observables'] = ['age']

data_params_ar = get_data_params(data.base)
if data.base == 'liver':
    data_params_ar['observables'] = ['gender']
else:
    data_params_ar['cells'] = ['Bcell', 'CD4T', 'CD8T', 'Gran', 'NK']
    data_params_ar['observables'] = ['gender']

pdm.residuals_table_approach_3(
    data,
    annotations,
    attributes,
    target_ss,
    target_ar,
    data_params_ss,
    data_params_ar
)
