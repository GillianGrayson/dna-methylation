import pandas as pd

data_file_path = 'D:/YandexDisk/Work/pydnameth/draft/variance/residuals/'
data_file_name = 'residuals_GSE87571.xlsx'

df = pd.read_excel(data_file_path + data_file_name)
genes = list(df.gene)

gene_list = []

for item in genes:
    if not isinstance(item, float):
        curr_genes = item.split(";")
        gene_list.extend(curr_genes)

gene_set = set(gene_list)

gene_data = pd.DataFrame(gene_set)
writer = pd.ExcelWriter(data_file_path + '\\' + data_file_name[:-5] + '_genes_set' + '.xlsx', engine='xlsxwriter')
gene_data.to_excel(writer, index=False, sheet_name='i', header=False)
writer.save()
