from pydnameth.infrastucture.path import get_data_base_path
import numpy as np
import pickle
import pandas as pd
from tqdm import tqdm


path = 'E:/YandexDisk/Work/pydnameth/unn_epic'

resid_suffix = "_part(v1)_config(0.01_0.10_0.10)_norm(fun)_cells(['Bcell', 'CD4T', 'CD8T', 'Neu', 'NK'])"

fn_dict = path + '/' + 'residuals_dict' + resid_suffix + '.pkl'
fn_missed_dict = path + '/' + 'residuals_missed_dict' + resid_suffix + '.pkl'
fn_data = path + '/' + 'residuals' + resid_suffix + '.npz'

betas_df = pd.read_pickle(f"{path}/betas_part(v1)_config(0.01_0.10_0.10)_norm(fun)_df.pkl")

f = open(fn_dict, 'rb')
residuals_dict = pickle.load(f)
f.close()

f = open(fn_missed_dict, 'rb')
residuals_missed_dict = pickle.load(f)
f.close()

data = np.load(fn_data)
residuals_data = data['data']

for cpg in tqdm(betas_df.index, mininterval=5, desc='cpgs_full'):
    res_data = residuals_data[residuals_dict[cpg], :]
    betas_df.loc[cpg,:] = res_data

betas_df.to_pickle(f"{path}/residual_part(v1)_config(0.01_0.10_0.10)_norm(fun)_cells(['Bcell', 'CD4T', 'CD8T', 'Neu', 'NK'])_df.pkl")

