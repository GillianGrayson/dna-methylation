from paper.routines.data.data_dicts import *
from paper.routines.data.approaches import *
from paper.methods.approach_3.filter import filter_data_dicts, add_best_pvalue
from paper.methods.approach_3.metal import *

proteomic = False
metal = True

pval_perc_ss = 10
pval_perc_ar = 10
pval_lim = 0.05
pval_prefix = 'p_value_fdr_bh'

pval_perc_ss_metal = 5
pval_perc_ar_metal = 5

type = 'residuals'
names = ['GSE40279', 'GSE87571', 'EPIC', 'GSE55763']
datasets = [Dataset(type, name) for name in names]

keys_save = [
    'item',
    'aux',
    'corr_coeff_ss',
    'p_value_ss',
    'p_value_fdr_bh_ss',
    'p_value_fdr_hb_ss',
    'lin_lin_corr_coeff_ar',
    'lin_lin_p_value_ar',
    'lin_lin_p_value_fdr_bh_ar',
    'lin_lin_p_value_fdr_b_ar',
    'lin_log_corr_coeff_ar',
    'lin_log_p_value_ar',
    'lin_log_p_value_fdr_bh_ar',
    'lin_log_p_value_fdr_b_ar',
    'log_lin_corr_coeff_ar',
    'log_lin_p_value_ar',
    'log_lin_p_value_fdr_bh_ar',
    'log_lin_p_value_fdr_b_ar',
    'log_log_corr_coeff_ar',
    'log_log_p_value_ar',
    'log_log_p_value_fdr_bh_ar',
    'log_log_p_value_fdr_b_ar',
]

keys_load = {}
for dataset in datasets:
    keys_load[dataset.name] = [
        'item',
        'aux',
        f'corr_coeff_{get_ss_hash(dataset)}',
        f'p_value_{get_ss_hash(dataset)}',
        f'p_value_fdr_bh_{get_ss_hash(dataset)}',
        f'p_value_bonferroni_{get_ss_hash(dataset)}',
        f'lin_lin_corr_coeff_{get_ar_hash(dataset)}',
        f'lin_lin_p_value_{get_ar_hash(dataset)}',
        f'lin_lin_p_value_fdr_bh_{get_ar_hash(dataset)}',
        f'lin_lin_p_value_bonferroni_{get_ar_hash(dataset)}',
        f'lin_log_corr_coeff_{get_ar_hash(dataset)}',
        f'lin_log_p_value_{get_ar_hash(dataset)}',
        f'lin_log_p_value_fdr_bh_{get_ar_hash(dataset)}',
        f'lin_log_p_value_bonferroni_{get_ar_hash(dataset)}',
        f'log_lin_corr_coeff_{get_ar_hash(dataset)}',
        f'log_lin_p_value_{get_ar_hash(dataset)}',
        f'log_lin_p_value_fdr_bh_{get_ar_hash(dataset)}',
        f'log_lin_p_value_bonferroni_{get_ar_hash(dataset)}',
        f'log_log_corr_coeff_{get_ar_hash(dataset)}',
        f'log_log_p_value_{get_ar_hash(dataset)}',
        f'log_log_p_value_fdr_bh_{get_ar_hash(dataset)}',
        f'log_log_p_value_bonferroni_{get_ar_hash(dataset)}',
    ]

save_path = f'{get_data_path()}/approaches/approach_3/{type}'
if not os.path.exists(save_path):
    os.makedirs(save_path)
if not os.path.exists(f'{save_path}/ss'):
    os.makedirs(f'{save_path}/ss')
if not os.path.exists(f'{save_path}/ar'):
    os.makedirs(f'{save_path}/ar')
if not os.path.exists(f'{save_path}/ssar'):
    os.makedirs(f'{save_path}/ssar')

data_dicts = get_data_dicts(datasets, 'aggregator', keys_load, keys_save, get_approach_3_hash)
add_best_pvalue(data_dicts, f'{pval_prefix}_ar')
ss_data_dicts, ar_data_dicts, ssar_data_dicts = filter_data_dicts(data_dicts, pval_prefix, pval_perc_ss, pval_perc_ar, pval_lim, save_path)

ss_result_dicts, ss_result_dicts_with_diff = process_intersections(ss_data_dicts, f'{save_path}/ss')
ar_result_dicts, ar_result_dicts_with_diff = process_intersections(ar_data_dicts, f'{save_path}/ar')
ssar_result_dicts, ssar_result_dicts_with_diff = process_intersections(ssar_data_dicts, f'{save_path}/ssar')

if metal == True:
    path = f'{save_path}/metal'

    data_dicts = {}
    metal_type = 'ss_qval'
    data_dicts['ss'] = metal_process(metal_type, pval_perc_ss_metal, path)
    metal_type = 'ar_qval'
    data_dicts['ar'] = metal_process(metal_type, pval_perc_ar_metal, path)

    if not os.path.exists(f'{path}/ssar'):
        os.makedirs(f'{path}/ssar')
    result_dicts, result_dicts_with_diff = process_intersections(data_dicts, f'{path}/ssar', 'MarkerName')

    mix_dicts = {}
    mix_dicts['METAL'] = {'item': result_dicts_with_diff['ar_ss']['MarkerName']}
    mix_dicts['Basic'] = {'item': ssar_result_dicts_with_diff['EPIC_GSE40279_GSE55763_GSE87571']['item']}

    if not os.path.exists(f'{path}/ssar_metal'):
        os.makedirs(f'{path}/ssar_metal')
    result_dicts, result_dicts_with_diff = process_intersections(mix_dicts, f'{path}/ssar_metal')

if proteomic == True:

    if not os.path.exists(f'{save_path}/proteome'):
        os.makedirs(f'{save_path}/proteome')
    ss_genes_lehallier, ar_genes_lehallier, ssar_genes_lehallier = get_human_plasma_proteome_dicts(f'{save_path}/proteome')

    for ds in ss_result_dicts_with_diff:

        tmp_ds = ds.replace('_', '+')

        if not os.path.exists(f'{save_path}/proteome/ss/{tmp_ds}'):
            os.makedirs(f'{save_path}/proteome/ss/{tmp_ds}')
        ss_target_dict = {tmp_ds: ss_result_dicts_with_diff[ds]}
        process_human_plasma_proteome(ss_target_dict, ss_genes_lehallier, f'{save_path}/proteome/ss/{tmp_ds}')

        if not os.path.exists(f'{save_path}/proteome/ar/{tmp_ds}'):
            os.makedirs(f'{save_path}/proteome/ar/{tmp_ds}')
        ar_target_dict = {tmp_ds: ar_result_dicts_with_diff[ds]}
        process_human_plasma_proteome(ar_target_dict, ar_genes_lehallier, f'{save_path}/proteome/ar/{tmp_ds}')

        if not os.path.exists(f'{save_path}/proteome/ssar/{tmp_ds}'):
            os.makedirs(f'{save_path}/proteome/ssar/{tmp_ds}')
        ssar_target_dict = {tmp_ds: ssar_result_dicts_with_diff[ds]}
        process_human_plasma_proteome(ssar_target_dict, ssar_genes_lehallier, f'{save_path}/proteome/ssar/{tmp_ds}')
