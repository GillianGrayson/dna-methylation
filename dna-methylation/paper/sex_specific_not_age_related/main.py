import itertools
import numpy as np
import copy
from tqdm import tqdm
import os
from paper.routines.infrastructure.path import get_data_path
from paper.routines.infrastructure.load.table import load_table_dict_xlsx, load_table_dict_pkl
from paper.routines.infrastructure.load.annotations import load_annotations_dict
from paper.routines.infrastructure.load.papers import load_papers_dict
from paper.routines.infrastructure.save.table import save_table_dict_xlsx
from paper.routines.plot.venn import get_layout_3, get_layout_4, get_trace_3, get_trace_4
from paper.routines.infrastructure.save.figure import save_figure

data_type = 'betas'
datasets = ['GSE40279', 'GSE87571', 'EPIC', 'GSE55763']
hashes = ['7875dff3886829397f5fbbbf9aaae009', '8c357499960c0612f784ca7ed3fedb2c', '23298d48a2fbeb252cfdcb90cfa004a3', '67553bd9c9801d1eeeba0dc2776db156']
area_key = 'area_intersection'
max_abs_slope_key = 'max_abs_slope'
area_lim = 0.5
slope_key = 'slope'
f_key = 'f'
m_key = 'm'
hashes_groups = [
    {f_key: '6e5e9526', m_key: '40e12959', area_key: 'ebc9f2bd', max_abs_slope_key: 'ebc9f2bd'},
    {f_key: '31efe635', m_key: '3dd80109', area_key: 'c5e6999a', max_abs_slope_key: 'c5e6999a'},
    {f_key: '7383db3e', m_key: '191c0e80', area_key: 'f410e129', max_abs_slope_key: 'f410e129'},
    {f_key: '6a7442e0', m_key: '0a75a8f8', area_key: 'fa723546', max_abs_slope_key: 'fa723546'},
]

cpg_key = 'item'
area_criteria_key = 'area_intersection'
slope_criteria_key = 'slope'

annotations_keys = ['CHR', 'MAPINFO', 'UCSC_REFGENE_NAME', 'UCSC_REFGENE_GROUP', 'RELATION_TO_UCSC_CPG_ISLAND']
papers_keys = ['inoshita', 'singmann', 'yousefi']

save_path = f'{get_data_path()}/approaches/sex_specific_not_age_related/{data_type}'
if not os.path.exists(save_path):
    os.makedirs(save_path)

data_dicts_passed = {}
cpg_ids_passed = {}

for ds_id, dataset in enumerate(datasets):

    curr_load_path = f'{get_data_path()}/{dataset}/{data_type}/table/aggregator/{hashes[ds_id]}'

    data_dict = load_table_dict_pkl(f'{curr_load_path}/default.pkl')

    cpg_ids_passed[dataset] = {}

    data_dict_passed = {}
    data_dict_passed[cpg_key] = []
    data_dict_passed[area_key] = []
    data_dict_passed[max_abs_slope_key] = []
    data_dict_passed[f'{slope_key}_{f_key}'] = []
    data_dict_passed[f'{slope_key}_{m_key}'] = []

    num_cpgs = len(data_dict[cpg_key])

    cpg_rows = data_dict[cpg_key]
    area_rows = data_dict[f'{area_key}_{hashes_groups[ds_id][area_key]}']
    max_abs_slope_rows = data_dict[f'{max_abs_slope_key}_{hashes_groups[ds_id][max_abs_slope_key]}']
    slope_f_rows = data_dict[f'{slope_key}_{hashes_groups[ds_id][f_key]}']
    slope_m_rows = data_dict[f'{slope_key}_{hashes_groups[ds_id][m_key]}']

    num_passed_cpgs = 0
    for cpg_id in tqdm(range(0, num_cpgs), desc=f'{dataset} processing'):

        if area_rows[cpg_id] < area_lim:

            cpg_ids_passed[dataset][cpg_rows[cpg_id]] = num_passed_cpgs
            num_passed_cpgs += 1

            data_dict_passed[cpg_key].append(cpg_rows[cpg_id])
            data_dict_passed[area_key].append(area_rows[cpg_id])
            data_dict_passed[max_abs_slope_key].append(max_abs_slope_rows[cpg_id])
            data_dict_passed[f'{slope_key}_{f_key}'].append(slope_f_rows[cpg_id])
            data_dict_passed[f'{slope_key}_{m_key}'].append(slope_m_rows[cpg_id])

    save_table_dict_xlsx(f'{save_path}/{dataset}', data_dict_passed)

    data_dicts_passed[dataset] = data_dict_passed

