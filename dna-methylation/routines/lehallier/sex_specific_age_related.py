from routines.lehallier.infrastructure import get_lehallier_data_path, load_table_dict_xlsx, save_table_dict_xlsx
from routines.lehallier.venn_diagram import plot_venn
from tqdm import tqdm
import numpy as np
import collections


def get_genes_from_file(fn):
    sex_specific_data_dict = load_table_dict_xlsx(fn)
    sex_specific_genes_raw = sex_specific_data_dict['aux']
    print(f'number of cpgs: {len(sex_specific_genes_raw)}')

    genes_list = []
    for gene_raw in sex_specific_genes_raw:
        if isinstance(gene_raw, str):
            curr_genes = gene_raw.split(';')
            genes_list += curr_genes

    return list(set(genes_list))


def get_genes(data_dict):
    genes_raw = data_dict['aux']
    print(f'number of cpgs: {len(genes_raw)}')

    genes_list = []
    for gene_raw in genes_raw:
        if isinstance(gene_raw, str):
            curr_genes = gene_raw.split(';')
            genes_list += curr_genes

    return list(set(genes_list))

suffix = '_bonferroni'


fn = get_lehallier_data_path() + '/' + 'proteins_genes.xlsx'
proteins_genes_data_dict = load_table_dict_xlsx(fn)

id_gene = {}
gene_id = {}
suspect_rows = []
suspect_ids = []
for row_id in tqdm(range(0, len(proteins_genes_data_dict['ID']))):
    id = proteins_genes_data_dict['ID'][row_id]
    gene = proteins_genes_data_dict['EntrezGeneSymbol'][row_id]

    if gene in gene_id:
        gene_id[gene].append(id)
    else:
        gene_id[gene] = [id]

    if id in id_gene:
        suspect_rows.append(row_id)
        suspect_ids.append(id)
    if isinstance(gene, str):
        id_gene[id] = gene
    else:
        suspect_rows.append(row_id)
        suspect_ids.append(id)
suspect_rows = [x + 2 for x in suspect_rows]
np.savetxt(get_lehallier_data_path() + '/' + 'suspect_rows.txt', suspect_rows, fmt='%d')
np.savetxt(get_lehallier_data_path() + '/' + 'suspect_ids.txt', suspect_ids, fmt='%s')


fn = get_lehallier_data_path() + '/' + 'age_sex.xlsx'
age_sex_data_dict = load_table_dict_xlsx(fn)
id_age_q = {}
id_sex_q = {}

for row_id in range(0, len(age_sex_data_dict['ID'])):
    id = age_sex_data_dict['ID'][row_id]
    age_q = age_sex_data_dict['q.Age'][row_id]
    sex_q = age_sex_data_dict['q.Sex'][row_id]

    id_age_q[id] = age_q
    id_sex_q[id] = sex_q

ar_genes_lehallier = []
ss_genes_lehallier = []
ssar_genes_lehallier = []
for id, gene in id_gene.items():
    if id_age_q[id] < 0.05:
        ar_genes_lehallier.append(gene)
    if id_sex_q[id] < 0.05:
        ss_genes_lehallier.append(gene)
    if id_age_q[id] < 0.05 and id_sex_q[id] < 0.05:
        ssar_genes_lehallier.append(gene)

print(f'Number of sex-specific (SS) genes in Lehallier, et. al.: {len(ss_genes_lehallier)}')
print(f'Number of unique sex-specific (SS) genes in Lehallier, et. al.: {len(set(ss_genes_lehallier))}')
genes_duplicates = [item for item, count in collections.Counter(ss_genes_lehallier).items() if count > 1]
genes_duplicates_str = {'id':[], 'gene':[]}
for gene in genes_duplicates:
    ids = gene_id[gene]
    for id in ids:
        genes_duplicates_str['id'].append(id)
        genes_duplicates_str['gene'].append(gene)
save_table_dict_xlsx(get_lehallier_data_path() + '/' + 'duplicates_ss', genes_duplicates_str)

