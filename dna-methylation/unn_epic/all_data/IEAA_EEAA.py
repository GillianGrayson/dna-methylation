import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats
import numpy as np

def scale(x, out_range=(-1, 1)):
    domain = np.min(x), np.max(x)
    y = (x - (domain[1] + domain[0]) / 2) / (domain[1] - domain[0])
    return y * (out_range[1] - out_range[0]) + (out_range[1] + out_range[0]) / 2

y_name = 'Age'
formula_IEAA = 'DNAmAge ~ Age + CD8naive + CD8pCD28nCD45RAn + PlasmaBlast + CD4T + NK + Mono + Gran'
formula_EEAA = 'Age ~ WA'
part = 'v22'
target_part = 'Control'

path = f'E:/YandexDisk/Work/pydnameth/unn_epic/all_data'
df_merged = pd.read_excel(f'{path}/table_part({part}).xlsx', converters={'ID': str}, engine='openpyxl')
C_df = df_merged.loc[df_merged['Group'] == 'Control']
T_df = df_merged.loc[df_merged['Group'] == 'Disease']

model_IEAA = smf.ols(formula=formula_IEAA, data=C_df).fit()
IEA = model_IEAA.predict(df_merged)
df_merged[f"IEA"] = IEA
df_merged[f"IEAA"] = df_merged["DNAmAge"] - IEA

r_H, _ = stats.pearsonr(C_df["Age"].to_list(), C_df["DNAmAgeHannum"].to_list())
r_1, _ = stats.pearsonr(C_df["Age"].to_list(), C_df["CD8naive"].to_list())
r_2, _ = stats.pearsonr(C_df["Age"].to_list(), C_df["CD8pCD28nCD45RAn"].to_list())
r_3, _ = stats.pearsonr(C_df["Age"].to_list(), C_df["PlasmaBlast"].to_list())

wa = r_H * df_merged["DNAmAgeHannum"].to_numpy() + r_1 * df_merged["CD8naive"].to_numpy() + r_2 * df_merged["CD8pCD28nCD45RAn"].to_numpy() + r_3 * df_merged["PlasmaBlast"].to_numpy()
wa = wa / (r_H + r_1 + r_2 + r_3)

min_wa = np.min(df_merged["DNAmAgeHannum"].to_numpy())
max_wa = np.max(df_merged["DNAmAgeHannum"].to_numpy())
wa_normalized = scale(wa, out_range=(min_wa, max_wa))
df_merged[f"WA"] = wa
C_df = df_merged.loc[df_merged['Group'] == 'Control']

model_EEAA = smf.ols(formula=formula_EEAA, data=C_df).fit()
EEA = model_EEAA.predict(df_merged)
df_merged[f"EEA"] = IEA
df_merged[f"EEAA"] = df_merged["Age"] - IEA


df_merged.to_excel(f'{path}/current_table.xlsx', index=False)

