import pandas as pd

path = 'C:/Users/User/YandexDisk/pydnameth/variance/betas'
files_names = ['betas_equal.xlsx', 'betas_equal_residuals.xlsx']

files_paths = [path + '\\' + file_name for file_name in files_names]

cpg_dict = dict.fromkeys([file_name[:-5] for file_name in files_names], [])
gene_dict = dict.fromkeys([file_name[:-5] for file_name in files_names], [])
for file_id in range(0, len(files_names)):
    file_name = files_names[file_id][:-5]
    file_path = files_paths[file_id]
    df = pd.read_excel(file_path)
    cpg_dict[file_name] = list(df.cpg)
    gene_dict[file_name] = list(df.gene)

diff_cpgs = set(cpg_dict[files_names[0][:-5]])
for file_id in range(1, len(files_names)):
    file_name = files_names[file_id]
    cpg_data = cpg_dict[file_name[:-5]]
    diff_cpgs = {*diff_cpgs} ^ {*cpg_data}

diff_cpgs = list(diff_cpgs)

# Table for intersection
diff_dict = {}
diff_dict['i'] = []
diff_dict['gene'] = []

for f_id in range(0, len(diff_cpgs)):
    cpg = diff_cpgs[f_id]
    diff_dict['i'].append(cpg)
    gene_id = cpg_dict[files_names[0][:-5]].index(cpg)
    gene = gene_dict[files_names[0][:-5]][gene_id]
    diff_dict['gene'].append(gene)

i_df = pd.DataFrame(diff_dict)
name = '_'.join([file_name[:-5] for file_name in files_names])
writer = pd.ExcelWriter(path + '\\' + name + '_diff.xlsx', engine='xlsxwriter')
i_df.to_excel(writer, index=False, sheet_name='i')
writer.save()
