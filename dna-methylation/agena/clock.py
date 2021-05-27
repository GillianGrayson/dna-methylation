from functools import reduce
import numpy as np
import pandas as pd
from sklearn.model_selection import RepeatedKFold, GridSearchCV
from sklearn.linear_model import ElasticNet
import os
import copy
from sklearn.metrics import mean_squared_error, mean_absolute_error


dataset = 'GSE55763'
outcome = 'age'

agena_path = f"E:/YandexDisk/Work/pydnameth/unn_epic/agena"
global_path = f"E:/YandexDisk/Work/pydnameth"

table_path = f"{agena_path}/{dataset}"
if not os.path.exists(table_path):
    os.makedirs(table_path)

cpgs = np.loadtxt(F"{agena_path}/cpgs(11).txt", dtype='str')

table_fn = f"{table_path}/table.xlsx"
if not os.path.isfile(table_fn):

    beta_fn = f"{global_path}/{dataset}/betas.txt"
    df = pd.read_csv(beta_fn, delimiter = "\t", index_col='ID_REF')
    beta = df.T
    beta = beta[cpgs]
    ids_beta = [x.split('_')[0] for x in beta.index.values.tolist()]


    pheno_fn = f"{global_path}/{dataset}/observables.txt"
    df = pd.read_csv(pheno_fn, delimiter = "\t", index_col='geo_accession')
    pheno = df
    ids_pheno = pheno.index.values.tolist()
    beta.index = ids_pheno

    print(f"is equal ids: {ids_pheno == ids_beta}")
    print(f"is equal lens: {len(ids_pheno) == len(ids_beta)}")

    dfs = [beta, pheno]
    table = reduce(lambda left, right: pd.merge(left, right, left_index=True, right_index=True), dfs)
    table.index.name = "ID"

    table.to_excel(table_fn, index=True, index_label="ID")

else:
    table = pd.read_excel(table_fn, engine='openpyxl')

X = table[list(cpgs)].to_numpy()
y = table[outcome].to_numpy()

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
results = search.fit(X, y)

model = results.best_estimator_

score = model.score(X, y)
params = copy.deepcopy(results.best_params_)

searching_process = pd.DataFrame(results.cv_results_)
searching_process.to_excel(f"{table_path}/searching_process.xlsx", index=False)

model_dict = {'feature': ['Intercept'], 'coef': [model.intercept_]}
num_features = 0
for f_id, f in enumerate(cpgs):
    coef = model.coef_[f_id]
    if abs(coef) > 0:
        model_dict['feature'].append(f)
        model_dict['coef'].append(coef)
        num_features += 1
model_df = pd.DataFrame(model_dict)
model_df.to_excel(f'{table_path}/clock.xlsx', index=False)

y_pred = model.predict(X)
table[f"{outcome}_pred"] = y_pred
table.to_excel(table_fn, index=True, index_label="ID")
score = model.score(X, y)
rmse = np.sqrt(mean_squared_error(y_pred, y))
mae = mean_absolute_error(y_pred, y)
params["R2"] = score
params["RMSE"] = rmse
params["MAE"] = mae
params['num_features'] = num_features

params_df = pd.DataFrame({'Feature': list(params.keys()), 'Value': list(params.values())})
params_df.to_excel(f'{table_path}/params.xlsx', index=False)

