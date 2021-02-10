import pydnameth as pdm


data = pdm.Data(
    path='',
    base='unn_epic'
)

data_params = {
    'part': 'wo_noIntensity_detP',
    'config': '0.01_0.10_0.00',
    'norm': 'fun',

}

chip_type = '850k'
fn = 'observables_part(wo_noIntensity_detP)'

pdm.betas_horvath_calculator_create_regular(
    chip_type=chip_type,
    observables_fn=fn,
    data=data,
    data_params=data_params
)
