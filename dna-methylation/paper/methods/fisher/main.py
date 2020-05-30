from paper.routines.infrastructure.load.table import load_table_dict_xlsx
from paper.routines.infrastructure.save.table import save_table_dict_xlsx
from paper.routines.infrastructure.load.annotations import load_annotations_dict
from paper.methods.fisher.routines import perform_fisher
from collections import defaultdict
import numpy as np
import os


save_path = 'E:/YandexDisk/Work/pydnameth/approaches/approach_3/residuals/fisher'

global_fn = 'E:/YandexDisk/Work/pydnameth/approaches/approach_3/residuals/metal/ar_qval.xlsx'
global_dict = load_table_dict_xlsx(global_fn)
global_probe_key = 'MarkerName'

target_fn = 'E:/YandexDisk/Work/pydnameth/approaches/approach_3/residuals/metal/ssar/intersection_with_difference/ar_ss.xlsx'
target_dict = load_table_dict_xlsx(target_fn)
target_probe_key = 'MarkerName'

annotations_dict = load_annotations_dict()

target_variables = ['RELATION_TO_UCSC_CPG_ISLAND', 'CHR', 'UCSC_REFGENE_GROUP']

for var in target_variables:

    count_global = {}
    for probe in global_dict[global_probe_key]:
        opts = annotations_dict[var][probe].split(';')
        for opt in opts:
            if opt in count_global:
                count_global[opt] += 1
            else:
                count_global[opt] = 1
    global_num = np.sum(list(count_global.values()))

    count_target = {}
    for probe in target_dict[target_probe_key]:
        opts = annotations_dict[var][probe].split(';')
        for opt in opts:
            if opt in count_target:
                count_target[opt] += 1
            else:
                count_target[opt] = 1
    target_num = np.sum(list(count_target.values()))

    odds_ratios = {}
    p_values = {}
    res_table_dict = defaultdict(list)
    for opt in count_target:
        odds_ratio, p_value = perform_fisher(count_target[opt], count_global[opt], target_num, global_num)
        odds_ratios[opt] = odds_ratio
        p_values[opt] = p_value

        res_table_dict[var].append(opt)
        res_table_dict['number of probes'].append(count_target[opt])
        res_table_dict['total number of probes'].append(count_global[opt])
        res_table_dict['p-value'].append(p_values[opt])
        res_table_dict['odds ratio'].append(odds_ratios[opt])

    if not os.path.exists(save_path):
        os.makedirs(save_path)
    save_table_dict_xlsx(f'{save_path}/{var}', res_table_dict)

aa = 1

