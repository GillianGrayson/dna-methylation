import pydnameth as pdm
from scripts.develop.routines import *


data = pdm.Data(
    #path='E:/YandexDisk/Work/pydnameth',
    #base='liver'
    # path='',
    path='E:/YandexDisk/Work/pydnameth/tissues/brain(DLPFC)',
    # base='GSE87571'
    base='GSE74193'
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
    #name='observables',
    name='observables_part(control)',
    types={}
    #types={'group': 'Control'}
)

attributes = pdm.Attributes(
    target='',
    observables=observables,
    cells=cells
)

target_ss = 'sex'
target_ar = 'age'

data_params_ss = get_data_params(data.base)
if data.base == 'liver':
    data_params_ss['observables'] = ['age']
elif data.base == 'GSE74193':
    data_params_ss['cells'] = ['propNeuron']
    data_params_ss['observables'] = ['age']
elif data.base == 'GSE61446':
    data_params_ss['observables'] = ['age']
else:
    data_params_ss['cells'] = ['Bcell', 'CD4T', 'CD8T', 'Gran', 'NK']
    data_params_ss['observables'] = ['age']

data_params_ar = get_data_params(data.base)
if data.base == 'liver':
    data_params_ar['observables'] = ['gender']
elif data.base == 'GSE74193':
    data_params_ar['cells'] = ['propNeuron']
    data_params_ar['observables'] = ['sex']
elif data.base == 'GSE61446':
    data_params_ar['observables'] = ['sex']
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
