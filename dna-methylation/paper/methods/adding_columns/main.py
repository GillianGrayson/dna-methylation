from paper.routines.infrastructure.load.table import load_table_dict_by_key_xlsx, load_table_dict_xlsx
from paper.routines.infrastructure.save.table import save_table_dict_xlsx

# dataset = 'GSE55763'
#
# source_fn = f'E:/YandexDisk/Work/pydnameth/approaches/ancova/{dataset}.xlsx'
# source_keys = ['x:category_pval']

# target_fn = 'E:/YandexDisk/Work/pydnameth/draft/fixes/materials_and_methods/common/supplementary_file_1_tmp.xlsx'
# target_main_key = 'CpG'
# target_keys = [f'interaction p-value ({dataset})']

source_fn = f'E:/YandexDisk/Work/pydnameth/approaches/ancova/p_bh_ancova.xlsx'
source_keys = ['P-value']

target_fn = 'E:/YandexDisk/Work/pydnameth/draft/fixes/materials_and_methods/common/supplementary_file_1_tmp.xlsx'
target_main_key = 'CpG'
target_keys = [f'METAL interaction p-value']

save_fn = 'E:/YandexDisk/Work/pydnameth/draft/fixes/materials_and_methods/common/supplementary_file_1_tmp'

source_dict = load_table_dict_by_key_xlsx(source_fn, 'MarkerName')
target_dict = load_table_dict_xlsx(target_fn)

for key in target_keys:
    target_dict[key] = []
for item in target_dict[target_main_key]:
    for key_id, key  in enumerate(target_keys):
        if item in source_dict[source_keys[key_id]]:
            target_dict[key].append(source_dict[source_keys[key_id]][item])
        else:
            target_dict[key].append('NA')

save_table_dict_xlsx(save_fn, target_dict)
