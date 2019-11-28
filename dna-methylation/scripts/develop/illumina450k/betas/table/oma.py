import pydnameth as pdm

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

if data.base == 'GSE55763':
    observables_list = [
        {'gender': 'any', 'is_duplicate': '0', 'age': (35, 100)},
    ]
else:
    observables_list = [
        {'gender': 'any'},
    ]

for obs in observables_list:

    observables = pdm.Observables(
        name='observables',
        types=obs
    )

    attributes = pdm.Attributes(
        target='age',
        observables=observables,
        cells=cells
    )

    pdm.betas_table_linreg(
        data=data,
        annotations=annotations,
        attributes=attributes
    )