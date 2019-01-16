from source.config.data.data import *
from source.config.setup.setup import *
from source.config.annotations.annotations import *
from source.config.attributes.attributes import *
from source.config.config import *
from source.scripts.cpg.advanced.clock.linreg.processing import *
from source.setup.advanced.clock.clock import ClockExogType


def generate_clock(config_from, config_to):
    if config_to.setup.method == Method.linreg:
        generate_clock_linreg(config_from, config_to)

target = 'age'

data = Data(
    name='cpg_beta',
    type=DataType.cpg,
    path='',
    base='GSE40279'
)

setup_from = Setup(
    experiment=Experiment.base,
    task=Task.table,
    method=Method.linreg,
    params={
        'out_limit': 0.0,
        'out_sigma': 0.0
    }
)

setup_to = Setup(
    experiment=Experiment.advanced,
    task=Task.clock,
    method=Method.linreg,
    params={
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

    config_from = Config(
        data=data,
        setup=setup_from,
        annotations=annotations,
        attributes=attributes,
        target=target
    )

    config_to = Config(
        data=data,
        setup=setup_to,
        annotations=annotations,
        attributes=attributes,
        target=target
    )

    generate_clock(config_from, config_to)
