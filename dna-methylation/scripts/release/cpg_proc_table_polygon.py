import pydnameth as pdm

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
    types={'gender': 'vs'}
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
    {'smoke': ['1', '2']},
    {'smoke': ['3', '4']}
]

pdm.cpg_proc_table_polygon(
    data=data,
    annotations=annotations,
    attributes=attributes,
    observables_list=observables_list
)