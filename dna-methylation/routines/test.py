import plotly.graph_objs as go
import plotly
import plotly.io as pio
import colorlover as cl

def save_figure(fn, fig):
    plotly.offline.plot(fig, filename=fn + '.html', auto_open=False, show_link=True)
    pio.write_image(fig, fn + '.png')
    pio.write_image(fig, fn + '.pdf')

import plotly.plotly as py
import plotly.graph_objs as go

trace1 = go.Scatter(
    x=[-1, 2, 3],
    y=[-2, 3, 4],
    xaxis = 'x',
    yaxis = 'y'
)
trace2 = go.Scatter(
    x=[20, 30, 40],
    y=[5, 5, 5],
    xaxis='x2',
    yaxis='y'
)
trace3 = go.Scatter(
    x=[2, 3, 4],
    y=[600, 700, 800],
    xaxis='x',
    yaxis='y2'
)
trace4 = go.Scatter(
    x=[40, 50, 60],
    y=[700, 800, 900],
    xaxis='x2',
    yaxis='y2'
)
data = [trace1, trace2, trace3, trace4]
layout = {}
layout['showlegend'] = False
layout['xaxis'] = {}
layout['xaxis']['domain'] = [0, 0.45]
layout['xaxis']['zeroline'] = False
layout['xaxis']['showgrid'] = True
layout['xaxis']['showline'] = True
layout['xaxis']['mirror'] = 'allticks'

layout['yaxis'] = {}
layout['yaxis']['domain'] = [0, 0.45]
layout['yaxis']['zeroline'] = False
layout['yaxis']['showgrid'] = True
layout['yaxis']['showline'] = True
layout['yaxis']['mirror'] = 'allticks'

layout['xaxis2'] = {}
layout['xaxis2']['domain'] = [0.55, 1]
layout['xaxis2']['zeroline'] = False
layout['xaxis2']['showgrid'] = True
layout['xaxis2']['showline'] = True
layout['xaxis2']['mirror'] = 'allticks'

layout['yaxis2'] = {}
layout['yaxis2']['domain'] = [0.55, 1]
layout['yaxis2']['zeroline'] = False
layout['yaxis2']['showgrid'] = True
layout['yaxis2']['showline'] = True
layout['yaxis2']['mirror'] = 'allticks'


fig = go.Figure(data=data, layout=layout)

save_figure('tmp', fig)