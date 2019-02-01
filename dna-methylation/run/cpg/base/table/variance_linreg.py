import pydnameth as pdm

data = pdm.Data(
    name='cpg_beta',
    type=pdm.DataType.cpg,
    path='',
    base='EPIC'
)

setup = pdm.Setup(
    experiment=pdm.Experiment.base,
    task=pdm.Task.table,
    method=pdm.Method.variance_linreg,
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
    types={
        'gender': 'any'
    }
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

obs_list = [
    {'gender': 'F'},
    {'gender': 'M'},
    {'gender': 'any'}
]

for obs in obs_list:
    attributes.observables.types = obs

    config = pdm.Config(
        data=data,
        setup=setup,
        annotations=annotations,
        attributes=attributes
    )

    pdm.run(config)
