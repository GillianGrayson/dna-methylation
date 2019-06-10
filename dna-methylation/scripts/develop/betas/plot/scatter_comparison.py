import pydnameth as pdm
import pandas as pd
import os.path

fn = 'scatter_table_rows.xlsx'
rows_dict = {}
if os.path.isfile(fn):
    df = pd.read_excel(fn)
    tmp_dict = df.to_dict()
    for key in tmp_dict:
        curr_dict = tmp_dict[key]
        rows_dict[key] = list(curr_dict.values())

fn = 'scatter_table_cols.xlsx'
cols_dict = {}
if os.path.isfile(fn):
    df = pd.read_excel(fn)
    tmp_dict = df.to_dict()
    for key in tmp_dict:
        curr_dict = tmp_dict[key]
        cols_dict[key] = list(curr_dict.values())

data_bases = cols_dict['data_base']  # cols

data_list = []
annotations_list = []
attributes_list = []
observables_list = []

for data_base in data_bases:

    data = pdm.Data(
        path='',
        base=data_base
    )
    data_list.append(data)

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
    annotations_list.append(annotations)


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
    attributes_list.append(attributes)

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

pdm.betas_plot_scatter_comparison(
    data_list=data_list,
    annotations_list=annotations_list,
    attributes_list=attributes_list,
    observables_list=observables_list,
    rows_dict=rows_dict,
    cols_dict=cols_dict,
    method_params={
        'line': 'no',
        'fit': 'yes',
        'semi_window': '8',
    }
)
