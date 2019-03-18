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

cells_types = ['B', 'CD4T', 'NK', 'CD8T', 'Gran']

cells = pdm.Cells(
    name='cells',
    types=cells_types
)

obs_list = [
    {'gender': 'F'},
]

for obs in obs_list:

    observables = pdm.Observables(
        name='observables',
        types=obs
    )

    attributes = pdm.Attributes(
        target='age',
        observables=observables,
        cells=cells
    )

    pdm.residuals_special_proc_table_linreg_dev(
        data=data,
        annotations=annotations,
        attributes=attributes
    )