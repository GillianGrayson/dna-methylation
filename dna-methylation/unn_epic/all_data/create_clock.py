import pandas as pd
from sklearn.linear_model import ElasticNetCV
from sklearn.model_selection import RepeatedKFold
from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np
import pickle
from pathlib import Path


def calc_metrics(model, X, y, comment):
      y_pred = model.predict(X)
      score = model.score(X, y)
      rmse = np.sqrt(mean_squared_error(y_pred, y))
      mae = mean_absolute_error(y_pred, y)
      print(f'{comment} score: {score}')
      print(f'{comment} rmse: {rmse}')
      print(f'{comment} mae: {mae}')
      return y_pred

y_name = 'DNAmAge'
part = 'wo_noIntensity_detP_subset'

path = f'E:/YandexDisk/Work/pydnameth/unn_epic/all_data'
df_merged = pd.read_excel(f'{path}/part({part}).xlsx', converters={'ID': str}, engine='openpyxl')

with open(f'{path}/features_list.txt') as f:
    target_features = f.read().splitlines()

X_C_df = df_merged.loc[df_merged['Sample_Group'] == 'C']
X_C = X_C_df[list(target_features)].to_numpy()
y_C = X_C_df[y_name].to_numpy()

X_T_df = df_merged.loc[df_merged['Sample_Group'] == 'T']
X_T = X_T_df[list(target_features)].to_numpy()
y_T = X_T_df[y_name].to_numpy()

X_all = df_merged[list(target_features)].to_numpy()
y_all = df_merged[y_name].to_numpy()

ratios = np.linspace(0, 1, 11)
alphas = np.logspace(-5, 2, 8)

cv = RepeatedKFold(n_splits=5, n_repeats=100, random_state=1)
model = ElasticNetCV(l1_ratio=ratios, alphas=alphas, cv=cv)
model.fit(X_all, y_all)

model_dict = {'feauture': ['Intercept'], 'coef': [model.intercept_]}
for f_id, f in enumerate(target_features):
      coef = model.coef_[f_id]
      if abs(coef) > 0:
            model_dict['feauture'].append(f)
            model_dict['coef'].append(coef)
model_df = pd.DataFrame(model_dict)

Path(f'{path}/clock/{y_name}/part({part})').mkdir(parents=True, exist_ok=True)
model_df.to_excel(f'{path}/clock/{y_name}/part({part})/all_biochemMultiplex.xlsx', index=False)

with open(f'{path}/clock/{y_name}/part({part})/all_biochemMultiplex.pkl', 'wb') as handle:
    pickle.dump(model, handle, protocol=pickle.HIGHEST_PROTOCOL)

print(f'alpha: {model.alpha_}')
print(f'l1_ratio: {model.l1_ratio_}')

y_pred_C = calc_metrics(model, X_C, y_C, 'ctrl')
y_pred_T = calc_metrics(model, X_T, y_T, 'ckd')
y_pred_all = calc_metrics(model, X_all, y_all, 'all')

df_merged[f'CKDAge_{y_name}_all'] = y_pred_all

# = pd.concat([X_C_df, X_T_df])
#df_merged= pd.merge(df_merged, tmp_df[['ID', 'CKDAge']], on=['ID'], how='inner')
df_merged.to_excel(f'{path}/part(wo_noIntensity_detP_subset).xlsx', index=False)
