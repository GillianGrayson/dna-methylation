import pandas as pd

path = 'C:/Users/user/Desktop/sex_specific'
files_names = ['1.xlsx', '2.xlsx', '3.xlsx', '4.xlsx']

files_paths = [path + '\\' + file_name for file_name in files_names]

cpg_dict = dict.fromkeys([file_name[:-5] for file_name in files_names], [])
gene_dict = dict.fromkeys([file_name[:-5] for file_name in files_names], [])
for file_id in range(0, len(files_names)):
    file_name = files_names[file_id][:-5]
    file_path = files_paths[file_id]
    df = pd.read_excel(file_path)
    cpg_dict[file_name] = list(df.item)
    gene_dict[file_name] = list(df.aux)

u_cpgs = set(cpg_dict[files_names[0][:-5]])
for file_id in range(1, len(files_names)):
    file_name = files_names[file_id]
    cpg_data = cpg_dict[file_name[:-5]]
    u_cpgs = set(u_cpgs.union(cpg_data))

u_cpgs = list(u_cpgs)

# Table for intersection
u_dict = {}
u_dict['item'] = []
u_dict['aux'] = []

for f_id in range(0, len(u_cpgs)):
    cpg = u_cpgs[f_id]
    u_dict['item'].append(cpg)
    for file_id in range(0, len(files_names)):
        if cpg in cpg_dict[files_names[file_id][:-5]]:
            gene_id = cpg_dict[files_names[file_id][:-5]].index(cpg)
            gene = gene_dict[files_names[file_id][:-5]][gene_id]
            break
    u_dict['aux'].append(gene)

i_df = pd.DataFrame(u_dict)
name = 'union_' + '_'.join([file_name[:-5] for file_name in files_names])
writer = pd.ExcelWriter(path + '\\' + name + '.xlsx', engine='xlsxwriter')
i_df.to_excel(writer, index=False, sheet_name='u')
writer.save()
