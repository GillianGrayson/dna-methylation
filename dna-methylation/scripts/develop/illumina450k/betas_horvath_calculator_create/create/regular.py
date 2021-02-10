import pydnameth as pdm
from scripts.develop.routines import *

data = pdm.Data(
    path='E:/YandexDisk/Work/pydnameth/script_datasets/GPL13534/filtered/blood(whole)',
    base='GSE87571'
)

data_params = {
    'norm': 'fun',
    'part': 'wo_missedFeatures',
}

chip_type = '450k'
fn = 'observables_part(wo_missedFeatures)'

pdm.betas_horvath_calculator_create_regular(
    chip_type=chip_type,
    observables_fn=fn,
    data=data,
    data_params=data_params
)
