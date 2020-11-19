from routines.limma.annotations.load import load_annotations_dict
from routines.limma.annotations.subset import subset_annotations
from routines.limma.annotations.annotations import Annotations
from routines.limma.annotations.excluded import load_excluded
from routines.limma.annotations.add_info import add_info_to_dict
from paper.routines.infrastructure.load.table import load_table_dict_xlsx, load_table_dict_pkl
from paper.routines.infrastructure.save.table import save_table_dict_xlsx, save_table_dict_pkl
import os.path
from tqdm import tqdm
from paper.routines.plot.pdf import get_pdf_x_and_y
from paper.routines.plot.layout import get_layout
import plotly.graph_objs as go
import colorlover as cl
import numpy as np
import plotly
import pandas as pd
from functions.save.list import save_list


path = 'E:/YandexDisk/Work/pydnameth/unn_epic/bop/table/manova/80025992391d7842c38012ef54dee3ec'
fn = 'default'
target_metrics = ['p_value_fdr_bh_roy_80025992', 'p_value_bonferroni_roy_80025992']
limit = 0.05

table = {}
table['Number of'] = ['BoPs', 'Genes']

curr_fn = f'{path}/{fn}.pkl'
data = load_table_dict_pkl(curr_fn)

cpgs = data['item']
genes = data['genes_80025992']

for metric in target_metrics:
    column = np.asarray(data[metric])
    indexes = np.where(column < limit)
    cpgs_targ = [cpgs[i] for i in indexes[0]]
    genes_targ_raw = [genes[i] for i in indexes[0]]
    genes_targ = []
    for g in genes_targ_raw:
        if g != '':
            g_list = g.split(';')
            genes_targ += list(set(g_list))

    genes_targ = set(genes_targ)

    table[metric] = [len(cpgs_targ), len(genes_targ)]

    suffix = f'{path}/{metric}_{limit:.2E}'
    save_list(cpgs_targ, f'{suffix}_cpgs')
    save_list(genes_targ, f'{suffix}_genes')

df = pd.DataFrame(table)
df.to_csv(f'{path}/table_{limit:.2E}.csv', index=False)
