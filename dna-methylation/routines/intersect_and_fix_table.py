import pandas as pd


filenames = ['sex_specific_variance_residuals_GSE40279_GSE87571_EPIC_GSE55763.xlsx',
             'sex_specific_variance_residuals_GSE87571.xlsx']

path = 'D:/YandexDisk/pydnameth/draft/revision/v8'
files_path = [path + '\\' + file_name for file_name in filenames]

df_all = pd.read_excel(files_path[0], header=1)
df_gse87571 = pd.read_excel(files_path[1], header=1)

cpg_dict = {'all': list(df_all['ID_REF']), 'gse87571': list(df_gse87571['cpg'])}
common_cpgs = list(set(cpg_dict['all']).intersection(cpg_dict['gse87571']))

for cpg in common_cpgs:
    all_index = list(df_all['ID_REF']).index(cpg)
    gse87571_index = list(df_gse87571['cpg']).index(cpg)

    i_all = list(df_all['I in GSE87571'])[all_index]
    i_gse87571 = list(df_gse87571['increasing_fit'])[gse87571_index]

    if i_all > i_gse87571:
        df_gse87571 = df_gse87571.replace({'increasing_fit': i_gse87571}, i_all)
    elif i_all < i_gse87571 and i_all > 2:
        df_gse87571 = df_gse87571.replace({'increasing_fit': i_gse87571}, i_all)
    elif i_all < 2:
        df_gse87571 = df_gse87571.drop([gse87571_index])

writer = pd.ExcelWriter(path + '\\' +'sex_specific_variance_residulas_GSE87571_corrected.xlsx', engine='xlsxwriter')
df_gse87571.to_excel(writer, index=False)
writer.save()
