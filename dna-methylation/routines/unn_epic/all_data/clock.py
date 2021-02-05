import pandas as pd
from functools import reduce
from sklearn.linear_model import ElasticNetCV
from sklearn.model_selection import RepeatedKFold
from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np
import pickle


def calc_metrics(model, X, y, comment):
      y_pred = model.predict(X)
      score = model.score(X, y)
      rmse = np.sqrt(mean_squared_error(y_pred, y))
      mae = mean_absolute_error(y_pred, y)
      print(f'{comment} score: {score}')
      print(f'{comment} rmse: {rmse}')
      print(f'{comment} mae: {mae}')
      return y_pred

path = f'E:/YandexDisk/Work/pydnameth/unn_epic/all_data'

df_main = pd.read_excel(f'{path}/part(wo_noIntensity_detP).xlsx', converters={'ID': str})
df_biochem = pd.read_excel(f'{path}/markers/FGF23_FGF21_Klotho_GDF15.xlsx', converters={'ID': str})
df_multiplex = pd.read_excel(f'{path}/markers/MULTIPLEX_20_11_2020_xtd_ver1.xlsx', converters={'ID': str})

target_columns = set.union(set(df_biochem.columns), set(df_multiplex.columns))
target_columns.remove('ID')

data_frames = [df_main, df_biochem, df_multiplex]
df_merged = reduce(lambda left, right: pd.merge(left, right, on=['ID']), data_frames)
df_merged.to_excel(f'{path}/part(wo_noIntensity_detP_subset).xlsx', index=False)

X_C_df = df_merged.loc[df_merged['Sample_Group'] == 'C', list(target_columns) + ['DNAmPhenoAge']]
X_C = X_C_df[list(target_columns)].to_numpy()
y_C = X_C_df['DNAmPhenoAge'].to_numpy()

X_T_df = df_merged.loc[df_merged['Sample_Group'] == 'T', list(target_columns) + ['DNAmPhenoAge']]
X_T = X_T_df[list(target_columns)].to_numpy()
y_T = X_T_df['DNAmPhenoAge'].to_numpy()

cv = RepeatedKFold(n_splits=5, n_repeats=100, random_state=1)
model = ElasticNetCV(cv=cv)
model.fit(X_C, y_C)

model_dict = {'feauture': ['Intercept'], 'coef': [model.intercept_]}
for f_id, f in enumerate(target_columns):
      coef = model.coef_[f_id]
      if abs(coef) > 0:
            model_dict['feauture'].append(f)
            model_dict['coef'].append(coef)
model_df = pd.DataFrame(model_dict)
model_df.to_excel(f'{path}/clock/biochemMultiplex_part(ctrl_wo_noIntensity_detP_subset).xlsx', index=False)

with open(f'{path}/clock/biochemMultiplex_part(ctrl_wo_noIntensity_detP_subset).pkl', 'wb') as handle:
    pickle.dump(model, handle, protocol=pickle.HIGHEST_PROTOCOL)

print(f'alpha: {model.alpha_}')
print(f'l1_ratio: {model.l1_ratio_}')

y_pred_C = calc_metrics(model, X_C, y_C, 'ctrl')
y_pred_T = calc_metrics(model, X_T, y_T, 'ckd')

X_C_df['CKDAge'] = y_pred_C
X_C_df.to_excel(f'{path}/table/biochemMultiplex_part(ctrl_wo_noIntensity_detP_subset).xlsx', index=False)

X_T_df['CKDAge'] = y_pred_T
X_T_df.to_excel(f'{path}/table/biochemMultiplex_part(ckd_wo_noIntensity_detP_subset).xlsx', index=False)

a = 1
