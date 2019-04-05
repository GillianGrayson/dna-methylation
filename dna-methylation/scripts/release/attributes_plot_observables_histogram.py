import pydnameth as pdm

data = pdm.Data(
    name='cpg_beta',
    path='',
    base='EPIC'
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

observables_list = [
    {'gender': 'F'},
    {'gender': 'M'}
]

pdm.attributes_plot_observables_histogram(
    data=data,
    annotations=annotations,
    attributes=attributes,
    observables_list=observables_list,
    params={
        'bin_size': 1.0,
        'opacity': 0.80,
        'barmode': 'overlay',
        'x_range': [5, 105]
    }
)