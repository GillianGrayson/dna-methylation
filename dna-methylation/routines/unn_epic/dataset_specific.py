import pydnameth as pdm
from scripts.develop.routines import *
from tqdm import tqdm
import numpy as np
from scipy.stats import pearsonr, pointbiserialr
from statsmodels.stats.multitest import multipletests
from paper.routines.infrastructure.save.table import save_table_dict_xlsx

save_path = 'E:/YandexDisk/Work/pydnameth/unn_epic/comparison'

data_unn_epic = pdm.Data(
    path='',
    base='unn_epic'
)
annotations_unn_epic = pdm.Annotations(
    name='annotations',
    type='850k',
    exclude='bad_cpgs_from_ChAMP',
    select_dict={
        'CHR': ['-X', '-Y']
    }
)
target_unn_epic = 'Age'
observables_unn_epic = pdm.Observables(
    name='observables',
    types={}
)
cells_unn_epic = pdm.Cells(
    name='cell_counts_horvath_filtered_normalized',
    types='any'
)
attributes_unn_epic = pdm.Attributes(
    target=target_unn_epic,
    observables=observables_unn_epic,
    cells=cells_unn_epic
)
data_params_unn_epic = get_data_params(data_unn_epic.base)
config_unn = pdm.load_beta_config(
    data_unn_epic,
    annotations_unn_epic,
    attributes_unn_epic,
    data_params=data_params_unn_epic
)




data_other = pdm.Data(
    path='',
    base='GSE87571'
)
annotations_other = pdm.Annotations(
    name='annotations',
    type='450k',
    exclude='bad_cpgs',
    select_dict={
        'CHR': ['-X', '-Y']
    }
)
target_other = get_target(data_other.base)
observables_other = pdm.Observables(
    name='observables',
    types={}
)
cells_other = pdm.Cells(
    name='cells_horvath_calculator',
    types='any'
)
attributes_other = pdm.Attributes(
    target=target_other,
    observables=observables_other,
    cells=cells_other
)
data_params_other = get_data_params(data_other.base)
config_other = pdm.load_beta_config(
    data_other,
    annotations_other,
    attributes_other,
    data_params_other
)

cpgs_unn = list(set(config_unn.cpg_list).intersection(config_unn.base_dict.keys()))
cpgs_other = list(set(config_other.cpg_list).intersection(config_other.base_dict.keys()))
common_cpgs = list(set(cpgs_unn).intersection(set(cpgs_other)))

metrics = [
    'item',
    'aux_unn',
    'aux_other',
    'corr_coeff',
    'p_value',
    'p_value_benjamini_hochberg',
    'p_value_bonferroni'
]
result = {}
for key in metrics:
    result[key] = []

for cpg_id, cpg in tqdm(enumerate(common_cpgs), mininterval=60.0, desc='cpgs_processing'):
    betas_unn = config_unn.base_data[config_unn.base_dict[cpg], config_unn.attributes_indexes]
    label_unn = [1] * len(betas_unn)
    betas_other = config_other.base_data[config_other.base_dict[cpg], config_other.attributes_indexes]
    label_other = [0] * len(betas_other)
    betas_all = np.concatenate((betas_unn, betas_other), axis=0)
    label_all = np.asarray(label_unn + label_other)

    if len(set(label_all)) != 2:
        raise RuntimeError('x variable is not binary in pbc')

    corr_coeff, p_value = pointbiserialr(label_all, betas_all)

    result['corr_coeff'].append(corr_coeff)
    result['p_value'].append(p_value)

    result['item'].append(cpg)
    aux = ''
    if cpg in config_unn.cpg_gene_dict:
        aux = ';'.join(config_unn.cpg_gene_dict[cpg])
    result['aux_unn'].append(aux)
    aux = ''
    if cpg in config_other.cpg_gene_dict:
        aux = ';'.join(config_other.cpg_gene_dict[cpg])
    result['aux_other'].append(aux)

pvals = np.asarray(result['p_value'])
reject, pvals_corr, alphacSidak, alphacBonf = multipletests(
    pvals,
    0.05,
    method='fdr_bh'
)
result['p_value_benjamini_hochberg'] = pvals_corr

reject, pvals_corr, alphacSidak, alphacBonf = multipletests(
    pvals,
    0.05,
    method='bonferroni'
)
result['p_value_bonferroni'] = pvals_corr

save_table_dict_xlsx(f'{save_path}/pbc_vs_GSE87571', result)
