import pandas as pd
import plotly.graph_objs as go
import colorlover as cl
import plotly
import numpy as np

data_path = 'D:/Aaron/Bio/variance/v2/'
data_files = ['R2_mean.csv']

eps = 0.00000001

for data_file in data_files:
    raw_data = pd.read_csv(data_path + data_file)
    column_names = list(raw_data.columns)
    curr_data = []
    curr_plot_data = []
    max_y = -1
    min_y = 1000
    for column_name in column_names:
        curr_data.append(list(raw_data[column_name]))

    for id in range(0, len(curr_data)):
        curr_data[id] = [x for x in curr_data[id] if str(x) != 'nan']

    for id in range(0, len(curr_data)):

        if 'R2' in data_file:
            max_x = 1.0
            min_x = 0.0
        else:
            max_x = np.max([np.max(curr_data[i]) for i in range(0, len(curr_data))])
            min_x = np.min([np.min(curr_data[i]) for i in range(0, len(curr_data))])
        num_bins = 1000
        shift = (max_x - min_x) / num_bins
        x = [(shift / 2) + i * shift for i in range(0, num_bins)]
        y = [0] * num_bins
        num_outliers = 0
        for curr_y in curr_data[id]:
            if 'mean' in data_file:
                curr_y = curr_y / 2
            if curr_y > max_x or curr_y < min_x:
                num_outliers += 1
            else:
                index = int(round((curr_y - min_x) / (max_x - min_x + eps) * num_bins))
                y[index] += 1

        sum_y = sum(y)
        y = [curr_y / (sum_y * shift) for curr_y in y]
        if min(y) < min_y:
            min_y = min(y)
        if max(y) > max_y:
            max_y = max(y)

        # Colors setup
        color = cl.scales['8']['qual']['Set1'][id]
        coordinates = color[4:-1].split(',')
        color_transparent = 'rgba(' + ','.join(coordinates) + ',' + str(0.1) + ')'
        color_border = 'rgba(' + ','.join(coordinates) + ',' + str(0.8) + ')'

        scatter = go.Scatter(
            x=x,
            y=y,
            name=column_names[id],
            mode='lines',
            line=dict(
                width=4,
                color=color_border
            ),
        )
        curr_plot_data.append(scatter)

    layout = go.Layout(
        title=dict(
            text='',
            font=dict(
                family='Arial',
                size=33,
            )
        ),
        autosize=True,
        margin=go.layout.Margin(
            l=95,
            r=10,
            b=80,
            t=85,
            pad=0
        ),
        barmode='overlay',
        legend=dict(
            font=dict(
                family='Arial',
                size=16,
            ),
            orientation="h",
            x=0.33,
            y=1.11,
        ),
        xaxis=dict(
            title='R2',
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
            range=(min_x, max_x)
        ),
        yaxis=dict(
            title='PDF',
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
            range=(min_y, max_y)
        ),
    )

    figure = go.Figure(data=curr_plot_data, layout=layout)
    plotly.io.write_image(figure, data_path + data_file[:-4] + '.png')
