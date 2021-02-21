import pandas as pd
from functools import reduce

path = f'E:/YandexDisk/Work/pydnameth/unn_epic/all_data'

df_main = pd.read_excel(f'{path}/raw/DNAm_part(wo_noIntensity_detP).xlsx', converters={'ID': str}, engine='openpyxl')
df_biochem = pd.read_excel(f'{path}/raw/FGF23_FGF21_Klotho_GDF15.xlsx', converters={'ID': str}, engine='openpyxl')
df_multiplex = pd.read_excel(f'{path}/raw/MULTIPLEX_20_11_2020_xtd_ver1.xlsx', converters={'ID': str}, engine='openpyxl')
df_gdoc = pd.read_excel(f'{path}/raw/gdoc.xlsx', converters={'ID': str}, engine='openpyxl')

data_frames = [df_main, df_multiplex, df_gdoc]
df_merged = reduce(lambda left, right: pd.merge(left, right, on=['ID']), data_frames)
df_merged.to_excel(f'{path}/current_table.xlsx', index=False)

