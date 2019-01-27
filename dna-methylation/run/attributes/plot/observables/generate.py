from library.model.main import *

target = 'age'

data = Data(
    name='cpg_beta',
    type=DataType.attributes,
    path='',
    base='GSE40279'
)

setup = Setup(
    experiment=Experiment.plot,
    task=Task.observables,
    method=Method.histogram,
    params={}
)

annotations = Annotations(
    name='annotations',
    exclude=CommonTypes.none.value,
    cross_reactive=CrossReactive.exclude.value,
    snp=SNP.exclude.value,
    chr=Chromosome.non_gender.value,
    gene_region=GeneRegion.yes.value,
    geo=CommonTypes.any.value,
    probe_class=CommonTypes.any.value
)

observables = Observables(
    file_name='observables',
    types={'gender': 'vs'}
)

cells = Cells(
    file_name='cells',
    types=CommonTypes.any.value
)

attributes = Attributes(
    observables=observables,
    cells=cells
)

observables_types = [
    {'gender': 'any'},
    {'gender': 'F'},
    {'gender': 'M'},
]

config = Config(
    data=data,
    setup=setup,
    annotations=annotations,
    attributes=attributes,
    target=target
)

configs_primary = []
for observable_type in observables_types:

    observables_primary = Observables(
        file_name='observables',
        types=observable_type
    )

    attributes_primary = Attributes(
        observables=observables_primary,
        cells=cells
    )

    config_primary = Config(
        data=data,
        setup=setup,
        annotations=annotations,
        attributes=attributes_primary,
        target=target
    )

    configs_primary.append(config_primary)

plot_experiment(config, configs_primary)

