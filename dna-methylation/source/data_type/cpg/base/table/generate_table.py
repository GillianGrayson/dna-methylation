from source.config.data.data import *
from source.config.setup.setup import *
from source.config.annotation.annotation import *
from source.config.attribute.attribute import *
from source.config.config import *
from source.data_type.cpg.base.table.linreg.processing import *
from source.data_type.cpg.base.table.cluster.processing import *
from source.data_type.cpg.base.table.variance_linreg.processing import *


def generate_table(config):
    if config.setup.method == Method.linreg:
        generate_table_linreg(config)
    elif config.setup.method == Method.cluster:
        generate_table_cluster(config)
    elif config.setup.method == Method.variance_linreg:
        generate_table_variance_linreg(config)


data = Data(
    name='cpg_beta',
    type=DataType.cpg,
    path='',
    base=DataBase.GSE87571.value
)

setup = Setup(
    experiment=Experiment.base,
    task=Task.table,
    method=Method.linreg,
    params={},
    suffix='',
)

annotation = Annotation(
    name='annotation',
    exclude=Exclude.cluster.value,
    cross_reactive=CrossReactive.exclude.value,
    snp=SNP.exclude.value,
    chr=Chromosome.non_gender.value,
    gene_region=GeneRegion.yes.value,
    geo=Geo.any.value,
    probe_class=ProbeClass.any.value
)

attribute = Attribute(
    obs={AttributeKey.gender.value:Gender.any.value},
    name='attribute',
    cells=Cells.none.value,
    cells_name='cells',
)
obs_list = [
    {AttributeKey.gender.value: Gender.F.value},
    {AttributeKey.gender.value: Gender.M.value},
    {AttributeKey.gender.value: Gender.any.value}
]

for obs in obs_list:
    attribute.obs = obs

    config = Config(
        data=data,
        setup=setup,
        annotation=annotation,
        attribute=attribute,
        target=AttributeKey.age.value
    )

    generate_table(config)
