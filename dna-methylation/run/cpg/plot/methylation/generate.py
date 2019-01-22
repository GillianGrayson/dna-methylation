from library.model.main import *


target = 'age'

data = Data(
    name='cpg_beta',
    type=DataType.cpg,
    path='',
    base='EPIC'
)

setup_primary = Setup(
    experiment=Experiment.base,
    task=Task.table,
    method=Method.linreg,
    params={}
)

setup = Setup(
    experiment=Experiment.plot,
    task=Task.methylation,
    method=Method.scatter,
    params={'item': '',
            'method': setup_primary.method.value}
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
    {'gender': 'F'},
    {'gender': 'M'},
]

f = open('cpgs.txt', 'r')
cpgs = f.read().splitlines()

config = Config(
    data=data,
    setup=setup,
    annotations=annotations,
    attributes=attributes,
    target=target
)


for cpg in cpgs:

    config.setup.params['item'] = cpg

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
            setup=setup_primary,
            annotations=annotations,
            attributes=attributes_primary,
            target=target
        )

        configs_primary.append(config_primary)

    plot_experiment(config, configs_primary)

