import pandas as pd
from functools import reduce
import collections


path = f'E:/YandexDisk/Work/pydnameth/unn_epic/all_data'

df_DNAm = pd.read_excel(f'{path}/raw/DNAm_part(v2).xlsx', converters={'ID': str}, engine='openpyxl')
df_cells = pd.read_excel(f'{path}/raw/cells_part(v1).xlsx', converters={'ID': str}, engine='openpyxl')
df_biochem = pd.read_excel(f'{path}/raw/FGF23_FGF21_Klotho_GDF15_all.xlsx', converters={'ID': str}, engine='openpyxl')
df_multiplex = pd.read_excel(f'{path}/raw/MULTIPLEX_all.xlsx', converters={'ID': str}, engine='openpyxl')
df_gdoc = pd.read_excel(f'{path}/raw/gdoc_part(v2).xlsx', converters={'ID': str}, engine='openpyxl')
df_dignosis = pd.read_excel(f'{path}/raw/diseases_tmp.xlsx', converters={'ID': str}, engine='openpyxl')
df_drug = pd.read_excel(f'{path}/raw/drugs_tmp.xlsx', converters={'ID': str}, engine='openpyxl')
df_ages = pd.read_excel(f'{path}/raw/ages.xlsx', converters={'ID': str}, engine='openpyxl')
df_immunoclocks = pd.read_excel(f'{path}/raw/immuno_clocks.xlsx', converters={'ID': str}, engine='openpyxl')

df_tmp = pd.read_excel(f'{path}/table_part(v2).xlsx', converters={'ID': str}, engine='openpyxl')

IDs = df_dignosis['ID'].values
set_IDs = set(IDs)
print(len(set_IDs))
print([item for item, count in collections.Counter(IDs).items() if count > 1])


data_frames = [df_tmp, df_cells]
df_merged = reduce(lambda left, right: pd.merge(left, right, on=['ID']), data_frames)
df_merged.to_excel(f'{path}/current_table.xlsx', index=False)

print(set(df_DNAm['ID'].values) - set(df_merged['ID'].values))


ololo = 1
