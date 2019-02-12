import pydnameth as pdm

data = pdm.Data(
    name='cpg_beta',
    path='',
    base='GSE87571'
)

annotations = pdm.Annotations(
    name='annotations',
    exclude='none',
    cross_reactive='ex',
    snp='ex',
    chr='NS',
    gene_region='yes',
    geo='any',
    probe_class='any'
)

cells = pdm.Cells(
    name='cells',
    types='any'
)

obs_list = [
    {'gender': 'F'},
    {'gender': 'M'},
    {'gender': 'any'}
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

    pdm.cpg_proc_clock_linreg(
        data=data,
        annotations=annotations,
        attributes=attributes,
        params={
            'type': 'all',
            'part': 0.25,
            'size': 100,
            'runs': 100,
        }
    )
