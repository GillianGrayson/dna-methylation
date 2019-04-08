import plotly.plotly as py
import plotly.graph_objs as go
import plotly
import plotly.io as pio
import colorlover as cl
from collections import defaultdict
from csv import DictReader

def save_figure(fn, fig):
    plotly.offline.plot(fig, filename=fn + '.html', auto_open=False, show_link=True)
    pio.write_image(fig, fn + '.png')
    pio.write_image(fig, fn + '.pdf')

fn = "C:/Users/user/Google Drive/mlmg/draft/tests/GSE87571/fisher_table_Relation_to_UCSC_CpG_Island.csv"

table_dict = defaultdict(list)
with open(fn, 'r') as f:
    reader = DictReader(f)
    for row in reader:
        for col, dat in row.items():
            table_dict[col].append(dat)

#x_data = [('chr' + str(x)) for x in table_dict['CHR']]
x_data = table_dict['Relation_to_UCSC_CpG_Island']
y_data = list(map(float, table_dict['OR']))

less_ids = [id for id in range(0, len(y_data)) if y_data[id] < 1]
more_ids = [id for id in range(0, len(y_data)) if y_data[id] >= 1]

traces = []
for id in range(0, len(y_data)):
    if y_data[id] < 1.0:
        trace = go.Bar(
            x=[x_data[id]],
            y=[y_data[id]],
            base=[1.0 - y_data[id]],
            marker=dict(
                color='rgba(55, 128, 191, 0.7)',
                line=dict(
                    color='rgba(55, 128, 191, 1.0)',
                    width=2,
                )
            )
        )
    else:
        trace = go.Bar(
            x=[x_data[id]],
            y=[y_data[id] - 1.0],
            base=[1.0],
            marker=dict(
                color='rgba(219, 64, 82, 0.7)',
                line=dict(
                    color='rgba(219, 64, 82, 1.0)',
                    width=2,
                )
            )
        )
    traces.append(trace)

layout = go.Layout(
    showlegend=False,
    yaxis=dict(
        title='Odds ratio',
        type='log',
        autorange=True,
        showgrid=True,
        showline=True,
        mirror='ticks',
        titlefont=dict(
            family='Arial',
            size=33,
            color='black'
        ),
        showticklabels=True,
        tickangle=0,
        tickfont=dict(
            family='Arial',
            size=30,
            color='black'
        ),
        exponentformat='e',
        showexponent='all',
        #tickvals=[0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 0.8, 1, 2, 5, 10],
        #ticktext=['One', 'Three', 'Five', 'Seven', 'Nine', 'Eleven']
    ),
    xaxis=dict(
        autorange=True,
        showgrid=True,
        showline=True,
        mirror='ticks',
        tickangle=90,
        titlefont=dict(
            family='Arial',
            size=20,
            color='black'
        ),
        showticklabels=True,
        tickfont=dict(
            family='Arial',
            size=20,
            color='black'
        ),
        exponentformat='e',
        showexponent='all',
    ),
    autosize=True,
    margin=go.layout.Margin(
        l=120,
        r=20,
        b=120,
        t=20,
        pad=0
    ),
    barmode='overlay',
)

fig = go.Figure(data=traces, layout=layout)
#py.plot(fig, filename='waterfall-bar-profit')

save_figure('barplot', fig)