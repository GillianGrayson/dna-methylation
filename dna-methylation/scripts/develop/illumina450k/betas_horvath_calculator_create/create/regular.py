import pydnameth as pdm
from scripts.develop.routines import *

data = pdm.Data(
    path='E:/YandexDisk/Work/pydnameth/script_datasets/GPL13534/filtered/brain(DLPFC)',
    base='GSE74193'
)

data_params = {
    'norm': 'fun',
    'part': 'control',
}

chip_type = '450k'
fn = 'observables_part(control)'

pdm.betas_horvath_calculator_create_regular(
    chip_type=chip_type,
    observables_fn=fn,
    data=data,
    data_params=data_params
)
