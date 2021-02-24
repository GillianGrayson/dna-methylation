import pandas as pd
from sklearn.linear_model import ElasticNet, ElasticNetCV
from sklearn.model_selection import RepeatedKFold, GridSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
import pickle
from pathlib import Path
import os
import copy


def calc_metrics(model, X, y, comment, params):
      y_pred = model.predict(X)
      score = model.score(X, y)
      rmse = np.sqrt(mean_squared_error(y_pred, y))
      mae = mean_absolute_error(y_pred, y)
      params[f'{comment} R2'] = score
      params[f'{comment} RMSE'] = rmse
      params[f'{comment} MAE'] = mae
      return y_pred

y_name = 'DNAmAge'
part = 'wo_noIntensity_detP_H17+_negDNAmPhenoAge'

target_part = 'Control'

path = f'E:/YandexDisk/Work/pydnameth/unn_epic/all_data'
df_merged = pd.read_excel(f'{path}/table_part({part}).xlsx', converters={'ID': str}, engine='openpyxl')

save_path = f'{path}/clock/{target_part}/{y_name}/part({part})'
if not os.path.exists(save_path):
      os.makedirs(save_path)

with open(f'{path}/features_list.txt') as f:
    target_features = f.read().splitlines()

X_C_df = df_merged.loc[df_merged['Group'] == 'Control']
X_C = X_C_df[list(target_features)].to_numpy()
y_C = X_C_df[y_name].to_numpy()

X_T_df = df_merged.loc[df_merged['Group'] == 'Disease']
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
      raise ValueError("Unsopported target_part")

# define model evaluation method
cv = RepeatedKFold(n_splits=3, n_repeats=10, random_state=1)

# define model
model_type = ElasticNet(max_iter=10000, tol=0.001)
# define grid
grid = dict()
grid['alpha'] = np.logspace(-5, 1, 7)
grid['l1_ratio'] = np.linspace(0.0, 1.0, 11)
# define search
scoring = 'r2'
search = GridSearchCV(estimator=model_type, scoring=scoring, param_grid=grid, cv=cv, verbose=3)
# perform the search
results = search.fit(X_target, y_target)
# summarize

model = search.best_estimator_

score = model.score(X_target, y_target)

params = copy.deepcopy(results.best_params_)

searching_process = pd.DataFrame(search.cv_results_)
searching_process.to_excel(f'{path}/clock/{target_part}/{y_name}/part({part})/searching_process_{scoring}.xlsx', index=False)

model_dict = {'feauture': ['Intercept'], 'coef': [model.intercept_]}
num_features = 0
for f_id, f in enumerate(target_features):
      coef = model.coef_[f_id]
      if abs(coef) > 0:
            model_dict['feauture'].append(f)
            model_dict['coef'].append(coef)
            num_features += 1
model_df = pd.DataFrame(model_dict)

Path(f'{path}/clock/{y_name}/part({part})').mkdir(parents=True, exist_ok=True)
model_df.to_excel(f'{path}/clock/{target_part}/{y_name}/part({part})/clock.xlsx', index=False)

with open(f'{path}/clock/{target_part}/{y_name}/part({part})/clock.pkl', 'wb') as handle:
    pickle.dump(model, handle, protocol=pickle.HIGHEST_PROTOCOL)

y_pred_C = calc_metrics(model, X_C, y_C, 'Control', params)
y_pred_T = calc_metrics(model, X_T, y_T, 'Disease', params)
y_pred_all = calc_metrics(model, X_all, y_all, 'All', params)
params['num_features'] = num_features
params_df = pd.DataFrame({'Feature': list(params.keys()), 'Value': list(params.values())})
params_df.to_excel(f'{path}/clock/{target_part}/{y_name}/part({part})/params.xlsx', index=False)

print(params_df)

df_merged[f'CKDAge_{y_name}_{target_part}'] = y_pred_all

# = pd.concat([X_C_df, X_T_df])
#df_merged= pd.merge(df_merged, tmp_df[['ID', 'CKDAge']], on=['ID'], how='inner')
df_merged.to_excel(f'{path}/table_part({part}).xlsx', index=False)
