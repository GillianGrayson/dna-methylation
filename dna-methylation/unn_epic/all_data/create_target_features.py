import pandas as pd
import numpy as np

path = f'E:/YandexDisk/Work/pydnameth/unn_epic/all_data'

df_biochem = pd.read_excel(f'{path}/raw/FGF23_FGF21_Klotho_GDF15.xlsx', converters={'ID': str}, engine='openpyxl')
df_multiplex = pd.read_excel(f'{path}/raw/MULTIPLEX_20_11_2020_xtd_ver1.xlsx', converters={'ID': str}, engine='openpyxl')
df_dignosis = pd.read_excel(f'{path}/raw/diagnosis.xlsx', converters={'ID': str}, engine='openpyxl')
df_drug = pd.read_excel(f'{path}/raw/drug.xlsx', converters={'ID': str}, engine='openpyxl')

features = set.union(set(df_drug.columns))
features.remove('ID')
np.savetxt(f'{path}/drug_list.txt', list(features), fmt='%s')


