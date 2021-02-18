import pandas as pd
from functions.routines import label_race


path = f'E:/YandexDisk/Work/pydnameth/unn_epic/all_data/raw/origin'
columns = ['main diagnosis', 'concomitant diseases', 'drugs', 'excessive level of parathyroid hormone']

df = pd.read_excel(f"{path}/disease.xlsx", engine='openpyxl')

for col in columns:

    cds_raw = df[col].values
    cds = set()
    for row in cds_raw:
        if isinstance(row, str):
            row_cds = row.split(',')
            for cd in row_cds:
                cds.update([cd.lower()])
    tmp = {'yes', 'no', ''}
    cds.difference_update(tmp)

    cds = sorted(list(cds))

    for cd in cds:
        df[cd] = df.apply(lambda row: label_race(row, cd, col), axis=1)

df.to_excel(f"{path}/disease_upd.xlsx", index=False)




ololo = 1