datasets_ids = list(range(0, len(datasets)))
keys_ordered = copy.deepcopy(datasets)
sets = {}
checking = {}
for dataset in datasets:
    sets[dataset] = set(data_dicts_passed[dataset][cpg_key])
    checking[dataset] = 0

for L in range(2, len(datasets) + 1):
    for subset in itertools.combinations(datasets_ids, L):

        curr_ids = list(subset)

        curr_key_raw = np.sort(np.array(datasets)[np.array(curr_ids)])
        curr_key = '_'.join(list(curr_key_raw))

        if curr_key not in sets:

            cur_intersection = set(data_dicts_passed[datasets[curr_ids[0]]][cpg_key])
            for id in curr_ids[1::]:
                cur_intersection = cur_intersection.intersection(set(data_dicts_passed[datasets[id]][cpg_key]))
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
    if checking[dataset] != len(set(data_dicts_passed[dataset][cpg_key])):
        raise ValueError('Error in venn data creating')

annotations_dict = load_annotations_dict()
papers_dict = load_papers_dict()

curr_save_path = f'{save_path}/intersection'
if not os.path.exists(curr_save_path):
    os.makedirs(curr_save_path)

for set_key in sets:

    save_dict = {}

    for metrics_key in ['item'] + annotations_keys + papers_keys:
        save_dict[metrics_key] = []

    curr_datasets = set_key.split('_')
    for dataset in curr_datasets:
        for ds_key in data_dicts_passed[dataset]:
            if ds_key not in save_dict:
                save_dict[ds_key + '_' + dataset] = []

    for cpg in sets[set_key]:
        save_dict['item'].append(cpg)
        for dataset in curr_datasets:
            for ds_key in data_dicts_passed[dataset]:
                if ds_key not in save_dict:
                    save_dict[ds_key + '_' + dataset].append(data_dicts_passed[dataset][ds_key][cpg_ids_passed[dataset][cpg]])
        for ann_key in annotations_keys:
            save_dict[ann_key].append(annotations_dict[ann_key][cpg])
        for paper_key in papers_keys:
            if cpg in papers_dict[paper_key]:
                save_dict[paper_key].append(1)
            else:
                save_dict[paper_key].append(0)
    save_table_dict_xlsx(f'{curr_save_path}/{set_key}', save_dict)

curr_save_path = f'{save_path}/intersection_with_difference'
if not os.path.exists(curr_save_path):
    os.makedirs(curr_save_path)

venn_labels = []
for set_key in sets_with_difference:

    save_dict = {}

    for metrics_key in ['item'] + annotations_keys + papers_keys:
        save_dict[metrics_key] = []

    curr_datasets = set_key.split('_')
    for dataset in curr_datasets:
        for ds_key in data_dicts_passed[dataset]:
            if ds_key not in save_dict:
                save_dict[ds_key + '_' + dataset] = []

    for cpg in sets_with_difference[set_key]:
        save_dict['item'].append(cpg)
        for dataset in curr_datasets:
            for ds_key in data_dicts_passed[dataset]:
                if ds_key not in save_dict:
                    save_dict[ds_key + '_' + dataset].append(
                        data_dicts_passed[dataset][ds_key][cpg_ids_passed[dataset][cpg]])
        for ann_key in annotations_keys:
            save_dict[ann_key].append(annotations_dict[ann_key][cpg])
        for paper_key in papers_keys:
            if cpg in papers_dict[paper_key]:
                save_dict[paper_key].append(1)
            else:
                save_dict[paper_key].append(0)
    save_table_dict_xlsx(f'{curr_save_path}/{set_key}', save_dict)

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
