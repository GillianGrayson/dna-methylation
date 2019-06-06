import pydnameth as pdm

data = pdm.Data(
    path='',
    base='GSE87571'
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

if data.base == 'GSE55763':
    observables_list = [
        {'is_duplicate': '0', 'age': (35, 100)},
    ]
    cells = pdm.Cells(
        name='cells_horvath_calculator',
        types='any'
    )
else:
    observables_list = [
        {},
    ]
    cells = pdm.Cells(
        name='cells',
        types='any'
    )

method_params = {
    'eps': 0.15,
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