import pydnameth as pdm

data_sets = ['GSE40279', 'GSE87571', 'EPIC', 'GSE55763']

for data_set in data_sets:

    cell_types = ['B', 'CD4T', 'NK', 'CD8T', 'Gran']
    if data_set == 'GSE55763':
        cell_types = ['Bcell', 'CD4T', 'NK', 'CD8T', 'Gran']

    for cell_type in cell_types:

        data = pdm.Data(
            path='',
            base=data_set
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
            types=cell_type
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

        pdm.cells_table_z_test_linreg(
            data=data,
            annotations=annotations,
            attributes=attributes,
            observables_list=observables_list
        )
