import pydnameth as pdm

f = open('cpgs.txt', 'r')
cpg_list = f.read().splitlines()

data = pdm.Data(
    name='cpg_beta',
    path='',
    base='GSE87571'
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

pdm.cpg_plot_methylation_scatter(
    data=data,
    annotations=annotations,
    attributes=attributes,
    observables_list=observables_list,
    cpg_list=cpg_list,
    params={
        'x_range': [10, 110]
    }
)