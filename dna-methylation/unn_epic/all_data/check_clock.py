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
      rmse = np.sqrt(mean_squared_error(y, y_pred))
      mae = mean_absolute_error(y, y_pred)
      params[f'{comment} R2'] = score
      params[f'{comment} RMSE'] = rmse
      params[f'{comment} MAE'] = mae
      return y_pred

features_type = 'immuno'

y_name = 'Age'
part = 'v2'

target_part = 'Control'

path = f'E:/YandexDisk/Work/pydnameth/unn_epic/all_data'
fn = 'E:/YandexDisk/Work/pydnameth/unn_epic/all_data/raw/immuno_clocks.xlsx'
df_merged = pd.read_excel(fn, converters={'ID': str}, engine='openpyxl')
model_df = pd.read_excel(f'{path}/clock/{features_type}/{target_part}/{y_name}/part({part})/clock.xlsx', engine='openpyxl')

features = model_df['feature'].to_list()
coefs = model_df['coef'].to_list()

predicted = [coefs[0]] * df_merged.shape[0]
for index, row in df_merged.iterrows():
    for feat_id in range(1, len(features)):
        predicted[index] += row[features[feat_id]] * coefs[feat_id]

df_merged[f'Immuno{y_name}'] = predicted

df_merged.to_excel(fn, index=False)
