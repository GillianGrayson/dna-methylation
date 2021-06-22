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


part = "v1"
config = "0.01_0.10_0.10"
norm = "fun"

target_part = 'Control'

path = f'E:/YandexDisk/Work/pydnameth/unn_epic'
df = pd.read_excel(f'{path}/all_data/DNAmGrimAgeLike/{target_part}/table.xlsx', engine='openpyxl')
df.set_index("Sample_Name", inplace=True)

markers = ["IL12Bp70"]

for marker_id, marker in tqdm(enumerate(markers)):

    C_df = df.loc[df['Group'] == 'Control']
    T_df = df.loc[df['Group'] == 'ESRD']
    A_df = df

    y_real = C_df[marker].to_numpy()
    y_pred = C_df[f"{marker}_pred"].to_numpy()

    r2_C = r2_score(y_real, y_pred)
    r_C, pval_C = stats.pearsonr(y_real, y_pred)
    slope, intercept, r, p, se = stats.linregress(y_real, y_pred)

    y_real = T_df[marker].to_numpy()
    y_pred = T_df[f"{marker}_pred"].to_numpy()
    r2_T = r2_score(y_real, y_pred)
    r_T, pval_T = stats.pearsonr(y_real, y_pred)

    y_real = A_df[marker].to_numpy()
    y_pred = A_df[f"{marker}_pred"].to_numpy()
    r2_A = r2_score(y_real, y_pred)
    r_A, pval_A = stats.pearsonr(y_real, y_pred)

    ololo = 1
