import pydnameth as pdm

data = pdm.Data(
    name='cpg_beta',
    type=pdm.DataType.attributes,
    path='',
    base='EPIC'
)

setup = pdm.Setup(
    experiment=pdm.Experiment.plot,
    task=pdm.Task.observables,
    method=pdm.Method.histogram,
    params={}
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

observables = pdm.Observables(
    name='observables',
    types={'gender': 'vs'}
)

cells = pdm.Cells(
    name='cells',
    types='any'
)

attributes = pdm.Attributes(
    target='age',
    observables=observables,
    cells=cells
)

observables_types = [
    {'gender': 'any'},
    {'gender': 'F'},
    {'gender': 'M'},
]

config = pdm.Config(
    data=data,
    setup=setup,
    annotations=annotations,
    attributes=attributes,
)

configs_primary = []
for observable_type in observables_types:

    observables_primary = pdm.Observables(
        name='observables',
        types=observable_type
    )

    attributes_primary = pdm.Attributes(
        target='age',
        observables=observables_primary,
        cells=cells
    )

    config_primary = pdm.Config(
        data=data,
        setup=setup,
        annotations=annotations,
        attributes=attributes_primary,
    )

    configs_primary.append(config_primary)

pdm.run(config, configs_primary)

