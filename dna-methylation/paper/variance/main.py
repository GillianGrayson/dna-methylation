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
from paper.variance.functions import get_R2s_figure
from paper.plot.venn import get_layout_3, get_layout_4, get_trace_3, get_trace_4
from paper.infrastructure.save.figure import save_figure

R2_percentile_value = 75

data_type = 'residuals'
version = 'v8'
datasets = ['GSE40279', 'GSE87571', 'EPIC', 'GSE55763']
cpg_key = 'item'
area_criteria_key = 'area_intersection'
slope_criteria_key = 'max_abs_slope'

annotations_keys = ['CHR', 'MAPINFO', 'UCSC_REFGENE_NAME', 'UCSC_REFGENE_GROUP', 'RELATION_TO_UCSC_CPG_ISLAND']
papers_keys = ['inoshita', 'singmann', 'yousefi']

path = get_data_path() + '/draft/tables/polygon/' + data_type + '/' + version

data_dicts_passed = {}
cpgs_dicts_passed = {}
R2s = {}
R2_percentiles = {}

for dataset in datasets:

    if os.path.isfile(f'{path}/{dataset}_passed.xlsx'):
        data_dict_passed = load_table_dict_xlsx(f'{path}/{dataset}_passed.xlsx')
    else:
        data_dict = load_table_dict_xlsx(f'{path}/{dataset}.xlsx')

        data_dict_passed = {}
        for key in data_dict:
            data_dict_passed[key] = []

        num_cpgs = len(data_dict[cpg_key])

        min_R2 = np.minimum(data_dict['best_R2_gender(F)'], data_dict['best_R2_gender(F)'])
        data_dict['min_R2'] = min_R2
        R2s[dataset] = min_R2

        R2_percentile = np.percentile(min_R2, R2_percentile_value)
        R2_percentiles[dataset] = R2_percentile

        for cpg_id in tqdm(range(0, num_cpgs), desc=f'{dataset} processing'):
            if data_dict['min_R2'][cpg_id] > R2_percentile \
                    and data_dict['number_of_clusters'][cpg_id] == 1 \
                    and data_dict['percent_of_noise_points'][cpg_id] < 1.0:

                for key in data_dict:
                    data_dict_passed[key].append(data_dict[key][cpg_id])

        save_table_dict_xlsx(f'{path}/{dataset}_passed', data_dict_passed)

    data_dicts_passed[dataset] = data_dict_passed
    cpgs_dicts_passed[dataset] = data_dict_passed[cpg_key]

if R2s:
    save_table_dict_xlsx(f'{path}/R2s', R2s)
    R2s_figure = get_R2s_figure(R2s, R2_percentiles)
    save_figure(f'{path}/R2s', R2s_figure)

cpgs_intersection = set(cpgs_dicts_passed[datasets[0]])
for dataset in datasets[1::]:
    cpgs_intersection = cpgs_intersection.intersection(cpgs_dicts_passed[dataset])






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
