from source.config.data.data import *
from source.config.setup.setup import *
from source.config.annotations.annotations import *
from source.config.attributes.attributes import *
from source.config.config import *
from source.scripts.cpg.base.table.variance_linreg.processing import *
import plotly
import plotly.graph_objs as go


def add_target_histogram(config, plot_data):
    target = config.attributes_dict[config.target]
    histogram = go.Histogram(
        x=target,
        xbins=dict(start=min(target) - 0.5, end=max(target) + 0.5, size=1.0),
        marker=dict(opacity=0.5)
    )
    plot_data.append(histogram)


def plot_target_histogram(plot_data):
    layout = go.Layout(barmode='overlay')
    fig = go.Figure(data=plot_data, layout=layout)
    plotly.offline.plot(fig, filename='target_histogram.html', auto_open=False)


target = 'age'

data = Data(
    name='cpg_beta',
    type=DataType.cpg,
    path='',
    base='GSE87571'
)

setup = Setup(
    experiment=Experiment.base,
    task=Task.plot,
    method=Method.histogram,
    params={
        'color': 0.0,
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

    add_target_histogram(config, plot_data)

plot_target_histogram(plot_data)