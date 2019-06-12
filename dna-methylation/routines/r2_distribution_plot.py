import pandas as pd
import plotly.graph_objs as go
import colorlover as cl
import plotly
import numpy as np

data_path = 'D:/Aaron/Bio/variance/v2/'
data_files = ['I.csv']

eps = 0.00000001

for data_file in data_files:
    raw_data = pd.read_csv(data_path + data_file)
    column_names = list(raw_data.columns)
    curr_data = []
    curr_plot_data = []
    lines = []
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
            max_x = 3.0
            min_x = 1.0
        num_bins = 1000
        shift = (max_x - min_x) / num_bins
        x = [min_x + (shift / 2) + i * shift for i in range(0, num_bins)]
        y = [0] * num_bins
        num_outliers = 0
        for row_id, curr_y in enumerate(curr_data[id]):
            if curr_y > max_x or curr_y < min_x:
                num_outliers += 1
            else:
                index = int(np.floor((curr_y - min_x) / (max_x - min_x + eps) * num_bins))
                y[index] += 1

        sum_y = sum(y)
        y = [curr_y / (sum_y * shift) for curr_y in y]
        if min(y) < min_y:
            min_y = min(y)
        if max(y) > max_y:
            max_y = max(y)

        percentile = np.percentile(curr_data[id], 75)

        #print('Num outliers in ', column_names[id], ' : ', num_outliers)
        print('75% in ', column_names[id], ' : ', percentile)

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

        curr_line = {
            'type': 'line',
            'x0': percentile,
            'y0': min_y,
            'x1': percentile,
            'y1': max_y,
            'line': {
                'color': color_border,
                'width': 4,
            },
        }

        lines.append(curr_line)

    if 'I' in data_file:
        x_name = r'$I$'
    elif 'mean' in data_file:
        x_name = r'$\frac{R_F^2 + R_M^2}{2}$'
    elif 'R2' in data_file:
        x_name = r'$R^2$'

    layout = go.Layout(
        autosize=True,
        barmode='overlay',
        legend=dict(
            font=dict(
                family='Arial',
                size=16,
            ),
            orientation="h",
            x=0.11,
            y=1.11,
        ),
        margin=go.layout.Margin(
            l=95,
            r=10,
            b=80,
            t=85,
            pad=0
        ),
        shapes=lines,
        xaxis=dict(
            exponentformat='e',
            mirror='ticks',
            showexponent='all',
            showgrid=True,
            showline=True,
            showticklabels=True,
            tickangle=0,
            tickfont=dict(
                color='black',
                family='Arial',
                size=30
            ),
            title=dict(
                font=dict(
                    color='black',
                    family='Arial',
                    size=50),
                text=x_name)
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
            showexponent='all'
        )
    )

    figure = go.Figure(data=curr_plot_data, layout=layout)
    plotly.offline.plot(figure, filename=data_path + data_file[:-4] + '.html', auto_open=False, show_link=True)
    plotly.io.write_image(figure, data_path + data_file[:-4] + '.png')
    #plotly.io.write_image(figure, data_path + data_file[:-4] + '.pdf')
