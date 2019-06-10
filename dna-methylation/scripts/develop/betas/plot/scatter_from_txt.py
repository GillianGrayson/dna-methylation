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
elif data.base == 'GSE64244':
    observables_list = [
        {'disease_status': 'Turner_syndrome_45,X_(Maternal)'},
        {'disease_status': 'Turner_syndrome_45,X_(Paternal)'}
    ]
else:
    observables_list = [
        {'gender': 'F'},
        {'gender': 'M'}
    ]

pdm.betas_plot_scatter(
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
