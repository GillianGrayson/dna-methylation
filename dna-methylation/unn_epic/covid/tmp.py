import numpy as np
import pandas as pd
import os
import re
import pingouin as pg
from scipy import stats
from operator import sub
from tqdm import tqdm
from statsmodels.stats.multitest import multipletests


dataset_path = "E:/YandexDisk/Work/pydnameth/unn_epic"

data_type = 'betas'
norm = 'fun'
part = 'v1'
config = '0.01_0.10_0.10'

fn_obs = f"{dataset_path}/observables_part({part})"
if not os.path.isfile(f"{fn_obs}.pkl"):
    obs = pd.read_excel(f"{fn_obs}.xlsx", index_col=0, engine='openpyxl')
    obs.to_pickle(f"{fn_obs}.pkl")
else:
    obs = pd.read_pickle(f"{fn_obs}.pkl")


fn_betas = f"{dataset_path}/betas_part({part})_config({config})_norm({norm})"
if not os.path.isfile(f"{fn_betas}.pkl"):
    betas = pd.read_csv(f"{fn_betas}.txt", delimiter = "\t", index_col=0)
    betas.to_pickle(f"{fn_betas}.pkl")
else:
    betas = pd.read_pickle(f"{fn_betas}.pkl")

fn_ann = f"{dataset_path}/annotations"
if not os.path.isfile(f"{fn_ann}.pkl"):
    ann = pd.read_csv(f"{fn_ann}.txt", delimiter = "\t", index_col=0)
    ann.to_pickle(f"{fn_ann}.pkl")
else:
    ann = pd.read_pickle(f"{fn_ann}.pkl")

obs_bef = obs.loc[(obs['Sample_Chronology'] == 1) & (obs['ID'] != 'I64_1')].copy(deep=True)
obs_bef.loc[:, 'BetasColumn'] = ["X" + x for x in list(obs_bef.index)]
sn_bef = obs_bef['BetasColumn'].to_list()
obs_bef['COVID'].replace('before', 'yes', inplace=True)

obs_aft = obs.loc[(obs['Sample_Chronology'] == 2) & (obs['ID'] != 'I64_2')].copy(deep=True)
obs_aft.loc[:, 'BetasColumn'] = ["X" + x for x in list(obs_aft.index)]
sn_aft = obs_aft['BetasColumn'].to_list()
obs_aft['COVID'].replace('after', 'yes', inplace=True)

IDs_aft = obs_aft['ID'].to_list()
to_remove = ['+', ' (1)']
p = re.compile('|'.join(map(re.escape, to_remove))) # escape to handle metachars
IDs_aft = [p.sub('', s) for s in IDs_aft]
obs_aft['ID'] = IDs_aft

for l1,l2 in zip(obs_bef['ID'].to_list(), obs_aft['ID'].to_list()):
    if l1 != l2:
        raise ValueError('Wrong ID order in after and before')

betas_bef = betas[sn_bef].copy(deep=True)
betas_aft = betas[sn_aft].copy(deep=True)

metrics = [
    'cpg',
    'genes',
    'mean_bef_ctrl',
    'mean_aft_ctrl',
    'mean_bef_case',
    'mean_aft_case',
]
res = dict((x, []) for x in metrics)

kw_dict = {
    'betas_bef': [0] * obs_bef.shape[0],
    'betas_aft': [0] * obs_bef.shape[0],
    'betas_diff': [0] * obs_bef.shape[0],
    'group': obs_bef['COVID'].to_list(),
    'subject': obs_bef['ID'].to_list()
}
kw_df = pd.DataFrame(kw_dict)

for cpg in tqdm(betas_bef.index, mininterval=5, desc='cpgs_full'):
    res['cpg'].append(cpg)

    raw_genes = ann.loc[cpg, 'UCSC_RefGene_Name']
    genes = ''
    if isinstance(raw_genes, str):
        if raw_genes != '':
            genes = ';'.join(list(set(raw_genes.split(';'))))
    res['genes'].append(genes)

    dep_bef = betas_bef.loc[cpg, :].values.tolist()
    dep_aft = betas_aft.loc[cpg, :].values.tolist()

    kw_df.loc[:, 'betas_bef'] = list(dep_bef)
    kw_df.loc[:, 'betas_aft'] = list(dep_aft)
    kw_df.loc[:, 'betas_diff'] = list(map(sub, dep_aft, dep_bef))
    vals_bef_ctrl = kw_df.loc[kw_df['group'] == 'no', 'betas_bef'].values
    vals_aft_ctrl = kw_df.loc[kw_df['group'] == 'no', 'betas_aft'].values
    vals_bef_case = kw_df.loc[kw_df['group'] == 'yes', 'betas_bef'].values
    vals_aft_case = kw_df.loc[kw_df['group'] == 'yes', 'betas_aft'].values
    res['mean_bef_ctrl'].append(np.mean(vals_bef_ctrl))
    res['mean_aft_ctrl'].append(np.mean(vals_aft_ctrl))
    res['mean_bef_case'].append(np.mean(vals_bef_case))
    res['mean_aft_case'].append(np.mean(vals_aft_case))

if not os.path.exists(f'{dataset_path}/covid'):
    os.makedirs(f'{dataset_path}/covid')

res_df = pd.DataFrame(res)
fn_save = f"{dataset_path}/covid/tmp.xlsx"
res_df.to_excel(fn_save, index=False)
