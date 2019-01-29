import pydnameth as pdm


target = 'age'

data = pdm.Data(
    name='cpg_beta',
    type=pdm.DataType.cpg,
    path='',
    base='GSE87571'
)

setup_primary = pdm.Setup(
    experiment=pdm.Experiment.base,
    task=pdm.Task.table,
    method=pdm.Method.linreg,
    params={}
)

setup = pdm.Setup(
    experiment=pdm.Experiment.advanced,
    task=pdm.Task.clock,
    method=pdm.Method.linreg,
    params={
        'part': 0.25,
        'type': pdm.ClockExogType.all.value,
        'exogs': 100,
        'combs': 100,
        'runs': 100
    }
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
    types={}
)

cells = pdm.Cells(
    file_name='cells',
    types=pdm.CommonTypes.any.value
)

attributes = pdm.Attributes(
    observables=observables,
    cells=cells
)

observables_types_primary = [
    {'gender': 'F'},
    {'gender': 'M'},
    {'gender': pdm.CommonTypes.any.value}
]

for observable_type in observables_types_primary:

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
        setup=setup_primary,
        annotations=annotations,
        attributes=attributes_primary,
        target=target
    )

    config = pdm.Config(
        data=data,
        setup=setup,
        annotations=annotations,
        attributes=attributes_primary,
        target=target
    )

    pdm.advanced(config, [config_primary])
