import pandas as pd
from sklearn.linear_model import ElasticNet, ElasticNetCV
from sklearn.model_selection import RepeatedKFold, GridSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
import pickle
from pathlib import Path
import os
import copy
import statsmodels.formula.api as smf
from numpy import mean
from numpy import std
from numpy import absolute
from sklearn.model_selection import cross_val_score


def calc_metrics(model, df, y_name, comment, params):
    y = df.loc[:, y_name].values
    y_pred = model.predict(df)
    df = pd.DataFrame({'y_pred': y_pred, 'y': y})

    reg = smf.ols(formula=f"y_pred ~ y", data=df).fit()

    score_2 = r2_score(y, y_pred)

    rmse = np.sqrt(mean_squared_error(y, y_pred))
    mae = mean_absolute_error(y, y_pred)
    params[f'{comment} R2'] = score_2
    params[f'{comment} RMSE'] = rmse
    params[f'{comment} MAE'] = mae
    return y_pred


y_name = 'Age'
part = 'v2'

target_part = 'Control'
data_type = '3biomarkers_milli'

path = f'E:/YandexDisk/Work/pydnameth/unn_epic/all_data'
df_merged = pd.read_excel(f'{path}/table_part({part}).xlsx', converters={'ID': str}, engine='openpyxl')

save_path = f'{path}/clock/{data_type}/{target_part}/{y_name}/part({part})'
if not os.path.exists(save_path):
    os.makedirs(save_path)

with open(f'{path}/{data_type}.txt') as f:
    target_features = f.read().splitlines()

X_C_df = df_merged.loc[df_merged['Group'] == 'Control']
X_C = X_C_df[list(target_features)].to_numpy()
y_C = X_C_df[y_name].to_numpy()

X_T_df = df_merged.loc[df_merged['Group'] == 'ESRD']
X_T = X_T_df[list(target_features)].to_numpy()
y_T = X_T_df[y_name].to_numpy()

X_all = df_merged[list(target_features)].to_numpy()
y_all = df_merged[y_name].to_numpy()

if target_part == 'All':
    X_target = X_all
    y_target = y_all
elif target_part == 'Control':
    X_target = X_C
    y_target = y_C
else:
    raise ValueError("Unsupported target_part")

formula = ' + '.join(target_features)
model = smf.ols(formula=f"{y_name} ~ {formula}", data=X_C_df).fit()

Path(f'{path}/clock/{data_type}/{target_part}/{y_name}/part({part})').mkdir(parents=True, exist_ok=True)
df_to_save = model.params.to_frame(name='Value')
df_to_save.index.name = 'Name'
df_to_save.to_excel(f'{path}/clock/{data_type}/{target_part}/{y_name}/part({part})/clock.xlsx', index=True)

with open(f'{path}/clock/{data_type}/{target_part}/{y_name}/part({part})/clock.pkl', 'wb') as handle:
    pickle.dump(model, handle, protocol=pickle.HIGHEST_PROTOCOL)
params = {}
y_pred_C = calc_metrics(model, df_merged.loc[df_merged['Group'] == 'Control'], y_name, 'Control', params)
y_pred_T = calc_metrics(model, df_merged.loc[df_merged['Group'] == 'ESRD'], y_name, 'Disease', params)
y_pred_all = calc_metrics(model, df_merged, y_name, 'All', params)
params_df = pd.DataFrame({'Feature': list(params.keys()), 'Value': list(params.values())})
params_df.to_excel(f'{path}/clock/{data_type}/{target_part}/{y_name}/part({part})/params.xlsx', index=False)

print(params_df)

df_merged[f'{data_type}_{y_name}_{target_part}'] = y_pred_all

# = pd.concat([X_C_df, X_T_df])
# df_merged= pd.merge(df_merged, tmp_df[['ID', 'CKDAge']], on=['ID'], how='inner')
df_merged.to_excel(f'{path}/table_part({part}).xlsx', index=False)

