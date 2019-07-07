import plotly.graph_objs as go
import plotly
import plotly.io as pio
import pandas as pd
import colorlover as cl

def save_figure(fn, fig):
    plotly.offline.plot(fig, filename=fn + '.html', auto_open=False, show_link=True)
    pio.write_image(fig, fn + '.png')
    pio.write_image(fig, fn + '.pdf')

YRI = {
    'long': [4.56611111],
    'lat': [7.46611111],
    'name': 'Yoruba'
}

CHB = {
    'long': [108.94111111],
    'lat': [34.15361111],
    'name': 'Han Chinese'
}

populations = [YRI, CHB]

colors = cl.scales['8']['qual']['Dark2'][0:len(populations)]
coordinates = [color[4:-1].split(',') for color in colors]
colors_transparent = ['rgba(' + ','.join(coordinate) + ',' + str(0.75) + ')' for coordinate in coordinates]

elems = []
for id, population in enumerate(populations):
    elems.append(
        go.Scattergeo(
            lon=population['long'],
            lat=population['lat'],
            name=population['name'],
            hoverinfo='text',
            text=population['name'],
            mode='markers',
            marker=go.scattergeo.Marker(
                size=10,
                color=colors_transparent[id],
                line=go.scattergeo.marker.Line(
                    width=1,
                    color=colors[id]
                )
            )))

    if id > 0:
        elems.append(
        go.Scattergeo(
            lon = (populations[0]['long'][0], population['long'][0]),
            lat = (populations[0]['lat'][0], population['lat'][0]),
            mode = 'lines',
            line = go.scattergeo.Line(
                width = 2,
                color = colors[id],
            )
        ))


layout = go.Layout(
    title = go.layout.Title(
        text = 'Test'
    ),
    showlegend = True,
    geo = go.layout.Geo(
        showland = True,
        landcolor = 'rgb(243, 243, 243)',
        countrycolor = 'rgb(204, 204, 204)',
    ),
)

fig = go.Figure(data=elems , layout=layout)
save_figure('test', fig)
