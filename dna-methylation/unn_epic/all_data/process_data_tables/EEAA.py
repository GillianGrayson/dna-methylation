import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats
import numpy as np


formula_EEAA = 'BioAge4HAStatic ~ Age'
part = 'v2'

path = f'E:/YandexDisk/Work/pydnameth/unn_epic/all_data'
df_merged = pd.read_excel(f'{path}/table_part({part}).xlsx', converters={'ID': str}, engine='openpyxl')
C_df = df_merged.loc[df_merged['Group'] == 'Control']

model_EEAA = smf.ols(formula=formula_EEAA, data=C_df).fit()
EEA = model_EEAA.predict(df_merged)
df_merged[f"EEAA"] = df_merged["BioAge4HAStatic"] - EEA

df_merged.to_excel(f'{path}/current_table.xlsx', index=False)

