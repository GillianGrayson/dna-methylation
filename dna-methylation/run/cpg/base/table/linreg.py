import pydnameth as pdm

data = pdm.Data(
    name='cpg_beta',
    type=pdm.DataType.cpg,
    path='',
    base='GSE87571'
)

setup = pdm.Setup(
    experiment=pdm.Experiment.base,
    task=pdm.Task.table,
    method=pdm.Method.linreg,
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
    types={
        'gender': pdm.CommonTypes.any.value
    }
)

cells = pdm.Cells(
    file_name='cells',
    types=pdm.CommonTypes.any.value
)

attributes = pdm.Attributes(
    target='age',
    observables=observables,
    cells=cells
)

obs_list = [
    {'gender': 'F'},
    {'gender': 'M'},
    {'gender': pdm.CommonTypes.any.value}
]

for obs in obs_list:
    attributes.observables.types = obs

    config = pdm.Config(
        data=data,
        setup=setup,
        annotations=annotations,
        attributes=attributes
    )

    pdm.base(config)
