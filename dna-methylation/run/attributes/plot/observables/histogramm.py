import pydnameth as pdm

target = 'age'

data = pdm.Data(
    name='cpg_beta',
    type=pdm.DataType.attributes,
    path='',
    base='GSE40279'
)

setup = pdm.Setup(
    experiment=pdm.Experiment.plot,
    task=pdm.Task.observables,
    method=pdm.Method.histogram,
    params={}
)

annotations = pdm.Annotations(
    name='annotations',
    exclude=pdm.CommonTypes.none.value,
    cross_reactive=pdm.CrossReactive.exclude.value,
    snp=pdm.SNP.exclude.value,
    chr=pdm.Chromosome.non_gender.value,
    gene_region=pdm.GeneRegion.yes.value,
    geo=pdm.CommonTypes.any.value,
    probe_class=pdm.CommonTypes.any.value
)

observables = pdm.Observables(
    file_name='observables',
    types={'gender': 'vs'}
)

cells = pdm.Cells(
    file_name='cells',
    types=pdm.CommonTypes.any.value
)

attributes = pdm.Attributes(
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
    target=target
)

configs_primary = []
for observable_type in observables_types:

    observables_primary = pdm.Observables(
        file_name='observables',
        types=observable_type
    )

    attributes_primary = pdm.Attributes(
        observables=observables_primary,
        cells=cells
    )

    config_primary = pdm.Config(
        data=data,
        setup=setup,
        annotations=annotations,
        attributes=attributes_primary,
        target=target
    )

    configs_primary.append(config_primary)

pdm.plot(config, configs_primary)
