import pandas as pd
import numpy as np

data_file_path = 'C:/Users/User/YandexDisk/pydnameth/variance/betas/'
data_file_name = 'residuals_fixed.xlsx'

cpg_file_path = 'C:/Users/User/YandexDisk/pydnameth/variance/betas/'
cpg_file_name = 'betas_equal_residuals_equal_fixed.xlsx'

df = pd.read_excel(cpg_file_path + cpg_file_name)
cpg_list = list(df.cpg)

curr_data = pd.read_excel(data_file_path + data_file_name)
curr_cpgs = list(curr_data.cpg)

data_dict = dict((key,[]) for key in list(curr_data.columns))

for item in cpg_list:
    if item in curr_cpgs:
        index = curr_cpgs.index(item)
        for key in list(curr_data.columns):
            curr_value = curr_data.iloc[index][key]
            if isinstance(curr_value, float) and np.isnan(curr_value):
                curr_value = ''
            data_dict[key].append(curr_value)

data = pd.DataFrame(data_dict)
writer = pd.ExcelWriter(cpg_file_path + '\\' + cpg_file_name[:-5] + '_in_' + data_file_name[:-5] + '.xlsx', engine='xlsxwriter')
data.to_excel(writer, index=False, sheet_name='i')
writer.save()
