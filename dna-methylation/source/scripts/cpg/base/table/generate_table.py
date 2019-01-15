from source.config.data.data import *
from source.config.setup.setup import *
from source.config.annotations.annotations import *
from source.config.attributes.attributes import *
from source.config.config import *
from source.scripts.cpg.base.table.linreg.processing import *
from source.scripts.cpg.base.table.cluster.processing import *
from source.scripts.cpg.base.table.variance_linreg.processing import *


def generate_table(config):
    if config.setup.method == Method.linreg:
        generate_table_linreg(config)
    elif config.setup.method == Method.cluster:
        generate_table_cluster(config)
    elif config.setup.method == Method.variance_linreg:
        generate_table_variance_linreg(config)

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
    method=Method.variance_linreg,
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

    generate_table(config)
