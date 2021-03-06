import pydnameth as pdm

data_sets = ['GSE87571_TEST']

for data_set in data_sets:

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

    if data.base == 'GSE55763':
        data_params = None
        observables_list = [
            {'gender': 'F', 'is_duplicate': '0', 'age': (35, 100)},
            {'gender': 'M', 'is_duplicate': '0', 'age': (35, 100)}
        ]
        cells = pdm.Cells(
            name='cells_horvath_calculator',
            types='any'
        )
    elif data.base == 'E-MTAB-7309' or data.base == 'E-MTAB-7309-FILTERED':
        data_params = {
            'norm': 'quantile',
        }
        observables_list = [
            {'sex': 'female'},
            {'sex': 'male'}
        ]
        cells = pdm.Cells(
            name='cells_horvath_calculator',
            types='any'
        )
    else:
        data_params = None
        observables_list = [
            {'gender': 'F'},
            {'gender': 'M'}
        ]
        cells = pdm.Cells(
            name='cells',
            types='any'
        )

    attributes = pdm.Attributes(
        target='age',
        observables=observables,
        cells=cells
    )

    pdm.epimutations_table_aggregator_linreg(
        data=data,
        annotations=annotations,
        attributes=attributes,
        observables_list=observables_list,
        data_params=data_params
    )