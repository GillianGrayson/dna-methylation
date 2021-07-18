import GEOparse
from GEO_parsing.infrastructure.filter import split_words, only_words, get_raw_dict, get_gsm_dict, get_gse_gsm_dict
from GEO_parsing.infrastructure.path import get_data_path, make_dir
from GEO_parsing.routines import get_gsm
from functions.save.table import save_table_dict_xlsx
import os
from tqdm import tqdm
import ntpath

GPL = '13534'
suffix = '06_16_21'

gses = ['GSE156994']

characteristics_key = 'characteristics_ch1'


gsm_raw_dict = get_raw_dict( f'{get_data_path()}/GPL{GPL}/gsm_table_{suffix}')
gsm_dict = get_gsm_dict(f'{get_data_path()}/GPL{GPL}/GPL{GPL}_gsm_dict', gsm_raw_dict)
gse_gsms_dict = get_gse_gsm_dict(f'{get_data_path()}/GPL{GPL}/gse_gsms_dict', gsm_raw_dict, gsm_dict)

all_gses = sorted(gse_gsms_dict.keys(),  key=lambda s: len(gse_gsms_dict.get(s)),  reverse=True)


for gse_id, gse in tqdm(enumerate(gses)):

    path_tmp = f'{get_data_path()}/GPL{GPL}/tmp/{gse}'
    make_dir(path_tmp)

    # Init characteristics dicts
    gsms_exist = []
    gsm_data_dict = {}
    chs_keys = set()
    for gsm_id, gsm in tqdm(enumerate(gse_gsms_dict[gse]), desc='gsms processing'):
        try:
            gsm_data = get_gsm(gsm, f'{path_tmp}/gsms', is_remove=True)
            gsm_data_dict[gsm] = gsm_data
        except GEOparse.GEOparse.NoEntriesException:
            os.remove(f'{path_tmp}/gsms/{gsm}.txt')
            continue
        gsms_exist.append(gsm)
        chs_raw = gsm_data.metadata["characteristics_ch1"]
        for ch in chs_raw:
            ch_split = ch.split(': ')
            chs_keys.update([ch_split[0]])

    gsms_passed = [True] * len(gsm_data_dict)

    chs = {}
    chs['geo_accession'] = []
    #chs['description'] = []
    chs['title'] = []
    chs['source_name'] = []
    chs['Sample_Name'] = []
    chs['Sentrix_Position'] = []
    chs['Sentrix_ID'] = []
    for key in chs_keys:
        chs[key] = []

    for gsm_id, gsm in enumerate(gsm_data_dict):

        gsm_data = gsm_data_dict[gsm]

        if gsm_data.metadata['supplementary_file'][0] != 'NONE':
            supp_file = gsm_data.metadata['supplementary_file'][0]
            head, tail = ntpath.split(supp_file)
            tmp = os.path.splitext(tail)[0][0:-9]
            pd_parts = tmp.split('_')
            chs['Sample_Name'].append(pd_parts[0])
            chs['Sentrix_ID'].append(pd_parts[1])
            chs['Sentrix_Position'].append(pd_parts[2])
        else:
            chs['Sample_Name'].append(gsm)
            chs['Sentrix_ID'].append('')
            chs['Sentrix_Position'].append('')

        chs['geo_accession'].append(gsm_data.metadata['geo_accession'][0])
        #chs['description'].append(gsm_data.metadata['description'][0])
        chs['title'].append(gsm_data.metadata['title'][0])
        chs['source_name'].append(gsm_data.metadata['source_name_ch1'][0])

        chs_raw = gsm_data.metadata["characteristics_ch1"]
        exist_chs = []
        for ch in chs_raw:
            ch_split = ch.split(': ')
            if ch_split[0] not in exist_chs:
                exist_chs.append(ch_split[0])
                ch_value = ': '.join(ch_split[1::])
                chs[ch_split[0]].append(ch_value)
                separate_words = set(only_words(split_words(ch_value.lower())))
        missed_chs = list(chs_keys.difference(exist_chs))
        for ch in missed_chs:
            chs[ch].append('NA')

    save_table_dict_xlsx(f'{path_tmp}/pheno.xlsx', chs)
