import plotly.graph_objs as go
import colorlover as cl


def get_trace_3(labels):
    trace = go.Scatter(
        x=[0.50, 1.5, 2.50, 0.87, 1.50, 2.10, 1.5],
        y=[0.75, 2.5, 0.75, 1.67, 0.67, 1.67, 1.4],
        text=labels,
        mode='text',
        textfont=dict(
            color='black',
            size=20,
            family='Arail',
        )
    )
    return trace

def get_trace_4(labels):
    trace = go.Scatter(
        x=[0.320, 1.625, 2.950, +1.625, 1.050, 2.200, 2.200, 1.050, 1.100, 1.625, 2.150, 1.625, 1.625],
        y=[1.000, 2.300, 1.000, -0.300, 1.625, 1.625, 0.375, 0.375, 1.000, 1.530, 1.000, 0.470, 1.000],
        text=labels,
        mode='text',
        textfont=dict(
            color='black',
            size=15,
            family='Arail',
        )
    )
    return trace


def get_layout_3():
    colors = cl.scales['8']['qual']['Dark2'][0:4]
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
                'fillcolor': colors[3],
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
                'fillcolor': colors[2],
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
                'fillcolor': colors[1],
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
    return layout

def get_layout_4():
    colors = cl.scales['8']['qual']['Dark2'][0:4]
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

    return layout






