import pydnameth as pdm


items = ['Bcell', 'CD4T', 'NK', 'CD8T', 'Gran']
x_ranges = [[5, 105]] * len(items)
y_ranges = ['auto'] * len(items)

data_sets = ['GSE87571']

for data_set in data_sets:

    cell_types = items
    cell_name = 'cells_horvath_calculator'


    data = pdm.Data(
        path='',
        base=data_set
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
        name=cell_name,
        types=cell_types
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

    pdm.cells_plot_scatter(
        data=data,
        annotations=annotations,
        attributes=attributes,
        observables_list=observables_list,
        method_params={
            'items': items,
            'x_ranges': x_ranges,
            'y_ranges': y_ranges,
            'legend_size': 1,
            'line': 'no',
            'fit': 'yes',
            'semi_window': 8,
            'box_b': 'Q5',
            'box_t': 'Q95',
            'add': 'none',
        }
    )
