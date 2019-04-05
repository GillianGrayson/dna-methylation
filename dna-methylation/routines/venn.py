import plotly.graph_objs as go
import plotly
import plotly.io as pio
import colorlover as cl


def save_figure(fn, fig):
    plotly.offline.plot(fig, filename=fn + '.html', auto_open=False, show_link=True)
    pio.write_image(fig, fn + '.png')
    pio.write_image(fig, fn + '.pdf')


trace0 = go.Scatter(
    x=[0.5, 1.5, 2.5, 1.5, 1.5, 0.87, 2.10],
    y=[0.75, 2.5, 0.75, 0.67, 1.4, 1.67, 1.67],
    text=['GSE40279<br>3', 'EPIC<br>553', 'GSE87571<br>262', '0', '9', '0', '59'],
    mode='text',
    textfont=dict(
        color='black',
        size=33,
        family='Arail',
    )
)

data = [trace0]

colors = cl.scales['8']['qual']['Dark2'][0:3]
coordinates = [color[4:-1].split(',') for color in colors]
colors_transparent = ['rgba(' + ','.join(coordinate) + ',' + str(0.9) + ')' for coordinate in coordinates]

layout = {
    'xaxis': {
        'showticklabels': False,
        'showgrid': False,
        'zeroline': False,
        'range': [0, 3]
    },
    'yaxis': {
        'showticklabels': False,
        'showgrid': False,
        'zeroline': False,
        'range': [0, 3]
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
            'x0': 1,
            'y0': 0,
            'x1': 3,
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
            'x0': 0.5,
            'y0': 1,
            'x1': 2.5,
            'y1': 3,
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
    'height': 800,
    'width': 800,
}
fig = {
    'data': data,
    'layout': layout,
}
save_figure('venn', fig)
