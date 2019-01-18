import plotly.graph_objs as go
import colorlover as cl
from lib.infrastucture.save.figure import *


def add_attributes_histogram(config, plot_data):
    target = config.attributes_dict[config.target]
    histogram = go.Histogram(
        x=target,
        name='_'.join([key + '(' + value + ')' for key, value in config.attributes.observables.types.items()]),
        xbins=dict(
            start=min(target) - 0.5,
            end=max(target) + 0.5,
            size=1.0
        ),
        marker=dict(opacity=0.75),
    )
    plot_data.append(histogram)


def plot_attributes_histogram(plot_data, config):
    layout = go.Layout(
        autosize=True,
        barmode='overlay',
        colorway=cl.scales['8']['qual']['Set1'],
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
            title='count',
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
    save_figure(config, fig)
