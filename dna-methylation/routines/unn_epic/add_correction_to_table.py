from paper.routines.infrastructure.load.table import load_table_dict_xlsx, load_table_dict_pkl
from paper.routines.infrastructure.save.table import save_table_dict_xlsx, save_table_dict_pkl
from statsmodels.stats.multitest import multipletests


path = 'E:/YandexDisk/Work/pydnameth/unn_epic/bop/table/manova/3c48cd40ad58b06cc3b1f27e3c72554c'
fn = 'ABC'
target_metrics = ['Sample_Group_p_value_roy_3c48cd40']
limit = 0.05

table = {}
table['Number of'] = ['BoPs', 'Genes']

curr_fn = f'{path}/{fn}.xlsx'
data = load_table_dict_xlsx(curr_fn)

for metric in target_metrics:

    reject, pvals_corr, alphacSidak, alphacBonf = multipletests(
        data[metric],
        0.05,
        method='fdr_bh'
    )
    data[f'{metric}_fdr_bh'] = pvals_corr

    reject, pvals_corr, alphacSidak, alphacBonf = multipletests(
        data[metric],
        0.05,
        method='bonferroni'
    )
    data[f'{metric}_bonferroni'] = pvals_corr

save_table_dict_xlsx(f'{path}/{fn}_mod', data)
save_table_dict_pkl(f'{path}/{fn}_mod', data)
