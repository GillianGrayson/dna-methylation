import pandas as pd
from functions.routines import label_race


path = f'E:/YandexDisk/Work/pydnameth/unn_epic/all_data/raw/origin'
columns = ['drugs']

df = pd.read_excel(f"{path}/diagnosis_drug.xlsx", engine='openpyxl')

for col in columns:

    cds_raw = df[col].values
    cds = set()
    for row_id, row in enumerate(cds_raw):
        if isinstance(row, str):
            row_cds = sorted(list(set(row.split(', '))))
            df.iloc[row_id, df.columns.get_loc(col)] = ', '.join(row_cds)
            for cd in row_cds:
                cds.update([cd])
    tmp = {'yes', 'no', ''}
    cds.difference_update(tmp)

    cds = sorted(list(cds))

    for cd in cds:
        df[cd] = df.apply(lambda row: label_race(row, cd, col), axis=1)

df.to_excel(f"{path}/disease_upd.xlsx", index=False)




ololo = 1