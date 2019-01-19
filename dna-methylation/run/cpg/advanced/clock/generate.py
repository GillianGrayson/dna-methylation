from library.model.main import *


target = 'age'

data = Data(
    name='cpg_beta',
    type=DataType.cpg,
    path='',
    base='GSE87571'
)

setup_primary = Setup(
    experiment=Experiment.base,
    task=Task.table,
    method=Method.linreg,
    params={}
)

setup = Setup(
    experiment=Experiment.advanced,
    task=Task.clock,
    method=Method.linreg,
    params={
        'part': 0.25,
        'type': ClockExogType.all.value,
        'exogs': 100,
        'combs': 100,
        'runs': 100
    }
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
    types={}
)

cells = Cells(
    file_name='cells',
    types=CommonTypes.any.value
)

attributes = Attributes(
    observables=observables,
    cells=cells
)

obs_list = [
    {'gender': 'F'},
    {'gender': 'M'},
    {'gender': CommonTypes.any.value}
]

for obs in obs_list:
    attributes.observables.types = obs

    config_primary = Config(
        data=data,
        setup=setup_primary,
        annotations=annotations,
        attributes=attributes,
        target=target
    )

    config = Config(
        data=data,
        setup=setup,
        annotations=annotations,
        attributes=attributes,
        target=target
    )

    advanced_experiment(config, [config_primary])
