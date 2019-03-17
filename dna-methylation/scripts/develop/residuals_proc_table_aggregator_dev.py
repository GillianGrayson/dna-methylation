import pydnameth as pdm

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

pdm.residuals_proc_table_aggregator_dev(
    data=data,
    annotations=annotations,
    attributes=attributes,
    observables_list=observables_list,
    params=None
)