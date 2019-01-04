from source.config.data.data import *
from source.config.setup.setup import *
from source.config.annotation.annotation import *
from source.config.attribute.attribute import *
from source.config.auxillary.clock import *
from source.config.config import *
from source.data_type.cpg.advanced.clock.linreg.processing import *



def generate_clock(config_from, config_to):
    if config_to.setup.method == Method.linreg:
        generate_clock_linreg(config_from, config_to)


data = Data(
    name='cpg_beta',
    type=DataType.cpg,
    path='',
    base=DataBase.GSE87571.value
)

setup_from = Setup(
    experiment=Experiment.base,
    task=Task.table,
    method=Method.linreg,
    params={
        'out_limit': 0.0,
        'out_sigma': 0.0
    },
    suffix='',
)

setup_to = Setup(
    experiment=Experiment.advanced,
    task=Task.clock,
    method=Method.linreg,
    params={
        'exog_type': ClockExogType.all.value,
        'exog_num': 100,
        'exog_num_comb': 100
    },
    suffix='',
)

annotation = Annotation(
    name='annotation',
    exclude=Exclude.none.value,
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

    config_from = Config(
        data=data,
        setup=setup_from,
        annotation=annotation,
        attribute=attribute,
        target=AttributeKey.age.value
    )

    config_to = Config(
        data=data,
        setup=setup_to,
        annotation=annotation,
        attribute=attribute,
        target=AttributeKey.age.value
    )

    generate_clock(config_from, config_to)
