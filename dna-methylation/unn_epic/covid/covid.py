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
    'mixed_anova_pval',
    'diff_kw_pval'
]
res = dict((x, []) for x in metrics)

anova_dict = {
    'betas': [0] * (obs_bef.shape[0] + obs_aft.shape[0]),
    'group': obs_bef['COVID'].to_list() + obs_aft['COVID'].to_list(),
    'time': ['before'] * obs_bef.shape[0] + ['after'] * obs_aft.shape[0],
    'subject': obs_bef['ID'].to_list() + obs_aft['ID'].to_list()
}
anova_df = pd.DataFrame(anova_dict)

kw_dict = {
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

    anova_df.loc[:, 'betas'] = dep_bef + dep_aft
    aov = pg.mixed_anova(dv='betas', within='time', between='group', subject='subject', data=anova_df)
    res['mixed_anova_pval'].append(aov.loc[aov['Source'] == 'Interaction', 'p-unc'].values[0])

    kw_df.loc[:, 'betas_diff'] = list(map(sub, dep_aft, dep_bef))
    vals_1 = kw_df.loc[kw_df['group'] == 'no', 'betas_diff'].values
    vals_2 = kw_df.loc[kw_df['group'] == 'yes', 'betas_diff'].values
    _, kw_p_value = stats.kruskal(vals_1, vals_2)
    res['diff_kw_pval'].append(kw_p_value)

for metric in metrics[2::]:
    reject, pvals_corr, alphacSidak, alphacBonf = multipletests(res[metric], 0.05, method='fdr_bh')
    res[f'{metric}_fdr_bh'] = pvals_corr
    reject, pvals_corr, alphacSidak, alphacBonf = multipletests(res[metric], 0.05, method='bonferroni')
    res[f'{metric}_bonferroni'] = pvals_corr

if not os.path.exists(f'{dataset_path}/covid'):
    os.makedirs(f'{dataset_path}/covid')

res_df = pd.DataFrame(res)
fn_save = f"{dataset_path}/covid/table.xlsx"
res_df.to_excel(fn_save, index=False)
