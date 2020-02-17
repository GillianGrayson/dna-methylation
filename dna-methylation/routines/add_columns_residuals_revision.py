import pandas as pd

path_info = 'D:/YandexDisk/pydnameth/draft/revision/v11/'
path = 'D:/YandexDisk/pydnameth/draft/revision/v13/'

datasets = ['GSE40279', 'GSE87571', 'EPIC', 'GSE55763']

df_info = {'GSE40279': {},
           'GSE87571': {},
           'EPIC': {},
           'GSE55793': {}}
for dataset in datasets:
    file_info = path_info + 'increasing_type_residuals_' + dataset + '.xlsx'
    df_info[dataset] = pd.read_excel(file_info, header=0).to_dict('list')

file_base = path + 'sex_specific_variance_residuals_' + '_'.join(datasets) + '_raw.xlsx'
df_base = pd.read_excel(file_base, header=0)
cpg_list = df_base['ID_REF'].to_list()

increasing_type = {'GSE40279': {'F': [], 'M': []},
                   'GSE87571': {'F': [], 'M': []},
                   'EPIC': {'F': [], 'M': []},
                   'GSE55763': {'F': [], 'M': []}}

for item in cpg_list:
    for dataset in datasets:
        index = df_info[dataset]['item'].index(item)
        increasing_type[dataset]['F'].append(df_info[dataset]['increasing_type_F'][index])
        increasing_type[dataset]['M'].append(df_info[dataset]['increasing_type_M'][index])

base_column_id = 11
for dataset in datasets:
    df_base.insert(base_column_id, 'VARIANCE CHANGING TYPE IN F IN ' + dataset, increasing_type[dataset]['F'])
    base_column_id += 1
    df_base.insert(base_column_id, 'VARIANCE CHANGING TYPE IN M IN ' + dataset, increasing_type[dataset]['M'])
    base_column_id += 1

df_base.rename(columns={'mean_inc_fit_4': 'MEAN I'}, inplace=True)
df_base.rename(columns={'increasing_fit_GSE40279': 'I IN GSE40279'}, inplace=True)
df_base.rename(columns={'increasing_fit_GSE87571': 'I IN GSE87571'}, inplace=True)
df_base.rename(columns={'increasing_fit_EPIC': 'I IN EPIC'}, inplace=True)
df_base.rename(columns={'increasing_fit_GSE55763': 'I IN GSE55763'}, inplace=True)

df_base.rename(columns={'inoshita': 'IS FOUND IN INOSHITA, 2015'}, inplace=True)
df_base.rename(columns={'singmann': 'IS FOUND IN SINGMANN, 2015'}, inplace=True)
df_base.rename(columns={'yousefi': 'IS FOUND IN YOUSEFI, 2015'}, inplace=True)

file_betas = path_info + 'sex_specific_variance_betas_' + '_'.join(datasets) + '.xlsx'
df_betas = pd.read_excel(file_betas, header=1)
cpg_list_betas = df_betas['ID_REF'].to_list()
is_in_betas = []
for item in cpg_list:
    if item in cpg_list_betas:
        is_in_betas.append('YES')
    else:
        is_in_betas.append('NO')

df_base.insert(base_column_id, 'IS FOUND IN BETAS', is_in_betas)

file_result = path + 'sex_specific_variance_residuals_' + '_'.join(datasets) + '.xlsx'

writer = pd.ExcelWriter(file_result, engine='xlsxwriter')
df_base.to_excel(writer, index=False, startrow=1)
worksheet = writer.sheets['Sheet1']
worksheet.write(0, 0, 'Sex-associated differentially variable probes calculated on residuals from the intersection')
writer.save()
