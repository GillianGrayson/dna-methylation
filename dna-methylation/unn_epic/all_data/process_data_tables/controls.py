import pandas as pd
from functions.routines import label_race


path = f'E:/YandexDisk/Work/pydnameth/unn_epic/all_data/raw'

df = pd.read_excel(f"{path}/controls.xlsx", engine='openpyxl')

cds_raw = df['chronic diseases'].values
cds = set()
for row in cds_raw:
    row_cds = row.split(', ')
    for cd in row_cds:
        cds.update([cd.lower()])
tmp = {'yes', 'no'}
cds.difference_update(tmp)

for cd in cds:
    df[cd] = df.apply(lambda row: label_race(row, cd, 'chronic diseases'), axis=1)

df.to_excel(f"{path}/controls_upd.xlsx", index=False)


ololo = 1
