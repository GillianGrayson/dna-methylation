import pydnameth as pdm

data = pdm.Data(
    name='cpg_beta',
    type=pdm.DataType.cpg,
    path='',
    base='GSE87571'
)

setup_primary = pdm.Setup(
    experiment=pdm.Experiment.base,
    task=pdm.Task.table,
    method=pdm.Method.variance_linreg,
    params={}
)

setup = pdm.Setup(
    experiment=pdm.Experiment.advanced,
    task=pdm.Task.table,
    method=pdm.Method.polygon,
    params={'method_primary': setup_primary.method}
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

config = pdm.Config(
    data=data,
    setup=setup,
    annotations=annotations,
    attributes=attributes
)

observables_types_primary = [
    {'gender': 'F'},
    {'gender': 'M'},
]

configs_primary = []

for observable_type in observables_types_primary:

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
        setup=setup_primary,
        annotations=annotations,
        attributes=attributes_primary,
    )

    configs_primary.append(config_primary)

pdm.run(config, configs_primary)
