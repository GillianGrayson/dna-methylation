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

cells = pdm.Cells(
    name='cells',
    types='any'
)

if data.base == 'GSE55763':
    observables_list = [
        {'gender': 'any', 'is_duplicate': '0'},
    ]
else:
    observables_list = [
        {'gender': 'any'},
    ]

method_params = {
    'eps': 0.2,
    'min_samples_percentage': 1
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

    pdm.betas_table_cluster(
        data=data,
        annotations=annotations,
        attributes=attributes,
        method_params=method_params
    )