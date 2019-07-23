import pydnameth as pdm

data = pdm.Data(
    path='',
    base='GSE87571_TEST'
)

annotations = pdm.Annotations(
    name='annotations',
    type='450k',
    exclude='bad_cpgs',
    select_dict={
        'CHR': ['-X', '-Y']
    }
)

observables = pdm.Observables(
    name='observables',
    types={}
)

cells = pdm.Cells(
    name='cells_horvath_calculator',
    types='any'
)
data_params = {'cells': ['CD8T', 'CD4T', 'NK', 'Bcell', 'Gran']}

attributes = pdm.Attributes(
    target='age',
    observables=observables,
    cells=cells
)

if data.base == 'GSE55763':
    observables_list = [
        {'gender': 'F', 'is_duplicate': '0', 'age': (35, 100)},
        {'gender': 'M', 'is_duplicate': '0', 'age': (35, 100)}
    ]
elif data.base == 'E-MTAB-7309' or data.base == 'E-MTAB-7309-FILTERED':
    data_params['norm'] = 'quantile'
    observables_list = [
        {'sex': 'female'},
        {'sex': 'male'}
    ]
else:
    observables_list = [
        {'gender': 'F'},
        {'gender': 'M'}
    ]

pdm.residuals_common_table_aggregator_linreg(
    data=data,
    annotations=annotations,
    attributes=attributes,
    observables_list=observables_list,
    data_params=data_params
)