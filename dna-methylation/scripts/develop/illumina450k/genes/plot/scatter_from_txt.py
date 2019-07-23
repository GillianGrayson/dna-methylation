import pydnameth as pdm

f = open('genes.txt', 'r')
items = f.read().splitlines()
x_ranges = [[5, 105]] * len(items)
y_ranges = ['auto'] * len(items)


data = pdm.Data(
    path='',
    base='E-MTAB-7309-FILTERED'
)

annotations = pdm.Annotations(
    name='annotations',
    exclude='bad_cpgs',
    cross_reactive='any',
    snp='any',
    chr='NS',
    gene_region='any',
    geo='islands_shores',
    probe_class='any'
)

observables = pdm.Observables(
    name='observables',
    types={}
)

cells = pdm.Cells(
    name='cells_horvath_calculator',
    types='any'
)

attributes = pdm.Attributes(
    target='age',
    observables=observables,
    cells=cells
)

data_params = {'source': 'betas'}

if data.base == 'GSE55763':
    data_params = {'source': 'betas'}
    observables_list = [
        {'gender': 'F', 'is_duplicate': '0', 'age': (35, 100)},
        {'gender': 'M', 'is_duplicate': '0', 'age': (35, 100)}
    ]
elif data.base == 'E-MTAB-7309' or data.base == 'E-MTAB-7309-FILTERED':
    data_params = {
        'source': 'betas',
        'norm': 'quantile'
    }
    observables_list = [
        {'sex': 'female'},
        {'sex': 'male'}
    ]
else:
    data_params = {'source': 'betas'}
    observables_list = [
        {'gender': 'F'},
        {'gender': 'M'}
    ]

pdm.genes_plot_scatter(
    data=data,
    annotations=annotations,
    attributes=attributes,
    observables_list=observables_list,
    data_params=data_params,
    method_params={
        'items': items,
        'x_ranges': x_ranges,
        'y_ranges': y_ranges,
        'line': 'yes',
        'fit': 'none',
        'semi_window': 8,
        'box_b': 'Q5',
        'box_t': 'Q95',
        'legend_size': 1,
        'add': 'none'
    }
)