import pydnameth as pdm

f = open('cpgs.txt', 'r')
items = f.read().splitlines()
x_ranges = [[5, 105]] * len(items)
y_ranges = ['auto'] * len(items)

data = pdm.Data(
    path='',
    base='GSE88890'
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
    name='cells',
    types='any'
)

if data.base == 'GSE55763':
    target = 'age'
    observables_list = [
        {'gender': 'F', 'is_duplicate': '0', 'age': (35, 100)},
        {'gender': 'M', 'is_duplicate': '0', 'age': (35, 100)}
    ]
elif data.base == 'GSE64244':
    target = 'age'
    observables_list = [
        {'disease_status': 'Turner_syndrome_45,X_(Maternal)'},
        {'disease_status': 'Turner_syndrome_45,X_(Paternal)'}
    ]
elif data.base == 'GSE43414':
    x_ranges = ['auto'] * len(items)
    target = 'age.brain'
    observables_list = [
        {'source_tissue': 'superior_temporal_gyrus', 'Sex': 'FEMALE'},
        {'source_tissue': 'superior_temporal_gyrus', 'Sex': 'MALE'}
    ]
elif data.base == 'GSE88890':
    x_ranges = ['auto'] * len(items)
    target = 'age'
    observables_list = [
        {'gender': 'F'},
        {'gender': 'M'}
    ]
else:
    target = 'age'
    observables_list = [
        {'gender': 'F'},
        {'gender': 'M'}
    ]

attributes = pdm.Attributes(
    target=target,
    observables=observables,
    cells=cells
)

pdm.betas_plot_scatter(
    data=data,
    annotations=annotations,
    attributes=attributes,
    observables_list=observables_list,
    method_params={
        'items': items,
        'x_ranges': x_ranges,
        'y_ranges': y_ranges,
        'line': 'yes',
        'fit': 'none',
        'semi_window': 8,
        'box_b': 'Q5',
        'box_t': 'Q95',
        'legend_size': 2,
        'add': 'none'
    }
)
