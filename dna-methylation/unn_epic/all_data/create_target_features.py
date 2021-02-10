import pandas as pd
import numpy as np

path = f'E:/YandexDisk/Work/pydnameth/unn_epic/all_data'

df_biochem = pd.read_excel(f'{path}/markers/FGF23_FGF21_Klotho_GDF15.xlsx', converters={'ID': str}, engine='openpyxl')
df_multiplex = pd.read_excel(f'{path}/markers/MULTIPLEX_20_11_2020_xtd_ver1.xlsx', converters={'ID': str}, engine='openpyxl')

features = set.union(set(df_biochem.columns), set(df_multiplex.columns))
features.remove('ID')
np.savetxt(f'{path}/features_list.txt', list(features), fmt='%s')


