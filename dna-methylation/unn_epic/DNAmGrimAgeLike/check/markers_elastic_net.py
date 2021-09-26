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
from sklearn.model_selection import cross_val_score


def calc_metrics(model, X, y, comment, params):
    y_pred = model.predict(X)
    R2 = model.score(X, y)
    RMSE = np.sqrt(mean_squared_error(y, y_pred))
    MAE = mean_absolute_error(y, y_pred)
    params[f'{comment}_R2'].append(R2)
    params[f'{comment}_RMSE'].append(RMSE)
    params[f'{comment}_MAE'].append(MAE)
    r, pval = stats.pearsonr(y, y_pred)
    params[f'{comment}_pearson_r'].append(r)
    params[f'{comment}_pearson_pval'].append(pval)
    return y_pred


part = "v1"
config = "0.01_0.10_0.10"
norm = "fun"

target_part = 'Control'

path = f'E:/YandexDisk/Work/pydnameth/unn_epic'
df_pheno = pd.read_excel(f'{path}/all_data/table_part(v2).xlsx', converters={'ID': str}, engine='openpyxl')
df_pheno["Sample_Name"] = 'X' + df_pheno["Sample_Name"]
df_pheno.set_index("Sample_Name", inplace=True)

with open(f'{path}/all_data/immuno.txt') as f:
    markers = f.read().splitlines()
with open(f'{path}/all_data/cytokines.txt') as f:
    tmp = f.read().splitlines()
    markers.extend(tmp)
df_pheno = df_pheno[markers + ["Age", "Sex", "Group"]]
df_pheno = pd.get_dummies(data=df_pheno, columns=["Sex"])

fn_betas = f"{path}/betas_part({part})_config({config})_norm({norm})"
if not os.path.isfile(f"{fn_betas}_df.pkl"):
    df_betas = pd.read_csv(f"{fn_betas}.txt", delimiter ="\t", index_col=0)
    df_betas.to_pickle(f"{fn_betas}_df.pkl")
else:
    df_betas = pd.read_pickle(f"{fn_betas}_df.pkl")
df_betas = df_betas.T
df_betas = df_betas.loc[df_pheno.index.values.tolist(), :]
features = df_betas.columns.values.tolist() + ["Sex_F", "Sex_M"]

df = pd.merge(df_pheno, df_betas, left_index=True, right_index=True)

metrics = {}
metrics['marker'] = []
metrics['num_features'] = []
for m in ["num_features", "l1_ratio", "alpha"]:
    metrics[m] = []
for m1 in ["R2", "RMSE", "MAE", "pearson_r", "pearson_pval"]:
    for m2 in ["Control", "ESRD", "All"]:
        metrics[f"{m2}_{m1}"] = []

markers = ["IL12Bp70"]

for marker_id, marker in tqdm(enumerate(markers)):

    X_C_df = df.loc[df['Group'] == 'Control']
    X_C = X_C_df[features].to_numpy()
    y_C = X_C_df[marker].to_numpy()

    X_T_df = df.loc[df['Group'] == 'ESRD']
    X_T = X_T_df[features].to_numpy()
    y_T = X_T_df[marker].to_numpy()

    X_all = df[features].to_numpy()
    y_all = df[marker].to_numpy()

    if target_part == 'All':
        X_target = X_all
        y_target = y_all
    elif target_part == 'Control':
        X_target = X_C
        y_target = y_C
    else:
        raise ValueError("Unsupported target_part")


    cv = RepeatedKFold(n_splits=3, n_repeats=2, random_state=1337)
    model_type = ElasticNet()

    scores = cross_val_score(model_type, X_target, y_target, scoring='neg_mean_absolute_error', cv=cv, n_jobs=-1)
    print('Mean MAE: %.3f (%.3f)' % (np.mean(scores), np.std(scores)))

    model_type.fit(X_target, y_target)
    y_pred = model_type.predict(X_all)
    R2 = model_type.score(X_all, y_all)
    RMSE = np.sqrt(mean_squared_error(y_all, y_pred))
    MAE = mean_absolute_error(y_all, y_pred)
    r, pval = stats.pearsonr(y_all, y_pred)


    grid = dict()
    grid['alpha'] = np.logspace(-4, 4, 10)
    grid['l1_ratio'] = [0.5]

    search = ElasticNetCV(cv=3, n_jobs=4)
    results = search.fit(X_target, y_target)

    model = results.best_estimator_

    score = model.score(X_target, y_target)
    print(score)

    model_dict = {'feature': ['Intercept'], 'coef': [model.intercept_]}
    num_features = 0
    for f_id, f in enumerate(features):
        coef = model.coef_[f_id]
        if abs(coef) > 0:
            model_dict['feature'].append(f)
            model_dict['coef'].append(coef)
            num_features += 1
    model_df = pd.DataFrame(model_dict)

    Path(f'{path}/all_data/DNAmGrimAgeLike/{target_part}/markers/{marker}').mkdir(parents=True, exist_ok=True)
    model_df.to_excel(f'{path}/all_data/DNAmGrimAgeLike/{target_part}/markers/{marker}/clock.xlsx', index=False)

    metrics['marker'].append(marker)
    metrics['num_features'].append(num_features)
    metrics["l1_ratio"].append(results.best_params_["l1_ratio"])
    metrics["alpha"].append(results.best_params_["alpha"])

    y_pred_C = calc_metrics(model, X_C, y_C, 'Control', metrics)
    y_pred_T = calc_metrics(model, X_T, y_T, 'ESRD', metrics)
    y_pred_all = calc_metrics(model, X_all, y_all, 'All', metrics)
    df_pheno[f'{marker}_pred'] = y_pred_all
    df_pheno.to_excel(f'{path}/all_data/DNAmGrimAgeLike/{target_part}/markers/table.xlsx', index=True)

    metrics_df = pd.DataFrame(metrics)
    metrics_df.to_excel(f'{path}/all_data/DNAmGrimAgeLike/{target_part}/markers/params.xlsx', index=False)

