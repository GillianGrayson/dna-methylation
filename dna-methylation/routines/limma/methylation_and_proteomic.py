from paper.routines.data.data_dicts import *
from paper.methods.approach_3.metal import *

path = 'E:/YandexDisk/Work/pydnameth/methylation_and_proteomic/limma'
datasets = ['GSE87571', 'GSE74193', 'liver']
data_type = 'm'

is_rewrite = False

data_dicts = {}
for dataset in datasets:
    target_fn = f'{path}/{dataset}/{dataset}_{data_type}_filtered.pkl'
    filtered = load_table_dict_pkl(target_fn)
    data_dicts[dataset] = filtered

ss_data_dicts = {}
aa_data_dicts = {}
ssaa_data_dicts = {}
for dataset in data_dicts:
    ss_metric = 'Sex_adj.P.Val'
    ss_val = 0.05
    aa_metric = 'Age_adj.P.Val'
    aa_val = 0.05

    ss_ids = np.where(np.asarray(data_dicts[dataset][ss_metric]) < ss_val)
    aa_ids = np.where(np.asarray(data_dicts[dataset][aa_metric]) < aa_val)
    ssaa_ids = np.where((np.asarray(data_dicts[dataset][ss_metric]) < ss_val) & (np.asarray(data_dicts[dataset][aa_metric]) < aa_val))
    ss_data_dicts[dataset] = {}
    aa_data_dicts[dataset] = {}
    ssaa_data_dicts[dataset] = {}
    for key in data_dicts[dataset]:
        ss_data_dicts[dataset][key] = np.asarray(data_dicts[dataset][key])[ss_ids]
        aa_data_dicts[dataset][key] = np.asarray(data_dicts[dataset][key])[aa_ids]
        ssaa_data_dicts[dataset][key] = np.asarray(data_dicts[dataset][key])[ssaa_ids]

ss_dicts_full, ss_dicts_diff = process_intersections(ss_data_dicts, f'{path}/tables/ss', item_key='CpG', is_rewrite=is_rewrite)
aa_dicts_full, aa_dicts_diff = process_intersections(aa_data_dicts, f'{path}/tables/aa', item_key='CpG', is_rewrite=is_rewrite)
ssaa_dicts_full, ssaa_dicts_diff = process_intersections(ssaa_data_dicts, f'{path}/tables/ssaa', item_key='CpG', is_rewrite=is_rewrite)

ss_genes, aa_genes, ssaa_genes = get_human_plasma_proteome_dicts(f'{path}/proteome')

for ds in ss_dicts_diff:

    tmp_ds = ds.replace('_', '+')

    if not os.path.exists(f'{path}/proteome/ss/{tmp_ds}'):
        os.makedirs(f'{path}/proteome/ss/{tmp_ds}')
    ss_target_dict = {tmp_ds: ss_dicts_full[ds]}
    if len(ss_target_dict[tmp_ds]['CpG']) > 0:
        process_human_plasma_proteome(ss_target_dict, ss_genes, f'{path}/proteome/ss/{tmp_ds}', aux_key='UCSC_REFGENE_NAME')

    if not os.path.exists(f'{path}/proteome/aa/{tmp_ds}'):
        os.makedirs(f'{path}/proteome/aa/{tmp_ds}')
    ar_target_dict = {tmp_ds: aa_dicts_full[ds]}
    if len(ar_target_dict[tmp_ds]['CpG']) > 0:
        process_human_plasma_proteome(ar_target_dict, aa_genes, f'{path}/proteome/aa/{tmp_ds}', aux_key='UCSC_REFGENE_NAME')

    if not os.path.exists(f'{path}/proteome/ssaa/{tmp_ds}'):
        os.makedirs(f'{path}/proteome/ssaa/{tmp_ds}')
    ssar_target_dict = {tmp_ds: ssaa_dicts_full[ds]}
    if len(ssar_target_dict[tmp_ds]['CpG']) > 0:
        process_human_plasma_proteome(ssar_target_dict, ssaa_genes, f'{path}/proteome/ssaa/{tmp_ds}', aux_key='UCSC_REFGENE_NAME')

