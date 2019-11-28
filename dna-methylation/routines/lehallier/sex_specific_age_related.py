from routines.lehallier.infrastructure import get_lehallier_data_path, get_sex_specific_data_path, load_table_dict_xlsx
from tqdm import tqdm
import scipy.stats as stats
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

fn = get_lehallier_data_path() + '/GSE87571/' + 'sex_specific_age_related.xlsx'
ssar_genes_meth = get_genes(fn)
print(f'Number of sex-specific age-related (ar) genes in our draft: {len(ssar_genes_meth)}')

fn = get_lehallier_data_path() + '/GSE87571/' + 'genes.xlsx'
all_genes_meth = get_genes(fn)
print(f'Number of genes from methylation: {len(all_genes_meth)}')


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

print(f'Number of age-related (ar) genes in Lehallier, et. al.: {len(ar_genes_lehallier)}')
print(f'Number of unique age-related (ar) genes in Lehallier, et. al.: {len(set(ar_genes_lehallier))}')
print(f'Number of sex-specific (ss) genes in Lehallier, et. al.: {len(ss_genes_lehallier)}')
print(f'Number of unique sex-specific (ss) genes in Lehallier, et. al.: {len(set(ss_genes_lehallier))}')
print(f'Number of sex-specific age-related (ssae) genes in Lehallier, et. al.: {len(ssar_genes_lehallier)}')
print(f'Number of unique sex-specific age-related (ssae) genes in Lehallier, et. al.: {len(set(ssar_genes_lehallier))}')

ssar_intersection = set(ssar_genes_meth).intersection(set(ssar_genes_lehallier))
print(f'Number of sex-specific age-related (ssar) genes in intersection: {len(ssar_intersection)}')
print(ssar_intersection)

x = len(ssar_intersection)
n = len(ssar_genes_meth)
m = len(set(ssar_genes_lehallier))
N1 = len(set(id_gene.values()))
N2 = len(all_genes_meth)

contingency_table = [[x, m - x], [n - x, N2 - n - m + x]]
print(contingency_table)

a = np.sum(contingency_table, axis=0)
b = np.sum(contingency_table, axis=1)
if np.sum(a) == np.sum(b):
    print('contingency_table is ok')

oddsratio, pvalue = stats.fisher_exact(contingency_table)
print(f'oddsratio: {oddsratio}')
print(f'pvalue: {pvalue}')
