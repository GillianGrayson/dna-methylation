import pandas as pd

import itertools

path = 'E:/YandexDisk/Work/pydnameth/intersection'

base = 'variance.xlsx'

tables = [
    '2014 [Hall] 450k female more male CpGs.xlsx',
    '2014 [Hall] 450k male more female CpGs.xlsx',
    '2015 [Inoshita] 450k sex-specific CpGs with cells.xlsx',
    '2015 [Inoshita] 450k sex-specific CpGs without cells.xlsx',
    '2015 [Mamrut] 450k Integrative analysis of methylome and transcriptome in human blood.xlsx',
    '2015 [Singmann] 450k sex-specific CpGs.xlsx',
    '2015 [Yousefi] 450k sex-specific CpGs.xlsx',
    '2017 [White] 450k CD4T.xlsx',
    '2017 [White] 450k CD8T.xlsx',
    '2017 [White] 450k CD14Mono.xlsx',
    '2017 [White] 450k CD19B.xlsx',
    '2017 [White] 450k Lymphocyte_I.xlsx',
    '2017 [White] 450k Lymphocyte_II.xlsx',
    '2017 [White] 450k Myeloid.xlsx',
    '2017 [White] 450k Neu.xlsx',
    '2017 [White] 450k NK.xlsx',
    '2017 [White] 450k PanT.xlsx'
]

base_fn = path + '/' + base
df = pd.read_excel(base_fn)
base_items = list(df.item)
base_aux = list(df.aux)
base_aux = [x for x in base_aux if x != '']

print(base)

for table in tables:
    table_fn = path + '/' + table
    df = pd.read_excel(table_fn)
    table_items = list(df.item)
    table_aux = list(df.aux)
    table_aux = [x for x in table_aux if x != '']

    i_items = set(base_items).intersection(set(table_items))
    i_items = list(i_items)

    print(table + ': ' + str(len(i_items)) + ' from ' + str(len(table_items)))