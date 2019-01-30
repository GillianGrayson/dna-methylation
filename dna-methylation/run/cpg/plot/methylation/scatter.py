import pydnameth as dm

data = dm.Data(
    name='cpg_beta',
    type=dm.DataType.cpg,
    path='',
    base='EPIC'
)

setup_primary = dm.Setup(
    experiment=dm.Experiment.base,
    task=dm.Task.table,
    method=dm.Method.variance_linreg,
    params={}
)

setup = dm.Setup(
    experiment=dm.Experiment.plot,
    task=dm.Task.methylation,
    method=dm.Method.scatter,
    params={'item': '',
            'method': setup_primary.method.value}
)

annotations = dm.Annotations(
    name='annotations',
    exclude=dm.CommonTypes.none.value,
    cross_reactive=dm.CrossReactive.exclude.value,
    snp=dm.SNP.exclude.value,
    chr=dm.Chromosome.non_gender.value,
    gene_region=dm.GeneRegion.yes.value,
    geo=dm.CommonTypes.any.value,
    probe_class=dm.CommonTypes.any.value
)

observables = dm.Observables(
    file_name='observables',
    types={'gender': 'vs'}
)

cells = dm.Cells(
    file_name='cells',
    types=dm.CommonTypes.any.value
)

attributes = dm.Attributes(
    target='age',
    observables=observables,
    cells=cells
)

observables_types = [
    {'gender': 'F'},
    {'gender': 'M'},
]

f = open('cpgs.txt', 'r')
cpgs = f.read().splitlines()

config = dm.Config(
    data=data,
    setup=setup,
    annotations=annotations,
    attributes=attributes,
)

for cpg in cpgs:

    config.setup.params['item'] = cpg

    configs_primary = []
    for observable_type in observables_types:

        observables_primary = dm.Observables(
            file_name='observables',
            types=observable_type
        )

        attributes_primary = dm.Attributes(
            target='age',
            observables=observables_primary,
            cells=cells
        )

        config_primary = dm.Config(
            data=data,
            setup=setup_primary,
            annotations=annotations,
            attributes=attributes_primary
        )

        configs_primary.append(config_primary)

    dm.plot(config, configs_primary)

