import pandas as pd
from scipy.stats import mannwhitneyu
from scipy.stats import kruskal

path = "C:/Users/user/Downloads"

tbl = pd.read_excel(f"{path}/p_value_2_cpg2.xlsx", index_col='Subject')
df_ctrl = tbl.loc[tbl['Status'] == 'Control', :]
df_case = tbl.loc[tbl['Status'] == 'Disease', :]

cpgs = ['cg19940537', 'cg00004883']
result = {'CpG': cpgs, 'pval_mw': [], 'pval_kw': []}

for cpg_id, cpg in enumerate(cpgs):
    data_1 = df_ctrl[cpg].values
    data_2 = df_case[cpg].values
    stat, p = mannwhitneyu(data_1, data_2)
    result['pval_mw'].append(p)
    stat, p = kruskal(data_1, data_2)
    result['pval_kw'].append(p)

pd.DataFrame(result).to_excel(f"{path}/pvals.xlsx", index=False)
