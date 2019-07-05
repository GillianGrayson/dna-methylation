import pandas as pd

cpg_file_path = 'D:/Aaron/Bio/variance/v19/'
cpg_file_name = 'Supp_variance.xlsx'

data_file_path = 'C:/Users/User/YandexDisk/pydnameth/GSE87571/'
data_file_name = 'annotations.txt'

df = pd.read_excel(cpg_file_path + cpg_file_name)
data_dict = {}
data_dict['ID_REF'] = list(df.cpg)
data_dict['UCSC_REFGENE_NAME'] = []
data_dict['MAPINFO'] = []
data_dict['CHR'] = []
data_dict['RELATION_TO_UCSC_CPG_ISLAND'] = []
data_dict['UCSC_REFGENE_GROUP'] = []
data_dict['MEAN_I'] = list(df.mean_I)

keys = [
    'ID_REF',
    'UCSC_REFGENE_NAME',
    'MAPINFO',
    'CHR',
    'RELATION_TO_UCSC_CPG_ISLAND',
    'UCSC_REFGENE_GROUP'
]

cpg_info_dict = {}
for key in keys:
    cpg_info_dict[key] = []

f = open(data_file_path + data_file_name)
key_line = f.readline()
header_keys = key_line.split("\t")
header_keys = [x.rstrip() for x in header_keys]
for line in f:
    values = line.split('\t')
    for key_id in range(0, len(keys)):
        index = header_keys.index(keys[key_id])
        cpg_info_dict[keys[key_id]].append(values[index])
f.close()

for id in range(0,len(data_dict['ID_REF'])):
    curr_cpg = data_dict['ID_REF'][id]
    index = cpg_info_dict['ID_REF'].index(curr_cpg)
    data_dict['UCSC_REFGENE_NAME'].append(cpg_info_dict['UCSC_REFGENE_NAME'][index])
    data_dict['MAPINFO'].append(cpg_info_dict['MAPINFO'][index])
    data_dict['CHR'].append(cpg_info_dict['CHR'][index])
    data_dict['RELATION_TO_UCSC_CPG_ISLAND'].append(cpg_info_dict['RELATION_TO_UCSC_CPG_ISLAND'][index])
    data_dict['UCSC_REFGENE_GROUP'].append(cpg_info_dict['UCSC_REFGENE_GROUP'][index])

data = pd.DataFrame(data_dict)
writer = pd.ExcelWriter(cpg_file_path + '\\' + cpg_file_name[:-5] + '_info' + '.xlsx', engine='xlsxwriter')
data.to_excel(writer, index=False, sheet_name='i')
writer.save()

