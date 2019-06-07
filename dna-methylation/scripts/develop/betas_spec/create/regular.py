import pydnameth as pdm

data = pdm.Data(
    path='',
    base='GSE55763'
)

data_params = {'file': 'cpgs_variance.txt'}

if data.base == 'GSE55763':
    observables = pdm.Observables(
        name='observables',
        types={}
        #types={'is_duplicate': '0', 'age': (35, 100)}
    )
else:
    observables = pdm.Observables(
        name='observables',
        types={}
    )

pdm.betas_spec_create_regular(data, data_params, observables)
