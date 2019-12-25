import itertools
import numpy as np
import copy
from tqdm import tqdm
import os
from paper.infrastructure.path import get_data_path
from paper.infrastructure.load.table import load_table_dict_xlsx
from paper.infrastructure.load.annotations import load_annotations_dict
from paper.infrastructure.load.papers import load_papers_dict
from paper.infrastructure.save.table import save_table_dict_xlsx
from paper.plot.venn import get_layout_3, get_layout_4, get_trace_3, get_trace_4
from paper.infrastructure.save.figure import save_figure

pval_percentile_lim = 90
pval_null_accepted = 0.5

data_type = 'betas'
datasets = ['GSE87571']
hashes = ['c098dc79338657b0b9c35f55a8441e80']
f_key = 'f'
m_key = 'f'
hashes_groups = [{f_key: '25dcc690', m_key: '00f7ba4d'}]
cpg_key = 'item'
pval_key = 'bp_lm_pvalue_fdr_bh'
type_key = 'type'

annotations_keys = ['CHR', 'MAPINFO', 'UCSC_REFGENE_NAME', 'UCSC_REFGENE_GROUP', 'RELATION_TO_UCSC_CPG_ISLAND']
papers_keys = ['inoshita', 'singmann', 'yousefi']

save_path = f'{get_data_path()}/approaches/approach_4'

f_var_dicts_passed = {}
m_var_dicts_passed = {}
f_m_var_dicts_passed = {}

pvals = {}
pvals_percentiles = {}

for ds_id, dataset in enumerate(datasets):
    curr_load_path = f'{get_data_path()}/{dataset}/{data_type}/table/aggregator/{hashes[ds_id]}'
    curr_save_path = f'{save_path}'

    if os.path.isfile(f'{curr_save_path}/{dataset}_f_var.xlsx') \
            and os.path.isfile(f'{curr_save_path}/{dataset}_m_var.xlsx') \
            and os.path.isfile(f'{curr_save_path}/{dataset}_f_m_var.xlsx'):

        f_var_passed = load_table_dict_xlsx(f'{curr_save_path}/{dataset}_f_var.xlsx')
        m_var_passed = load_table_dict_xlsx(f'{curr_save_path}/{dataset}_m_var.xlsx')
        f_m_var_passed = load_table_dict_xlsx(f'{curr_save_path}/{dataset}_f_m_var.xlsx')
    else:
        data_dict = load_table_dict_xlsx(f'{curr_load_path}/default.xlsx')

        f_var_passed = {}
        m_var_passed = {}
        f_m_var_passed = {}
        for key in data_dict:
            f_var_passed[key] = []
            m_var_passed[key] = []
            f_m_var_passed[key] = []

        num_cpgs = len(data_dict[cpg_key])

        pval_f = data_dict[-np.log10(f'{pval_key}_{hashes_groups[ds_id][f_key]}')]
        pval_m = data_dict[-np.log10(f'{pval_key}_{hashes_groups[ds_id][m_key]}')]
        pval_f_percentile = np.percentile(pval_f, pval_percentile_lim)
        pval_m_percentile = np.percentile(pval_m, pval_percentile_lim)

        pvals[dataset] = {f_key: pval_f, m_key: pval_m}
        pvals_percentiles[dataset] = {f_key: pval_f_percentile, m_key: pval_m_percentile}

        print(f'{dataset} persentile {f_key}: {np.power(10.0, -pval_f_percentile)}')
        print(f'{dataset} persentile {m_key}: {np.power(10.0, -pval_m_percentile)}')

        for cpg_id in tqdm(range(0, num_cpgs), desc=f'{dataset} processing'):

            if (data_dict[f'{pval_key}_{hashes_groups[ds_id][f_key]}'] < np.power(10.0, -pval_f_percentile)) \
                    and (data_dict[f'{pval_key}_{hashes_groups[ds_id][m_key]}'] > pval_null_accepted):
                for key in data_dict:
                    f_var_passed[key].append(data_dict[key][cpg_id])

            if (data_dict[f'{pval_key}_{hashes_groups[ds_id][m_key]}'] < np.power(10.0, -pval_f_percentile)) \
                    and (data_dict[f'{pval_key}_{hashes_groups[ds_id][f_key]}'] > pval_null_accepted):
                for key in data_dict:
                    m_var_passed[key].append(data_dict[key][cpg_id])

            if (data_dict[f'{pval_key}_{hashes_groups[ds_id][f_key]}'] < np.power(10.0, -pval_f_percentile)) \
                    and (data_dict[f'{pval_key}_{hashes_groups[ds_id][m_key]}'] < np.power(10.0, -pval_f_percentile)) \
                    and (data_dict[f'{type_key}_{hashes_groups[ds_id][f_key]}'] != data_dict[f'{type_key}_{hashes_groups[ds_id][m_key]}']):
                for key in data_dict:
                    f_m_var_passed[key].append(data_dict[key][cpg_id])

        save_table_dict_xlsx(f'{curr_save_path}/{dataset}_f_var', f_var_passed)
        save_table_dict_xlsx(f'{curr_save_path}/{dataset}_m_var', f_var_passed)
        save_table_dict_xlsx(f'{curr_save_path}/{dataset}_f_m_var', f_m_var_passed)

    f_var_dicts_passed[dataset] = f_var_passed
    m_var_dicts_passed[dataset] = m_var_passed
    f_m_var_dicts_passed[dataset] = f_m_var_passed

