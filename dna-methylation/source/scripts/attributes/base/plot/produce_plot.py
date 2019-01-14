from source.config.data.data import *
from source.config.setup.setup import *
from source.config.annotations.annotations import *
from source.config.attributes.attributes import *
from source.config.config import *
from source.scripts.attributes.base.plot.histogram.processing import *


target = 'age'

data = Data(
    name='cpg_beta',
    type=DataType.attributes,
    path='',
    base='GSE87571'
)

setup = Setup(
    experiment=Experiment.base,
    task=Task.plot,
    method=Method.histogram,
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
        'gender': CommonTypes.all.value
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
    {'gender': CommonTypes.any.value},
    {'gender': 'F'},
    {'gender': 'M'},
]
plot_data = []

for obs in obs_list:
    attributes.observables.types = obs

    config = Config(
        data=data,
        setup=setup,
        annotations=annotations,
        attributes=attributes,
        target=target
    )

    add_attributes_histogram(config, plot_data)

attributes.observables.types = {'gender': CommonTypes.all.value}
save_config = config = Config(
    data=data,
    setup=setup,
    annotations=annotations,
    attributes=attributes,
    target=target
)
plot_attributes_histogram(plot_data, save_config)