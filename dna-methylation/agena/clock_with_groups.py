from functools import reduce
import numpy as np
import pandas as pd
from sklearn.model_selection import RepeatedKFold, GridSearchCV
from sklearn.linear_model import ElasticNet
import os
import copy
from sklearn.metrics import mean_squared_error, mean_absolute_error
import pickle


def calc_metrics(model, X, y, comment, params):
    y_pred = model.predict(X)
    score = model.score(X, y)
    rmse = np.sqrt(mean_squared_error(y, y_pred))
    mae = mean_absolute_error(y, y_pred)
    params[f'{comment} R2'] = score
    params[f'{comment} RMSE'] = rmse
    params[f'{comment} MAE'] = mae
    return y_pred


is_pkl = True

dataset = 'GSE52588'
dataset_beta_suffix = ''
dataset_pheno_suffix = ''
outcome = 'age'

agena_path = f"E:/YandexDisk/Work/pydnameth/unn_epic/agena"
global_path = f"E:/YandexDisk/Work/pydnameth"

table_path = f"{agena_path}/{dataset}"
if not os.path.exists(table_path):
    os.makedirs(table_path)

cpgs = np.loadtxt(F"{agena_path}/cpgs(17).txt", dtype='str')

table_fn = f"{table_path}/table.xlsx"
if not os.path.isfile(table_fn):

    if is_pkl:
        data_fn = f"{global_path}/{dataset}/data.pkl"
        f = open(data_fn, 'rb')
        data = pickle.load(f)
        f.close()
        beta = data['beta']
        pheno = data['pheno']
    else:
        beta_fn = f"{global_path}/{dataset}/betas{dataset_beta_suffix}.txt"
        df = pd.read_csv(beta_fn, delimiter = "\t", index_col='IlmnID')
        beta = df.T

        pheno_fn = f"{global_path}/{dataset}/observables{dataset_pheno_suffix}.txt"
        df = pd.read_csv(pheno_fn, delimiter="\t", index_col='ID')
        pheno = df

    remaining_cpgs = list(set.intersection(set(cpgs), set(list(beta.columns.values))))
    missed_cpgs = list(set(cpgs) - set(remaining_cpgs))
    print(f"missed_cpgs: {missed_cpgs}")
    beta = beta[remaining_cpgs]
    ids_beta = [x.split('_')[0] for x in beta.index.values.tolist()]

    ids_pheno = pheno.index.values.tolist()
    beta.index = ids_pheno

    print(f"is equal ids: {ids_pheno == ids_beta}")
    print(f"is equal lens: {len(ids_pheno) == len(ids_beta)}")

    dfs = [beta, pheno]
    table = reduce(lambda left, right: pd.merge(left, right, left_index=True, right_index=True), dfs)
    table.index.name = "ID"

    table.to_excel(table_fn, index=True, index_label="ID")

else:
    table = pd.read_excel(table_fn, engine='openpyxl', index_col='ID')
    remaining_cpgs = list(set.intersection(set(cpgs), set(list(table.columns.values))))

X_all = table[list(remaining_cpgs)].to_numpy()
y_all = table[outcome].to_numpy()

X_DS_df = table.loc[table['group'] == 'DS']
X_DS = X_DS_df[list(remaining_cpgs)].to_numpy()
y_DS = X_DS_df[outcome].to_numpy()

X_S_df = table.loc[table['group'] == 'Siblings']
X_S = X_S_df[list(remaining_cpgs)].to_numpy()
y_S = X_S_df[outcome].to_numpy()

X_M_df = table.loc[table['group'] == 'Mothers']
X_M = X_M_df[list(remaining_cpgs)].to_numpy()
y_M = X_M_df[outcome].to_numpy()

X_NDS_df = table.loc[table['group'] != 'DS']
X_NDS = X_NDS_df[list(remaining_cpgs)].to_numpy()
y_NDS = X_NDS_df[outcome].to_numpy()

X_target = X_NDS
y_target = y_NDS


scoring = 'r2'
cv = RepeatedKFold(n_splits=3, n_repeats=5, random_state=1)
model_type = ElasticNet(max_iter=1000, tol=0.0001)

# define grid
alphas = np.logspace(-5, 3, 50)
l1_ratios = np.linspace(0.0, 1.0, 11)

grid = dict()
grid['alpha'] = alphas
grid['l1_ratio'] = l1_ratios

search = GridSearchCV(estimator=model_type, scoring=scoring, param_grid=grid, cv=cv, verbose=3)
results = search.fit(X_target, y_target)

model = results.best_estimator_

score = model.score(X_target, y_target)
params = copy.deepcopy(results.best_params_)

searching_process = pd.DataFrame(results.cv_results_)
searching_process.to_excel(f"{table_path}/searching_process.xlsx", index=False)

model_dict = {'feature': ['Intercept'], 'coef': [model.intercept_]}
num_features = 0
for f_id, f in enumerate(remaining_cpgs):
    coef = model.coef_[f_id]
    if abs(coef) > 0:
        model_dict['feature'].append(f)
        model_dict['coef'].append(coef)
        num_features += 1
model_df = pd.DataFrame(model_dict)
model_df.to_excel(f'{table_path}/clock.xlsx', index=False)

y_pred = model.predict(X_all)
table[f"{outcome}_pred"] = y_pred
table.to_excel(table_fn, index=True, index_label="ID")

y_pred_DS = calc_metrics(model, X_DS, y_DS, 'DS', params)
y_pred_S = calc_metrics(model, X_S, y_S, 'Siblings', params)
y_pred_M = calc_metrics(model, X_M, y_M, 'Mothers', params)
y_pred_NDS = calc_metrics(model, X_NDS, y_NDS, 'NDS', params)
y_pred_all = calc_metrics(model, X_all, y_all, 'All', params)
params['num_features'] = num_features
params_df = pd.DataFrame({'Feature': list(params.keys()), 'Value': list(params.values())})
params_df.to_excel(f'{table_path}/params.xlsx', index=False)
