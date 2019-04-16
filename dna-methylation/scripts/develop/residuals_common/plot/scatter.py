import pydnameth as pdm

f = open('cpgs.txt', 'r')
cpg_list = f.read().splitlines()

data = pdm.Data(
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

data_params = {'cells': ['B', 'CD4T', 'NK', 'CD8T', 'Gran']}

pdm.residuals_common_plot_scatter_dev(
    data=data,
    annotations=annotations,
    attributes=attributes,
    observables_list=observables_list,
    cpg_list=cpg_list,
    data_params = data_params,
    method_params={
        'x_range': [5, 105],
        'y_range': [-0.4, 0.4],
        'details': 1
    },
)