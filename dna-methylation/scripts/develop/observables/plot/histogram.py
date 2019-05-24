import pydnameth as pdm

data = pdm.Data(
    path='',
    base='GSE55763'
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
    {'gender': 'F', 'description': 'population_study_sample'},
    {'gender': 'M', 'description': 'population_study_sample'}
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