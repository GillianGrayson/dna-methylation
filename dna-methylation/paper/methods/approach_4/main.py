from paper.routines.data.data_dicts import *
from paper.routines.data.approaches import *
from paper.methods.approach_4.filter import filter_data_dicts
from paper.routines.data.human_plasma_proteome import *

pval_perc = 10
pval_null_lim = 0.05

type = 'residuals'
names = ['GSE40279', 'GSE87571', 'EPIC', 'GSE55763']
datasets = [Dataset(type, name) for name in names]

keys_save = [
    'item',
    'aux',
    'type_f',
    'bp_f_pvalue_fdr_bh_f',
    'type_m',
    'bp_f_pvalue_fdr_bh_m',
]

keys_load = {}
for dataset in datasets:
    keys_load[dataset.name] = [
        'item',
        'aux',
        f'type_{get_hs_f_hash(dataset)}',
        f'bp_f_pvalue_fdr_bh_{get_hs_f_hash(dataset)}',
        f'type_{get_hs_m_hash(dataset)}',
        f'bp_f_pvalue_fdr_bh_{get_hs_m_hash(dataset)}',
    ]

save_path = f'{get_data_path()}/approaches/approach_4/{type}'
if not os.path.exists(save_path):
    os.makedirs(save_path)
if not os.path.exists(f'{save_path}/f'):
    os.makedirs(f'{save_path}/f')
if not os.path.exists(f'{save_path}/m'):
    os.makedirs(f'{save_path}/m')
if not os.path.exists(f'{save_path}/fm'):
    os.makedirs(f'{save_path}/fm')

data_dicts = get_data_dicts(datasets, 'aggregator', keys_load, keys_save, get_approach_4_hash)
ss_data_dicts, ar_data_dicts, ssar_data_dicts = filter_data_dicts(data_dicts, pval_perc, pval_null_lim, save_path)

f_result_dicts, f_result_dicts_with_diff = process_intersections(ss_data_dicts, f'{save_path}/f')
m_result_dicts, m_result_dicts_with_diff = process_intersections(ar_data_dicts, f'{save_path}/m')
fm_result_dicts, fm_result_dicts_with_diff = process_intersections(ssar_data_dicts, f'{save_path}/fm')
