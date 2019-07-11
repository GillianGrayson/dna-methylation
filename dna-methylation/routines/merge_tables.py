import pandas as pd
import numpy as np

main_file_path = 'C:/Users/User/YandexDisk/pydnameth/variance/betas/'
main_file_name = 'residuals.xlsx'

main_df = pd.read_excel(main_file_path + main_file_name)
main_cpg_list = list(main_df.cpg)

data_dict = dict((key, []) for key in list(main_df.columns))

merged_file_path = 'C:/Users/User/YandexDisk/pydnameth/variance/betas/'
merged_file_name = 'betas_equal_residuals_equal_fixed.xlsx'

merged_df = pd.read_excel(merged_file_path + merged_file_name)
merged_cpg_list = list(merged_df.cpg)

for id in range(0, len(merged_cpg_list)):
    item = merged_cpg_list[id]
    for key in list(main_df.columns):
        curr_value = merged_df.iloc[id][key]
        if isinstance(curr_value, float) and np.isnan(curr_value):
            curr_value = ''
        data_dict[key].append(curr_value)

for id in range(0, len(main_cpg_list)):
    item = main_cpg_list[id]
    if item not in merged_cpg_list:
        for key in list(main_df.columns):
            curr_value = main_df.iloc[id][key]
            if isinstance(curr_value, float) and np.isnan(curr_value):
                curr_value = ''
            data_dict[key].append(curr_value)

data = pd.DataFrame(data_dict)
writer = pd.ExcelWriter(main_file_path + '\\' + main_file_name[:-5] + '_fixed' + '.xlsx', engine='xlsxwriter')
data.to_excel(writer, index=False, sheet_name='i')
writer.save()
