import pandas as pd

path = f'E:/YandexDisk/Work/pydnameth/draft/2/supplementary/part(v2)'
df = pd.read_excel(f'{path}/SupplementaryTable3.xlsx', converters={'ID': str}, engine='openpyxl', sheet_name='Age Acceleration (Disease)')

metrics = ['DNAmAgeHannum Acceleration p-value','DNAmAge Acceleration p-value', 'DNAmPhenoAge Acceleration p-value', 'DNAmGrimAge Acceleration p-value', 'Phenotypical Age Acceleration p-value', 'ImmunoAge Acceleration p-value', 'IEAA p-value']

table = {'below 0.05': ['Disease']}
limit = 0.05

for m in metrics:
    tmp = df.loc[(df[m] < 0.05), :].copy(deep=True)
    num_remains = tmp.shape[0]
    table[m] = [num_remains]

res = pd.DataFrame(table)

res.to_excel(f'{path}/current_table.xlsx', index=False)

