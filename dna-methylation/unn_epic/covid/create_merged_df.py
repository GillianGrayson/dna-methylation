import pandas as pd
from functools import reduce
import collections


path = f'E:/YandexDisk/Work/pydnameth/unn_epic/covid'

df_1 = pd.read_excel(f'{path}/table_1.xlsx', converters={'ID': str}, engine='openpyxl')
df_2 = pd.read_excel(f'{path}/tmp.xlsx', converters={'ID': str}, engine='openpyxl')


data_frames = [df_1, df_2]
df_merged = reduce(lambda left, right: pd.merge(left, right, on=['cpg']), data_frames)
df_merged.to_excel(f'{path}/current_table.xlsx', index=False)

