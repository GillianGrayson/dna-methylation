import pydnameth as pdm

f = open('cpgs.txt', 'r')
items = f.read().splitlines()
x_ranges = [[5, 105]] * len(items)
y_ranges = ['auto'] * len(items)


data = pdm.Data(
    path='',
    base='GSE87571'
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


if data.base == 'GSE55763':
    observables_list = [
        {'gender': 'F', 'is_duplicate': '0', 'age': (35, 100)},
        {'gender': 'M', 'is_duplicate': '0', 'age': (35, 100)}
    ]

    data_params = {
        'cells': ['Bcell', 'CD4T', 'NK', 'CD8T', 'Gran'],
        'observables': ['age']
    }

    cells = pdm.Cells(
        name='cells_horvath_calculator',
        types='any'
    )

else:
    observables_list = [
        {'gender': 'F'},
        {'gender': 'M'}
    ]

    data_params = {
        'cells': ['B', 'CD4T', 'NK', 'CD8T', 'Gran'],
        'observables': ['age']
    }

    cells = pdm.Cells(
        name='cells',
        types='any'
    )

attributes = pdm.Attributes(
    target='age',
    observables=observables,
    cells=cells
)

pdm.residuals_common_plot_scatter(
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
        'legend_size': 1,
        'add': 'none'
    }
)