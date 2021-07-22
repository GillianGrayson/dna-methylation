import pandas as pd
from functools import reduce
import collections


path = f'E:/YandexDisk/Work/students/nerobova/cpg_correct'

df_1 = pd.read_excel(f'{path}/article1.xlsx', converters={'ID': str}, engine='openpyxl')
df_2 = pd.read_excel(f'{path}/article2.xlsx', converters={'ID': str}, engine='openpyxl')
df_3 = pd.read_excel(f'{path}/article3.xlsx', converters={'ID': str}, engine='openpyxl')
df_4 = pd.read_excel(f'{path}/article4.xlsx', converters={'ID': str}, engine='openpyxl')
df_5 = pd.read_excel(f'{path}/article5.xlsx', converters={'ID': str}, engine='openpyxl')
df_tmp = pd.read_excel(f'{path}/tmp1.xlsx', converters={'ID': str}, engine='openpyxl')


s1 = set(df_1['CpG'].to_list())
s2 = set(df_2['CpG'].to_list())
s3 = set(df_3['CpG'].to_list())
s4 = set(df_4['CpG'].to_list())
s5 = set(df_5['CpG'].to_list())
stmp = set(df_tmp['CpG'].to_list())

i_tmp_1 = set.intersection(s1, stmp)
i_tmp_2 = set.intersection(s2, stmp)
i_tmp_3 = set.intersection(s3, stmp)
i_tmp_4 = set.intersection(s4, stmp)
i_tmp_5 = set.intersection(s5, stmp)



ololo = 1
