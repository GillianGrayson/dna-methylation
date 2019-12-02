from routines.lehallier.infrastructure import get_lehallier_data_path, load_table_dict_xlsx
from routines.lehallier.venn_diagram import plot_venn
from tqdm import tqdm
import numpy as np


def get_genes(fn):
    sex_specific_data_dict = load_table_dict_xlsx(fn)
    sex_specific_genes_raw = sex_specific_data_dict['aux']

    genes_list = []
    for gene_raw in sex_specific_genes_raw:
        if isinstance(gene_raw, str):
            curr_genes = gene_raw.split(';')
            genes_list += curr_genes

    return list(set(genes_list))


fn = get_lehallier_data_path() + '/' + 'proteins_genes.xlsx'
proteins_genes_data_dict = load_table_dict_xlsx(fn)

id_gene = {}

for row_id in tqdm(range(0, len(proteins_genes_data_dict['ID']))):
    id = proteins_genes_data_dict['ID'][row_id]
    gene = proteins_genes_data_dict['EntrezGeneSymbol'][row_id]
    if isinstance(gene, str):
        id_gene[id] = gene


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

fn = get_lehallier_data_path() + '/methylation/GSE87571/' + 'sex_specific.xlsx'
genes_GSE87571 = get_genes(fn)
print(f'Number of sex-specific (SS) genes in GSE87571: {len(genes_GSE87571)}')

fn = get_lehallier_data_path() + '/methylation/liver/' + 'sex_specific.xlsx'
genes_liver = get_genes(fn)
print(f'Number of sex-specific (SS) genes in liver: {len(genes_liver)}')

lists = [ss_genes_lehallier, genes_GSE87571, genes_liver]
labels = ['lehallier', 'GSE87571', 'liver']
suffix = 'ss'

plot_venn(lists, labels, get_lehallier_data_path() + '/methylation', suffix)



print(f'Number of age-related (ar) genes in Lehallier, et. al.: {len(ar_genes_lehallier)}')
print(f'Number of unique age-related (ar) genes in Lehallier, et. al.: {len(set(ar_genes_lehallier))}')

fn = get_lehallier_data_path() + '/methylation/GSE87571/' + 'age_related.xlsx'
genes_GSE87571 = get_genes(fn)
print(f'Number of age-related (AR) genes in GSE87571: {len(genes_GSE87571)}')

fn = get_lehallier_data_path() + '/methylation/liver/' + 'age_related.xlsx'
genes_liver = get_genes(fn)
print(f'Number of age-related (AR) genes in liver: {len(genes_liver)}')

lists = [ar_genes_lehallier, genes_GSE87571, genes_liver]
labels = ['lehallier', 'GSE87571', 'liver']
suffix = 'ar'

plot_venn(lists, labels, get_lehallier_data_path() + '/methylation', suffix)



print(f'Number of sex-specific age-related (ssae) genes in Lehallier, et. al.: {len(ssar_genes_lehallier)}')
print(f'Number of unique sex-specific age-related (ssae) genes in Lehallier, et. al.: {len(set(ssar_genes_lehallier))}')




# fn = get_lehallier_data_path() + '/GSE87571/' + 'genes.xlsx'
# all_genes_meth = get_genes(fn)
# print(f'Number of genes from methylation: {len(all_genes_meth)}')
#
# x = len(ssar_intersection)
# n = len(ssar_genes_meth)
# m = len(set(ssar_genes_lehallier))
# N1 = len(set(id_gene.values()))
# N2 = len(all_genes_meth)
