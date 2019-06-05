import pydnameth as pdm

data = pdm.Data(
    path='',
    base='GSE55763'
)

annotations = pdm.Annotations(
    name='annotations',
    exclude='bad_cpgs',
    cross_reactive='any',
    snp='any',
    chr='NS',
    gene_region='any',
    geo='any',
    probe_class='any'
)

observables = pdm.Observables(
    name='observables',
    types={}
)

if data.base == 'GSE55763':
    data_params = None
    observables_list = [
        {'gender': 'F', 'is_duplicate': '0', 'age': (35, 100)},
        {'gender': 'M', 'is_duplicate': '0', 'age': (35, 100)}
    ]
    cells = pdm.Cells(
        name='cells_horvath_calculator',
        types='any'
    )
elif data.base == 'E-MTAB-7309' or data.base == 'E-MTAB-7309-FILTERED':
    data_params = {
        'norm': 'quantile',
    }
    observables_list = [
        {'sex': 'female'},
        {'sex': 'male'}
    ]
    cells = pdm.Cells(
        name='cells_horvath_calculator',
        types='any'
    )
else:
    data_params = None
    observables_list = [
        {'gender': 'F'},
        {'gender': 'M'}
    ]
    cells = pdm.Cells(
        name='cells',
        types='any'
    )

attributes = pdm.Attributes(
    target='age',
    observables=observables,
    cells=cells
)

pdm.betas_table_aggregator_linreg(
    data=data,
    annotations=annotations,
    attributes=attributes,
    observables_list=observables_list,
    data_params=data_params
)