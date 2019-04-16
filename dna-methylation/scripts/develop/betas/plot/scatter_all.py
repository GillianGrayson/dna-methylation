import pydnameth as pdm
import pandas as pd
import os.path


f = open('cpgs.txt', 'r')
cpg_list = f.read().splitlines()

# fn = 'cpgs.xlsx'
# table_dict = {}
# if os.path.isfile(fn):
#     df = pd.read_excel(fn)
#     tmp_dict = df.to_dict()
#     for key in tmp_dict:
#         curr_dict = tmp_dict[key]
#         table_dict[key] = list(curr_dict.values())

# cpgs = table_dict['cpg']
# y_begins = table_dict['begin']
# y_ends = table_dict['end']

data_bases = ['GSE87571']

#for cpg_id in range(0, len(cpgs)):
    #cpg_list = [cpgs[cpg_id]]
    #y_begin = y_begins[cpg_id]
    #y_end = y_ends[cpg_id]

for data_base in data_bases:
    data = pdm.Data(
        name='cpg_beta',
        path='',
        base=data_base
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
            'x_range': [5, 105],
            #'y_range': [y_begin, y_end],
            'details': 1
        }
    )
