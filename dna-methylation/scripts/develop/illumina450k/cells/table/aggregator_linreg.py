import pydnameth as pdm

data_sets = ['GSE87571_TEST']

for data_set in data_sets:

    cell_types = ['Bcell', 'CD4T', 'NK', 'CD8T', 'Gran']
    cell_name = 'cells_horvath_calculator'

    data = pdm.Data(
        path='',
        base=data_set
    )

    annotations = pdm.Annotations(
        name='annotations',
        type='450k',
        exclude='bad_cpgs',
        select_dict={
            'CHR': ['-X', '-Y']
        }
    )

    observables = pdm.Observables(
        name='observables',
        types={}
    )

    cells = pdm.Cells(
        name=cell_name,
        types=cell_types
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

    pdm.cells_table_aggregator_linreg(
        data=data,
        annotations=annotations,
        attributes=attributes,
        observables_list=observables_list
    )
