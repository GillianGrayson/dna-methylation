import pydnameth as pdm

items = ['epimutations']
x_ranges = [[5, 105]] * len(items)
y_ranges = ['auto'] * len(items)

data_bases = ['GSE87571']

for data_base in data_bases:

    data = pdm.Data(
        path='',
        base=data_base
    )

    annotations = pdm.Annotations(
        name='annotations',
        exclude='bad_cpgs',
        cross_reactive='any',
        snp='any',
        chr='NS',
        gene_region='any',
        geo='any',
        probe_class='any'
    )

    observables = pdm.Observables(
        name='observables',
        types={}
    )

    cells = pdm.Cells(
        name='cells',
        types='any'
    )

    attributes = pdm.Attributes(
        target='age',
        observables=observables,
        cells=cells
    )

    if data.base == 'GSE55763':
        observables_list = [
            {'gender': 'F', 'is_duplicate': '0', 'age': (35, 100)},
            {'gender': 'M', 'is_duplicate': '0', 'age': (35, 100)}
        ]
    else:
        observables_list = [
            {'gender': 'F'},
            {'gender': 'M'}
        ]

    pdm.epimutations_plot_scatter(
        data=data,
        annotations=annotations,
        attributes=attributes,
        observables_list=observables_list,
        method_params={
            'items': items,
            'x_ranges': x_ranges,
            'y_ranges': y_ranges,
            'line': 'no',
            'fit': 'yes',
            'semi_window': 8,
            'box_b': 'Q5',
            'box_t': 'Q95',
            'add': 'none',
            'legend_size': 1
        }
    )