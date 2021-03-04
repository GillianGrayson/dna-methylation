import pandas as pd

path = 'E:/YandexDisk/pydnameth/draft/revision/v11/'

datasets = ['GSE40279', 'GSE87571', 'EPIC', 'GSE55763']
data_types = ['betas', 'residuals']

for dataset in datasets:
    for data_type in data_types:
        file_new = path + 'increasing_type_' + data_type + '_' + dataset + '.xlsx'
        df_new = pd.read_excel(file_new, header=0).to_dict('list')

        file_base = path + 'sex_specific_variance_' + data_type + '_' + dataset + '.xlsx'
        table_header = pd.read_excel(file_base, header=None).iat[0, 0]
        df_base = pd.read_excel(file_base, header=1)
        cpg_list = df_base['ID_REF'].to_list()

        increasing_type_f = []
        increasing_type_m = []
        for item in cpg_list:
            index = df_new['item'].index(item)
            increasing_type_f.append(df_new['increasing_type_F'][index])
            increasing_type_m.append(df_new['increasing_type_M'][index])

        df_base.insert(7, 'VARIANCE CHANGING TYPE IN F', increasing_type_f)
        df_base.insert(8, 'VARIANCE CHANGING TYPE IN M', increasing_type_m)

        df_base.rename(columns={'VARIANCE INCREASES MORE IN': 'VARIANCE CHANGES MORE IN'}, inplace=True)

        file_result = path + 'sex_specific_variance_' + data_type + '_' + dataset + '_new.xlsx'

        writer = pd.ExcelWriter(file_result, engine='xlsxwriter')
        df_base.to_excel(writer, index=False, startrow=1)
        worksheet = writer.sheets['Sheet1']
        worksheet.write(0, 0, table_header)
        writer.save()

for data_type in data_types:
    df_new = {'GSE40279': {},
              'GSE87571': {},
              'EPIC': {},
              'GSE55793': {}}
    for dataset in datasets:
        file_new = path + 'increasing_type_' + data_type + '_' + dataset + '.xlsx'
        df_new[dataset] = pd.read_excel(file_new, header=0).to_dict('list')

    file_base = path + 'sex_specific_variance_' + data_type + '_' + '_'.join(datasets) + '.xlsx'
    table_header = pd.read_excel(file_base, header=None).iat[0, 0]
    df_base = pd.read_excel(file_base, header=1)
    cpg_list = df_base['ID_REF'].to_list()

    increasing_type = {'GSE40279': {'F': [], 'M': []},
                       'GSE87571': {'F': [], 'M': []},
                       'EPIC': {'F': [], 'M': []},
                       'GSE55763': {'F': [], 'M': []}}

    for item in cpg_list:
        for dataset in datasets:
            index = df_new[dataset]['item'].index(item)
            increasing_type[dataset]['F'].append(df_new[dataset]['increasing_type_F'][index])
            increasing_type[dataset]['M'].append(df_new[dataset]['increasing_type_M'][index])

    base_column_id = 11
    for dataset in datasets:
        df_base.insert(base_column_id, 'VARIANCE CHANGING TYPE IN F IN ' + dataset, increasing_type[dataset]['F'])
        base_column_id += 1
        df_base.insert(base_column_id, 'VARIANCE CHANGING TYPE IN M IN ' + dataset, increasing_type[dataset]['M'])
        base_column_id += 1

    file_result = path + 'sex_specific_variance_' + data_type + '_' + '_'.join(datasets) + '_new.xlsx'

    writer = pd.ExcelWriter(file_result, engine='xlsxwriter')
    df_base.to_excel(writer, index=False, startrow=1)
    worksheet = writer.sheets['Sheet1']
    worksheet.write(0, 0, table_header)
    writer.save()
