import pandas as pd
import numpy as np

cpg_file_path = 'D:/Aaron/Bio/variance/v12/'
cpg_file_name = '1_2_3_4.xlsx'

data_file_path = 'D:/Aaron/Bio/variance/v2/'
data_file_names = ['GSE40279.xlsx', 'GSE87571.xlsx', 'EPIC.xlsx', 'GSE55763.xlsx']

df = pd.read_excel(cpg_file_path + cpg_file_name)
data_dict = {}
data_dict['cpg'] = list(df.cpg)
data_dict['gene'] = list(df.gene)

for data_file_name in data_file_names:
    print(data_file_name[:-5])
    data_dict[data_file_name[:-5]] = []
    curr_data = pd.read_excel(data_file_path + data_file_name)
    curr_cpgs = list(curr_data.item)
    curr_inc = list(curr_data.increasing_1_box_common)
    for item in data_dict['cpg']:
        index = curr_cpgs.index(item)
        data_dict[data_file_name[:-5]].append(curr_inc[index])

data_dict['max_inc'] = []
data_dict['mean_inc_4'] = []
data_dict['mean_inc_3'] = []
for id in range(0, len(data_dict['cpg'])):
    vals = []
    for data_file_name in data_file_names:
        vals.append(data_dict[data_file_name[:-5]][id])
    data_dict['max_inc'].append(max(vals))
    data_dict['mean_inc_4'].append(np.mean(vals))
    data_dict['mean_inc_3'].append(np.mean(vals[1:]))

data = pd.DataFrame(data_dict)
writer = pd.ExcelWriter(cpg_file_path + '\\' + cpg_file_name[:-5] + '_modified' + '.xlsx', engine='xlsxwriter')
data.to_excel(writer, index=False, sheet_name='i')
writer.save()