fn = get_lehallier_data_path() + '/methylation/GSE87571/' + 'sex_specific' + suffix + '.xlsx'
genes_GSE87571 = get_genes_from_file(fn)
print(f'Number of sex-specific (SS) genes in GSE87571: {len(genes_GSE87571)}')

fn = get_lehallier_data_path() + '/methylation/liver/' + 'sex_specific' + suffix + '.xlsx'
genes_liver = get_genes_from_file(fn)
print(f'Number of sex-specific (SS) genes in liver: {len(genes_liver)}')

lists = [ss_genes_lehallier, genes_GSE87571, genes_liver]
labels = ['lehallier', 'GSE87571', 'liver']

plot_venn(lists, labels, get_lehallier_data_path() + '/methylation', 'ss' + suffix)



print(f'Number of age-related (ar) genes in Lehallier, et. al.: {len(ar_genes_lehallier)}')
print(f'Number of unique age-related (ar) genes in Lehallier, et. al.: {len(set(ar_genes_lehallier))}')
genes_duplicates = [item for item, count in collections.Counter(ar_genes_lehallier).items() if count > 1]
genes_duplicates_str = {'id':[], 'gene':[]}
for gene in genes_duplicates:
    ids = gene_id[gene]
    for id in ids:
        genes_duplicates_str['id'].append(id)
        genes_duplicates_str['gene'].append(gene)
save_table_dict_xlsx(get_lehallier_data_path() + '/' + 'duplicates_ar', genes_duplicates_str)

fn = get_lehallier_data_path() + '/methylation/GSE87571/' + 'age_related' + suffix + '.xlsx'
genes_GSE87571 = get_genes_from_file(fn)
print(f'Number of age-related (AR) genes in GSE87571: {len(genes_GSE87571)}')

fn = get_lehallier_data_path() + '/methylation/liver/' + 'age_related' + suffix + '.xlsx'
genes_liver = get_genes_from_file(fn)
print(f'Number of age-related (AR) genes in liver: {len(genes_liver)}')

lists = [ar_genes_lehallier, genes_GSE87571, genes_liver]
labels = ['lehallier', 'GSE87571', 'liver']

plot_venn(lists, labels, get_lehallier_data_path() + '/methylation', 'ar' + suffix)


print(f'Number of sex-specific age-related (ssae) genes in Lehallier, et. al.: {len(ssar_genes_lehallier)}')
print(f'Number of unique sex-specific age-related (ssae) genes in Lehallier, et. al.: {len(set(ssar_genes_lehallier))}')
genes_duplicates = [item for item, count in collections.Counter(ar_genes_lehallier).items() if count > 1]
genes_duplicates_str = {'id':[], 'gene':[]}
for gene in genes_duplicates:
    ids = gene_id[gene]
    for id in ids:
        genes_duplicates_str['id'].append(id)
        genes_duplicates_str['gene'].append(gene)
save_table_dict_xlsx(get_lehallier_data_path() + '/' + 'duplicates_ssar', genes_duplicates_str)

fn = get_lehallier_data_path() + '/methylation/GSE87571/' + 'sex_specific_age_related' + suffix + '.xlsx'
genes_GSE87571 = get_genes_from_file(fn)
print(f'Number of sex-specific age-related (SSAR) genes in GSE87571: {len(genes_GSE87571)}')

fn = get_lehallier_data_path() + '/methylation/liver/' + 'sex_specific_age_related' + suffix + '.xlsx'
genes_liver = get_genes_from_file(fn)
print(f'Number of sex-specific age-related (SSAR) genes in liver: {len(genes_liver)}')

lists = [ssar_genes_lehallier, genes_GSE87571, genes_liver]
labels = ['lehallier', 'GSE87571', 'liver']

plot_venn(lists, labels, get_lehallier_data_path() + '/methylation', 'ssar' + suffix)




# fn = get_lehallier_data_path() + '/GSE87571/' + 'genes.xlsx'
# all_genes_meth = get_genes(fn)
# print(f'Number of genes from methylation: {len(all_genes_meth)}')
#
# x = len(ssar_intersection)
# n = len(ssar_genes_meth)
# m = len(set(ssar_genes_lehallier))
# N1 = len(set(id_gene.values()))
# N2 = len(all_genes_meth)
