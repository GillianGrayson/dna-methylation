import pydnameth as pdm


data = pdm.Data(
    path='',
    base='unn_epic'
)

data_params = {
    'part': 'v1',
    'config': '0.01_0.10_0.10',
    'norm': 'fun',

}

chip_type = '850k'
fn = 'observables_part(v1)'

pdm.betas_horvath_calculator_create_regular(
    chip_type=chip_type,
    observables_fn=fn,
    data=data,
    data_params=data_params
)
