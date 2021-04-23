from functools import reduce

import pandas as pd

path = f'E:/YandexDisk/Work/pydnameth/draft/2/supplementary/part(v2)/4'
df = pd.read_excel(f'{path}/SupplementaryTable7.xlsx', converters={'ID': str}, engine='openpyxl', sheet_name='Age Acceleration (Disease)')

#metrics = ['Age p-value', 'DNAmAgeHannum p-value','DNAmAge p-value', 'DNAmPhenoAge p-value', 'DNAmGrimAge p-value', 'Phenotypical Age p-value', 'ImmunoAge p-value']
metrics = ['DNAmAgeHannum Acceleration p-value','DNAmAge Acceleration p-value', 'IEAA p-value',  'DNAmPhenoAge Acceleration p-value', 'DNAmGrimAge Acceleration p-value', 'Phenotypical Age Acceleration p-value', 'ImmunoAge Acceleration p-value']

table = {'below 0.05': ['Disease']}
limit = 0.05

lists = {}
for m in metrics:
    tmp = df.loc[(df[m] < 0.05), :].copy(deep=True)
    lists[m] = tmp['feature'].to_list()
    num_remains = tmp.shape[0]
    table[m] = [num_remains]

intersect = list(reduce(set.intersection, [set(item) for key,item in lists.items()]))

res = pd.DataFrame(table)

res.to_excel(f'{path}/current_table.xlsx', index=False)

