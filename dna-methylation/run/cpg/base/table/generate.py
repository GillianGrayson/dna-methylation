from library.config.data.data import *
from library.config.setup.setup import *
from library.config.annotations.annotations import *
from library.config.attributes.attributes import *
from library.config.config import *
from library.model.main import *

target = 'age'

data = Data(
    name='cpg_beta',
    type=DataType.cpg,
    path='',
    base='GSE87571'
)

setup = Setup(
    experiment=Experiment.base,
    task=Task.table,
    method=Method.linreg,
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
    types={
        'gender': CommonTypes.any.value
    }
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

    config = Config(
        data=data,
        setup=setup,
        annotations=annotations,
        attributes=attributes,
        target=target
    )

    base_experiment(config)
