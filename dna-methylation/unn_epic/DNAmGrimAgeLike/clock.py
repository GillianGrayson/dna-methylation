import pandas as pd
import copy
import numpy as np
import os
from tqdm import tqdm
from sklearn.linear_model import ElasticNet, ElasticNetCV
from sklearn.model_selection import RepeatedKFold, GridSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from pathlib import Path
import pickle
from scipy import stats


def calc_metrics(model, X, y, comment, params):
    y_pred = model.predict(X)
    score = model.score(X, y)
    rmse = np.sqrt(mean_squared_error(y, y_pred))
    mae = mean_absolute_error(y, y_pred)
    params[f'{comment} R2'] = score
    params[f'{comment} RMSE'] = rmse
    params[f'{comment} MAE'] = mae
    r, pval = stats.pearsonr(y, y_pred)
    params[f'{comment}_pearson_r'] = r
    params[f'{comment}_pearson_pval'] = pval
    return y_pred

version = "DNAmGrimAge_v2"
target_part = 'Control'
pearson_r_lim = 0.35

path = f'E:/YandexDisk/Work/pydnameth/unn_epic'
params_df = pd.read_excel(f'{path}/all_data/{version}/{target_part}/params.xlsx', engine='openpyxl')
params_df.set_index("marker", inplace=True)

params_df = params_df.loc[(params_df["Control_pearson_r"] > pearson_r_lim) & (params_df["ESRD_pearson_r"] > pearson_r_lim), :]
markers = params_df.index.values.tolist()
markers = [s + "_pred" for s in markers]

path = f'E:/YandexDisk/Work/pydnameth/unn_epic'
df = pd.read_excel(f'{path}/all_data/{version}/{target_part}/table.xlsx', engine='openpyxl')
df.set_index("Sample_Name", inplace=True)

X_C_df = df.loc[df['Group'] == 'Control']
X_C = X_C_df[markers].to_numpy()
y_C = X_C_df["Age"].to_numpy()

X_T_df = df.loc[df['Group'] == 'ESRD']
X_T = X_T_df[markers].to_numpy()
y_T = X_T_df["Age"].to_numpy()

X_all = df[markers].to_numpy()
y_all = df["Age"].to_numpy()

if target_part == 'All':
    X_target = X_all
    y_target = y_all
elif target_part == 'Control':
    X_target = X_C
    y_target = y_C
else:
    raise ValueError("Unsupported target_part")

scoring = 'r2'
cv = RepeatedKFold(n_splits=3, n_repeats=5, random_state=1)
model_type = ElasticNet()

alphas = np.logspace(-4, 4, 10)
l1_ratios = [0.5]

grid = dict()
grid['alpha'] = alphas
grid['l1_ratio'] = l1_ratios
search = GridSearchCV(estimator=model_type, scoring=scoring, param_grid=grid, cv=cv, verbose=3)
results = search.fit(X_target, y_target)

model = results.best_estimator_

score = model.score(X_target, y_target)
params = copy.deepcopy(results.best_params_)

model_dict = {'feature': ['Intercept'], 'coef': [model.intercept_]}
num_features = 0
for f_id, f in enumerate(markers):
    coef = model.coef_[f_id]
    if abs(coef) > 0:
        model_dict['feature'].append(f)
        model_dict['coef'].append(coef)
        num_features += 1
model_df = pd.DataFrame(model_dict)

Path(f'{path}/all_data/{version}/{target_part}/clock').mkdir(parents=True, exist_ok=True)
model_df.to_excel(f'{path}/all_data/{version}/{target_part}/clock/clock.xlsx', index=False)

y_pred_C = calc_metrics(model, X_C, y_C, 'Control', params)
y_pred_T = calc_metrics(model, X_T, y_T, 'Disease', params)
y_pred_all = calc_metrics(model, X_all, y_all, 'All', params)
params['num_features'] = num_features
params_df = pd.DataFrame({'Feature': list(params.keys()), 'Value': list(params.values())})
params_df.to_excel(f'{path}/all_data/{version}/{target_part}/clock/params.xlsx', index=False)

print(params_df)

df[f'DNAmImmunoAge_{target_part}'] = y_pred_all
df.to_excel(f'{path}/all_data/{version}/{target_part}/tmp.xlsx', index=True)