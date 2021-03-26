import pandas as pd
from functools import reduce
import collections
from statsmodels.stats.multitest import multipletests


path = f'E:/YandexDisk/Work/pydnameth/unn_epic/covid'

df_1 = pd.read_excel(f'{path}/betas.xlsx', converters={'ID': str}, engine='openpyxl')
df_2 = pd.read_excel(f'{path}/tmp.xlsx', converters={'ID': str}, engine='openpyxl')


data_frames = [df_1, df_2]
df_merged = reduce(lambda left, right: pd.merge(left, right, on=['cpg']), data_frames)

metrics = [
    'mixed_anova_pval',
    'diff_kw_pval',
    'Group_pval',
    'Sex_pval',
    'Age_pval',
    'Sex_Age_pval'
]

for metric in metrics:
    reject, pvals_corr, alphacSidak, alphacBonf = multipletests(df_merged[metric].to_list(), 0.05, method='fdr_bh')
    df_merged.loc[:, f'{metric}_fdr_bh'] = pvals_corr
    reject, pvals_corr, alphacSidak, alphacBonf = multipletests(df_merged[metric].to_list(), 0.05, method='bonferroni')
    df_merged.loc[:, f'{metric}_bonferroni'] = pvals_corr

df_merged.to_excel(f'{path}/current_table.xlsx', index=False)