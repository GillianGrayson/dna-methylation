from source.config.data.data import *
from source.config.setup.setup import *
from source.config.annotations.annotations import *
from source.config.attributes.attributes import *
from source.config.config import *
from source.infrastucture.save.figure import *
from source.infrastucture.load.cpg_data import *
import plotly.graph_objs as go
import colorlover as cl
from source.infrastucture.load.table import *


def add_cpg_scatter(config_from, config_to, cpg, color_id, plot_data):
    x = config_to.attributes_dict[config_to.target]
    betas = load_betas(config_to)
    cpg_row_dict = config_to.cpg_row_dict
    row_id = cpg_row_dict[cpg]
    y = betas[row_id]

    scatter = go.Scatter(
        x=x,
        y=y,
        name='_'.join([key + '(' + value + ')' for key, value in config_to.attributes.observables.types.items()]),
        mode='markers',
        marker=dict(
            opacity=0.75,
            size=15,
            color=cl.scales['8']['qual']['Set1'][color_id],
            line=dict(width=2)
        ),
    )
    plot_data.append(scatter)

    if not bool(config_to.setup.params):
        config_to.setup.params = {
            'method': Method.linreg.value,
            'details': 0
        }

    if config_to.setup.params['details'] > 0 and bool(config_from.setup.params):
        if config_to.setup.params['method'] == Method.linreg.value:
            table = load_table_dict(config_from)
            cpgs = table['id']
            cpg_id = cpgs.index(cpg)
            intercept = table['intercept'][cpg_id]
            intercept_std = table['intercept_std'][cpg_id]
            slope = table['slope'][cpg_id]
            slope_std = table['slope_std'][cpg_id]
            x_min = np.min(x)
            x_max = np.max(x)
            y_min = slope * x_min + intercept
            y_max = slope * x_max + intercept

            slope_tmp = slope + 3.0 * slope_std
            y_tmp =  slope_tmp * x_max + intercept

            y_diff = 3.0 * np.abs(intercept_std) + np.abs(y_tmp - y_max)

            y_min_up = y_min + y_diff
            y_min_down = y_min - y_diff

            y_max_up = y_max + y_diff
            y_max_down = y_max - y_diff

            if config_to.setup.params['details'] >= 1:
                scatter = go.Scatter(
                    x=[x_min, x_max],
                    y=[y_min, y_max],
                    mode='lines',
                    marker=dict(
                        color=cl.scales['8']['qual']['Set1'][color_id],
                        line=dict(width=8)
                    ),
                    showlegend=False
                )
                plot_data.append(scatter)

            if config_to.setup.params['details'] >= 2:
                scatter = go.Scatter(
                    x=[x_min, x_max, x_max, x_min, x_min],
                    y=[y_min_down, y_max_down, y_max_up, y_min_up, y_min_down],
                    fill='tozerox',
                    mode='lines',
                    marker=dict(
                        opacity=0.75,
                        color=cl.scales['8']['qual']['Set1'][color_id],
                        line=dict(width=4)
                    ),
                    showlegend=False
                )
                plot_data.append(scatter)

def plot_cpg_scatter(plot_data, cpg, config):
    genes = config.cpg_gene_dict[cpg]
    layout = go.Layout(
        title=cpg + '(' + ';'.join(genes) + ')',
        autosize=True,
        barmode='overlay',
        legend=dict(
            font=dict(
                family='sans-serif',
                size=16,
            ),
            orientation="h",
            x=0,
            y=1.15,
        ),
        xaxis=dict(
            title=config.target,
            showgrid=True,
            showline=True,
            mirror='ticks',
            titlefont=dict(
                family='Arial, sans-serif',
                size=24,
                color='black'
            ),
            showticklabels=True,
            tickangle=0,
            tickfont=dict(
                family='Old Standard TT, serif',
                size=20,
                color='black'
            ),
            exponentformat='e',
            showexponent='all'
        ),
        yaxis=dict(
            title='beta',
            showgrid=True,
            showline=True,
            mirror='ticks',
            titlefont=dict(
                family='Arial, sans-serif',
                size=24,
                color='black'
            ),
            showticklabels=True,
            tickangle=0,
            tickfont=dict(
                family='Old Standard TT, serif',
                size=20,
                color='black'
            ),
            exponentformat='e',
            showexponent='all'
        ),

    )
    fig = go.Figure(data=plot_data, layout=layout)
    save_figure(config, fig, cpg)

cpgs = [
    'cg01620164',
    'cg23256579',
    'cg27615582'
]

target = 'age'

data = Data(
    name='cpg_beta',
    type=DataType.cpg,
    path='',
    base='GSE87571'
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
    task=Task.plot,
    method=Method.scatter,
    params={
        'method': setup_from.method.value,
        'details': 2
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
    {'gender': 'F'},
    {'gender': 'M'},
]

for cpg in cpgs:
    print(cpg)
    plot_data = []
    for obs_id in range(0, len(obs_list)):
        obs = obs_list[obs_id]
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

        add_cpg_scatter(config_from, config_to, cpg, obs_id, plot_data)

    attributes.observables.types = {'gender': CommonTypes.vs.value}
    config_to = Config(
        data=data,
        setup=setup_to,
        annotations=annotations,
        attributes=attributes,
        target=target
    )
    plot_cpg_scatter(plot_data, cpg, config_to)
