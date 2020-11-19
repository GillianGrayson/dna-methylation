import pydnameth as pdm
from scripts.develop.routines import *

data = pdm.Data(
    path='',
    base='unn_epic'
)

#data_params = get_data_params(data.base)
data_params = {
    'norm': 'fun',
    'part': 'wo_noIntensity_detP',
}

fn = 'observables_part(wo_noIntensity_detP)'

pdm.betas_horvath_calculator_create_regular(
    fn,
    data=data,
    data_params=data_params
)
