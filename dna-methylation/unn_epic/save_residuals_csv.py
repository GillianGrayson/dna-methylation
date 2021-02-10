import pydnameth as pdm
from scripts.develop.routines import *
from tqdm import tqdm
import numpy as np
from scipy.stats import pearsonr, pointbiserialr
from statsmodels.stats.multitest import multipletests
from paper.routines.infrastructure.save.table import save_table_dict_xlsx
import pandas as pd

save_path = 'E:/YandexDisk/Work/pydnameth/unn_epic'

data = pdm.Data(
    path='',
    base='unn_epic'
)
annotations = pdm.Annotations(
    name='annotations',
    type='850k',
    exclude='bad_cpgs_from_ChAMP',
    select_dict={
        'CHR': ['-X', '-Y']
    }
)
target = 'Age'
observables_unn_epic = pdm.Observables(
    name='observables_part(final)',
    types={}
)
cells = pdm.Cells(
    name='cell_counts',
    types='any'
)
attributes = pdm.Attributes(
    target=target,
    observables=observables_unn_epic,
    cells=cells
)
data_params_unn_epic = {
    'norm': 'BMIQ',
    'part': 'final',
    'cells': ['Bcell', 'CD4T', 'CD8T', 'Neu', 'NK']
}

config = pdm.load_residuals_config(
    data,
    annotations,
    attributes,
    data_params=data_params_unn_epic
)

keys = ['X' + elem for elem in config.observables_dict['Sample_Name']]
res_dict = {}
for x_id, x in enumerate(keys):
    res_dict[x] = config.base_data[:, x_id]
res_dict['IlmnID'] = [0] * len(config.base_dict)
for cpg, row in config.base_dict.items():
    res_dict['IlmnID'][row] = cpg

df = pd.DataFrame(res_dict)
df.to_csv(f'{save_path}/residuals_tmp.csv')
