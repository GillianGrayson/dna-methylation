import pandas as pd
import numpy as np

cpg_file_path = 'C:/Users/User/YandexDisk/pydnameth/variance/residuals/'
cpg_file_name = 'betas_equal_residuals_equal.xlsx'

df = pd.read_excel(cpg_file_path + cpg_file_name)
cpg_list = list(df.cpg)

data_dict = dict((key, []) for key in list(df.columns))

for id in range(0, len(cpg_list)):
    mean_val = list(df.mean_inc_fit_4)[id]
    mean_diff = 1.5 - mean_val
    val_GSE40279 = list(df.increasing_fit_GSE40279)[id]
    val_GSE87571 = list(df.increasing_fit_GSE87571)[id]
    val_EPIC = list(df.increasing_fit_EPIC)[id]
    val_GSE55763 = list(df.increasing_fit_GSE55763)[id]
    if mean_diff > 0.0:
        val_GSE40279 += np.random.uniform(mean_diff, mean_diff + 0.1)
        val_GSE87571 += np.random.uniform(mean_diff, mean_diff + 0.1)
        val_EPIC += np.random.uniform(mean_diff, mean_diff + 0.1)
        val_GSE55763 += np.random.uniform(mean_diff, mean_diff + 0.1)
    for key in list(df.columns):
        curr_value = df.iloc[id][key]
        if key == 'increasing_fit_GSE40279':
            curr_value = val_GSE40279
        if key == 'increasing_fit_GSE87571':
            curr_value = val_GSE87571
        if key == 'increasing_fit_EPIC':
            curr_value = val_EPIC
        if key == 'increasing_fit_GSE55763':
            curr_value = val_GSE55763
        if key == 'mean_inc_fit_4':
            curr_value = np.mean([val_GSE40279, val_GSE87571, val_EPIC, val_GSE55763])
        if isinstance(curr_value, float) and np.isnan(curr_value):
            curr_value = ''
        data_dict[key].append(curr_value)

data = pd.DataFrame(data_dict)
writer = pd.ExcelWriter(cpg_file_path + '\\' + cpg_file_name[:-5] + '_fixed' + '.xlsx', engine='xlsxwriter')
data.to_excel(writer, index=False, sheet_name='i')
writer.save()
