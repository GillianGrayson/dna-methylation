import plotly.graph_objs as go
import plotly
import plotly.io as pio
import colorlover as cl


def save_figure(fn, fig):
    plotly.offline.plot(fig, filename=fn + '.html', auto_open=False, show_link=True)
    pio.write_image(fig, fn + '.png')
    pio.write_image(fig, fn + '.pdf')


trace0 = go.Scatter(
    x=[0.6, 0.7, 1.6, 2.85, 0.8, 1.9, 2.7, 1.45, 2.9, 2.15, 1.55, 2.73, 2.27, 2.2, 2.2],
    y=[-0.1, 1.1, 2.0, 1.8, 0.6, -0.2, 0.0, 1.25, 0.9, 1.9, 0.55, 0.45, 0.02, 1.2, 0.5],
    text=['GSE40279<br>1', 'GSE87571<br>2', 'EPIC<br>3', 'GSE55763<br>4', '12', '13', '14', '23', '24', '34', '123', '124', '134', '234', '1234'],
    mode='text',
    textfont=dict(
        color='black',
        size=33,
        family='Arail',
    )
)

data = [trace0]

colors = cl.scales['8']['qual']['Dark2'][0:4]
coordinates = [color[4:-1].split(',') for color in colors]
colors_transparent = ['rgba(' + ','.join(coordinate) + ',' + str(0.9) + ')' for coordinate in coordinates]

layout = {
    'xaxis': {
        'showticklabels': False,
        'showgrid': False,
        'zeroline': False,
        'range': [-0.05, 3.3]
    },
    'yaxis': {
        'showticklabels': False,
        'showgrid': False,
        'zeroline': False,
        'range': [-0.55, 3.05]
    },
    'shapes': [
        {
            'opacity': 0.5,
            'xref': 'x',
            'yref': 'y',
            'fillcolor': colors[0],
            'x0': 0,
            'y0': -0.5,
            'x1': 3,
            'y1': 1.0,
            'type': 'circle',
            'line': {
                'color': 'black'
            },
        },
        {
            'opacity': 0.5,
            'xref': 'x',
            'yref': 'y',
            'fillcolor': colors[1],
            'x0': 0.2,
            'y0': 0.1,
            'x1': 3.2,
            'y1': 1.6,
            'type': 'circle',
            'line': {
                'color': 'black',
            },
        },
{
            'opacity': 0.5,
            'xref': 'x',
            'yref': 'y',
            'fillcolor': colors[3],
            'x0': 1.15,
            'y0': -0.45,
            'x1': 2.65,
            'y1': 2.55,
            'type': 'circle',
            'line': {
                'color': 'black'
            },
        },
        {
            'opacity': 0.5,
            'xref': 'x',
            'yref': 'y',
            'fillcolor': colors[2],
            'x0': 1.75,
            'y0': -0.25,
            'x1': 3.25,
            'y1': 2.75,
            'type': 'circle',
            'line': {
                'color': 'black'
            },
        },
    ],
    'margin': {
        'l': 10,
        'r': 10,
        'b': 10,
        't': 10,
    },
    'height': 1000,
    'width': 1000,
}
fig = {
    'data': data,
    'layout': layout,
}
save_figure('venn4', fig)
