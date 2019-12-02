import itertools
import numpy as np
import copy
import plotly.graph_objs as go
import plotly
import plotly.io as pio
import colorlover as cl


def save_figure(fn, fig):
    plotly.offline.plot(fig, filename=fn + '.html', auto_open=False, show_link=True)
    pio.write_image(fig, fn + '.png')
    pio.write_image(fig, fn + '.pdf')


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


def plot_venn(lists, labels, path, suffix):

    ids = list(range(0, len(lists)))

    ordered_keys = []

    sizes = {}
    checking = {}
    for id, label in enumerate(labels):
        sizes[label] = len(set(lists[id]))
        ordered_keys.append(label)
        checking[label] = 0

    for L in range(2, len(lists) + 1):
        for subset in itertools.combinations(ids, L):

            curr_ids = list(subset)

            curr_labels_raw = np.array(labels)[np.array(curr_ids)]
            curr_labels_raw = np.sort(curr_labels_raw)
            curr_labels = '_'.join(list(curr_labels_raw))

            if curr_labels not in sizes:

                cur_intersection = set(lists[curr_ids[0]])
                for id in curr_ids[1::]:
                    cur_intersection = cur_intersection.intersection(set(lists[id]))
                sizes[curr_labels] = len(cur_intersection)

                ordered_keys.append(curr_labels)

    ordered_keys = ordered_keys[::-1]

    sizes_for_venn = copy.deepcopy(sizes)
    for key in ordered_keys:
        curr_labels = set(key.split('_'))
        for key_var in ordered_keys:
            curr_labels_var = set(key_var.split('_'))
            if key_var != key:
                if curr_labels.issubset(curr_labels_var):
                    sizes_for_venn[key] -= sizes_for_venn[key_var]

    for key in sizes_for_venn:
        curr_labels = key.split('_')
        for label in curr_labels:
            checking[label] += sizes_for_venn[key]

    for id, label in enumerate(labels):
        if checking[label] != len(set(lists[id])):
            raise ValueError('Error in venn data creating')
    print('Venn data ok')

    venn_labels = []
    for key in sizes_for_venn:
        curr_labels = key.split('_') + [str(sizes_for_venn[key])]
        venn_labels.append('<br>'.join(curr_labels))

    layout = get_layout_3()
    trace = get_trace_3(venn_labels)

    fig = {
        'data': [trace],
        'layout': layout,
    }

    fn = path + '/' + ordered_keys[0] + '_' + suffix
    save_figure(fn, fig)



