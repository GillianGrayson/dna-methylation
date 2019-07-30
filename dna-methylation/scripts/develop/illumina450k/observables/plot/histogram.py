import pydnameth as pdm

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
else:
    observables_list = [
        {'gender': 'F'},
        {'gender': 'M'}
    ]

pdm.observables_plot_histogram(
    data=data,
    annotations=annotations,
    attributes=attributes,
    observables_list=observables_list,
    method_params={
        'bin_size': 1.0,
        'opacity': 0.80,
        'barmode': 'overlay',
        'x_range': [5, 105],
        'legend_size': 1
    }
)