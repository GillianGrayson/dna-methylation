import pydnameth as pdm

f = open('cpgs.txt', 'r')
cpg_list = f.read().splitlines()

data = pdm.Data(
    name='cpg_beta',
    path='',
    base='GSE40279'
)

annotations = pdm.Annotations(
    name='annotations',
    exclude='none',
    cross_reactive='ex',
    snp='ex',
    chr='NS',
    gene_region='yes',
    geo='any',
    probe_class='any'
)

observables = pdm.Observables(
    name='observables',
    types={}
)

cells_types = ['B', 'CD4T', 'NK', 'CD8T', 'Gran']

cells = pdm.Cells(
    name='cells',
    types=cells_types
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

pdm.residuals_common_plot_methylation_scatter_dev(
    data=data,
    annotations=annotations,
    attributes=attributes,
    observables_list=observables_list,
    cpg_list=cpg_list,
    params={
        'x_range': [10, 110]
    }
)