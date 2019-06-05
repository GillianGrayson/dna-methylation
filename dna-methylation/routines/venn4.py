import plotly.graph_objs as go
import plotly
import plotly.io as pio
import colorlover as cl


def save_figure(fn, fig):
    plotly.offline.plot(fig, filename=fn + '.html', auto_open=False, show_link=True)
    pio.write_image(fig, fn + '.png')
    pio.write_image(fig, fn + '.pdf')


trace0 = go.Scatter(
    x=[0.32, 1.625, 2.95, 1.625, 1.05, 2.2, 2.2, 1.05, 1.1, 1.625, 2.15, 1.625, 1.625],
    y=[1.0, 2.3, 1.0, -0.3, 1.625, 1.625, 0.375, 0.375, 1.0, 1.53, 1.0, 0.47, 1.0],
    #text=['GSE40279<br>3', 'GSE87571<br>262', 'EPIC<br>552', 'GSE55763<br>121', '0', '38', '1', '0', '0', '3', '21', '0', '6'],
    text=['GSE40279<br>6', 'GSE87571<br>243', 'EPIC<br>371', 'GSE55763<br>109', '0', '25', '2', '0', '0', '1', '24', '0', '2'],
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
        'range': [0, 3.25]
    },
    'yaxis': {
        'showticklabels': False,
        'showgrid': False,
        'zeroline': False,
        'range': [-0.625, 2.625]
    },
    'shapes': [
        {
            'opacity': 0.5,
            'xref': 'x',
            'yref': 'y',
            'fillcolor': colors[0],
            'x0': 0,
            'y0': 0,
            'x1': 2,
            'y1': 2,
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
            'x0': 1.25,
            'y0': 0,
            'x1': 3.25,
            'y1': 2,
            'type': 'circle',
            'line': {
                'color': 'black',
            },
        },
        {
            'opacity': 0.5,
            'xref': 'x',
            'yref': 'y',
            'fillcolor': colors[2],
            'x0': 0.625,
            'y0': -0.625,
            'x1': 2.625,
            'y1': 1.375,
            'type': 'circle',
            'line': {
                'color': 'black'
            },
        },
        {
            'opacity': 0.5,
            'xref': 'x',
            'yref': 'y',
            'fillcolor': colors[3],
            'x0': 0.625,
            'y0': 0.625,
            'x1': 2.625,
            'y1': 2.625,
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
