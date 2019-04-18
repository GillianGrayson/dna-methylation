import pydnameth as pdm

data = pdm.Data(
    path='',
    base='EPIC'
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

cells = pdm.Cells(
    name='cells',
    types='any'
)

observables_list = [
    {'gender': 'F'},
    {'gender': 'M'}
]

data_params = {
    'cells': ['B', 'CD4T', 'NK', 'CD8T', 'Gran'],
    'observables': ['age']
}

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

    pdm.residuals_common_table_heteroscedasticity_dev(
        data=data,
        annotations=annotations,
        attributes=attributes,
        data_params=data_params
    )