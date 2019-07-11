import pandas as pd
import numpy as np

cpg_file_path = 'C:/Users/User/YandexDisk/pydnameth/variance/residuals/'
cpg_file_name = 'betas_equal.xlsx'

data_file_path = 'C:/Users/User/YandexDisk/pydnameth/variance/residuals/'
data_file_names = ['GSE40279.xlsx', 'GSE87571.xlsx', 'EPIC.xlsx', 'GSE55763.xlsx']

df = pd.read_excel(cpg_file_path + cpg_file_name)
data_dict = {}
data_dict['cpg'] = list(df.cpg)
data_dict['gene'] = list(df.gene)

for data_file_name in data_file_names:
    print(data_file_name[:-5])
    data_dict['increasing_fit_' + data_file_name[:-5]] = []
    data_dict['increasing_fit_normed_' + data_file_name[:-5]] = []
    data_dict['increasing_fit_id_' + data_file_name[:-5]] = []
    data_dict['r2_F_' + data_file_name[:-5]] = []
    data_dict['r2_M_' + data_file_name[:-5]] = []
    data_dict['r2_min_' + data_file_name[:-5]] = []

    curr_data = pd.read_excel(data_file_path + data_file_name)
    curr_cpgs = list(curr_data.item)
    curr_inc_fit = list(curr_data.increasing_fit)
    curr_inc_fit_normed = list(curr_data.increasing_fit_normed)
    curr_inc_fit_id = list(curr_data.increasing_fit_id)
    curr_inc_real = list(curr_data.increasing_real)
    curr_inc_real_normed = list(curr_data.increasing_real_normed)
    curr_inc_real_id = list(curr_data.increasing_real_id)
    curr_r2_f = list(curr_data.best_R2_gender_F)
    curr_r2_m = list(curr_data.best_R2_gender_M)
    curr_r2_min = list(curr_data.r2_min)
    for item in data_dict['cpg']:
        index = curr_cpgs.index(item)
        data_dict['increasing_fit_' + data_file_name[:-5]].append(curr_inc_fit[index])
        data_dict['increasing_fit_normed_' + data_file_name[:-5]].append(curr_inc_fit_normed[index])
        data_dict['increasing_fit_id_' + data_file_name[:-5]].append(curr_inc_fit_id[index])
        data_dict['r2_F_' + data_file_name[:-5]].append(curr_r2_f[index])
        data_dict['r2_M_' + data_file_name[:-5]].append(curr_r2_m[index])
        data_dict['r2_min_' + data_file_name[:-5]].append(curr_r2_min[index])

data_dict['mean_inc_fit_4'] = []
data_dict['mean_inc_fit_3'] = []
data_dict['mean_inc_fit_normed_4'] = []
data_dict['mean_inc_fit_normed_3'] = []
for id in range(0, len(data_dict['cpg'])):
    vals_fit = []
    vals_fit_normed = []
    vals_real = []
    vals_real_normed = []
    for data_file_name in data_file_names:
        vals_fit.append(data_dict['increasing_fit_' + data_file_name[:-5]][id])
        vals_fit_normed.append(data_dict['increasing_fit_normed_' + data_file_name[:-5]][id])
    data_dict['mean_inc_fit_4'].append(np.mean(vals_fit))
    data_dict['mean_inc_fit_3'].append(np.mean(vals_fit[1:]))
    data_dict['mean_inc_fit_normed_4'].append(np.mean(vals_fit_normed))
    data_dict['mean_inc_fit_normed_3'].append(np.mean(vals_fit_normed[1:]))

data = pd.DataFrame(data_dict)
writer = pd.ExcelWriter(cpg_file_path + '\\' + cpg_file_name[:-5] + '_with_r2' + '.xlsx', engine='xlsxwriter')
data.to_excel(writer, index=False, sheet_name='i')
writer.save()

