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

cells = pdm.Cells(
    name='cells',
    types='any'
)

obs_list = [
    {'gender': 'F'},
    {'gender': 'M'}
]

for obs in obs_list:

    observables = pdm.Observables(
        name='observables',
        types=obs
    )

    attributes = pdm.Attributes(
        target='age',
        observables=observables,
        cells=cells
    )

    pdm.betas_clock_linreg_dev(
        data=data,
        annotations=annotations,
        attributes=attributes,
        method_params={
            'type': 'all',
            'part': 0.25,
            'size': 100,
            'runs': 100,
        }
    )
