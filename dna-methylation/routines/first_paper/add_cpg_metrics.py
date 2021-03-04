import pandas as pd
import numpy as np
import os.path
import pickle
from tqdm import tqdm

cpg_fn = 'D:/YandexDisk/Work/pydnameth/vedunova/union.xlsx'

metrics_fn = 'D:/YandexDisk/Work/pydnameth/GSE87571/betas/table/aggregator/8c357499960c0612f784ca7ed3fedb2c/default.pkl'

df = pd.read_excel(cpg_fn)
data_dict = {}
data_dict['item'] = list(df.item)

metrics = ['aux', 'mean_gender(F)', 'slope_gender(F)', 'mean_gender(M)', 'slope_gender(M)']
for metric in metrics:
    data_dict[metric] = []

f = open(metrics_fn, 'rb')
metrics_dict = pickle.load(f)
f.close()

for item in tqdm(data_dict['item']):
    index = metrics_dict['item'].index(item)
    for metric in metrics:
        data_dict[metric].append(metrics_dict[metric][index])

data = pd.DataFrame(data_dict)
writer = pd.ExcelWriter('D:/YandexDisk/Work/pydnameth/vedunova/union_with_metrics.xlsx', engine='xlsxwriter')
data.to_excel(writer, index=False)
writer.save()