datasets_ids = list(range(0, len(datasets)))
keys_ordered = copy.deepcopy(datasets)
sets = {}
checking = {}
for dataset in datasets:
    sets[dataset] = set(cpgs_dicts_passed[dataset])
    checking[dataset] = 0

for L in range(2, len(datasets) + 1):
    for subset in itertools.combinations(datasets_ids, L):

        curr_ids = list(subset)

        curr_key_raw = np.sort(np.array(datasets)[np.array(curr_ids)])
        curr_key = '_'.join(list(curr_key_raw))

        if curr_key not in sets:

            cur_intersection = set(cpgs_dicts_passed[datasets[curr_ids[0]]])
            for id in curr_ids[1::]:
                cur_intersection = cur_intersection.intersection(set(cpgs_dicts_passed[datasets[id]]))
            sets[curr_key] = cur_intersection

            keys_ordered.append(curr_key)

keys_ordered = keys_ordered[::-1]

sets_with_difference = copy.deepcopy(sets)
for key in keys_ordered:
    curr_labels = set(key.split('_'))
    for key_var in keys_ordered:
        curr_labels_var = set(key_var.split('_'))
        if key_var != key:
            if curr_labels.issubset(curr_labels_var):
                sets_with_difference[key] -= sets_with_difference[key_var]

for set_key in sets_with_difference:
    curr_labels = set_key.split('_')
    for label in curr_labels:
        checking[label] += len(sets_with_difference[set_key])

for dataset in datasets:
    if checking[dataset] != len(set(cpgs_dicts_passed[dataset])):
        raise ValueError('Error in venn data creating')

annotations_dict = load_annotations_dict()
papers_dict = load_papers_dict()

save_path = f'{path}/intersection'
if not os.path.exists(save_path):
    os.makedirs(save_path)

for set_key in sets:
    save_dict = {}
    for metrics_key in ['cpg'] + annotations_keys + papers_keys:
        save_dict[metrics_key] = []
    for cpg in sets[set_key]:
        save_dict['cpg'].append(cpg)
        for ann_key in annotations_keys:
            save_dict[ann_key].append(annotations_dict[ann_key][cpg])
        for paper_key in papers_keys:
            if cpg in papers_dict[paper_key]:
                save_dict[paper_key].append(1)
            else:
                save_dict[paper_key].append(0)
    save_table_dict_xlsx(f'{save_path}/{set_key}', save_dict)

save_path = f'{path}/intersection_with_difference'
if not os.path.exists(save_path):
    os.makedirs(save_path)

venn_labels = []
for set_key in sets_with_difference:

    save_dict = {}
    for metrics_key in ['cpg'] + annotations_keys + papers_keys:
        save_dict[metrics_key] = []
    for cpg in sets_with_difference[set_key]:
        save_dict['cpg'].append(cpg)
        for ann_key in annotations_keys:
            save_dict[ann_key].append(annotations_dict[ann_key][cpg])
        for paper_key in papers_keys:
            if cpg in papers_dict[paper_key]:
                save_dict[paper_key].append(1)
            else:
                save_dict[paper_key].append(0)
    save_table_dict_xlsx(f'{save_path}/{set_key}', save_dict)

    curr_labels = set_key.split('_') + [str(len(sets_with_difference[set_key]))]
    venn_labels.append('<br>'.join(curr_labels))


if len(datasets) == 4:
    layout = get_layout_4()
    trace = get_trace_4(venn_labels)
elif len(datasets) == 3:
    layout = get_layout_3()
    trace = get_trace_3(venn_labels)
else:
    raise ValueError(f'Venn diagram is not supported')

fig = {
    'data': [trace],
    'layout': layout,
}

save_figure(f'{save_path}/{keys_ordered[0]}', fig)
