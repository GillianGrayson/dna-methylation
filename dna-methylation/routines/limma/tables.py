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

path = 'E:/YandexDisk/Work/pydnameth/methylation_and_proteomic/limma'
data_type = 'beta'
target_metric = 'Sex_adj.P.Val'
limits = [0.05, 0.01, 0.005, 0.001]
datasets = ['GSE87571', 'GSE74193', 'liver']
table = {'Dataset':['GSE87571', 'GSE74193', 'liver']}

for lim in limits:
    key = f'<{lim}'
    table[key] = []
    for dataset in datasets:
        target_fn = f'{path}/{dataset}/{dataset}_{data_type}_filtered.pkl'
        data = load_table_dict_pkl(target_fn)
        column = np.asarray(data[target_metric])
        remains = column[np.where(column < lim)]
        num_remains = remains.shape
        table[key].append(len(remains))

df = pd.DataFrame(table)
df.to_csv(f'{path}/counts/{target_metric}.csv', index=False)
