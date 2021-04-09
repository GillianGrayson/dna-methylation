import pandas as pd
import numpy as np

path = f'E:/YandexDisk/Work/pydnameth/unn_epic/all_data'

#df_biochem = pd.read_excel(f'{path}/raw/FGF23_FGF21_Klotho_GDF15.xlsx', converters={'ID': str}, engine='openpyxl')
df_multiplex = pd.read_excel(f'{path}/raw/MULTIPLEX_20_11_2020_xtd_ver1.xlsx', converters={'ID': str}, engine='openpyxl')
df_diseases = pd.read_excel(f'{path}/raw/diseases_tmp.xlsx', converters={'ID': str}, engine='openpyxl')
df_drugs = pd.read_excel(f'{path}/raw/drugs_tmp.xlsx', converters={'ID': str}, engine='openpyxl')

features = set.union(set(df_drugs.columns))
features.remove('ID')
features = sorted(list(features))
np.savetxt(f'{path}/drugs.txt', features, fmt='%s')


