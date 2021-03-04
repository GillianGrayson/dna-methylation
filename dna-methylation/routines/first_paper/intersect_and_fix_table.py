import pandas as pd

file_common = 'E:/YandexDisk/pydnameth/draft/revision/v8/sex_specific_variance_residuals_GSE40279_GSE87571_EPIC_GSE55763.xlsx'
file_new = 'E:/YandexDisk/pydnameth/variance/residuals/1_2_3_4_with_r2_with_added_info.xlsx'

df_common = pd.read_excel(file_common, header=1)
df_new = pd.read_excel(file_new)

cpg_dict = {'common': list(df_common['ID_REF']), 'new': list(df_new['item'])}
common_cpgs = list(set(cpg_dict['common']).intersection(cpg_dict['new']))

for cpg in common_cpgs:
    if cpg == 'cg26398921':
        o=0
    common_index = list(df_common['ID_REF']).index(cpg)
    new_index = list(df_new['item']).index(cpg)

    datasets = ['GSE40279', 'GSE87571', 'EPIC', 'GSE55763']

    for dataset in datasets:
        i_common = list(df_common['I in ' + dataset])[common_index]
        i_new = list(df_new['increasing_fit_' + dataset])[new_index]

        if i_common > i_new:
            df_new = df_new.replace({'increasing_fit_' + dataset: i_new}, i_common)
        elif i_common < i_new and i_common > 2:
            df_new = df_new.replace({'increasing_fit_' + dataset: i_new}, i_common)
        elif i_common < 2:
            df_new.drop([new_index])
            break

writer = pd.ExcelWriter('E:/YandexDisk/pydnameth/variance/residuals/1_2_3_4_with_r2_with_added_info_corrected.xlsx',
                        engine='xlsxwriter')
df_new.to_excel(writer, index=False)
writer.save()
