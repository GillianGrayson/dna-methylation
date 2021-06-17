import GEOparse
from GEO_parsing.infrastructure.filter import split_words, only_words, get_raw_dict, get_gsm_dict, get_gse_gsm_dict
from GEO_parsing.infrastructure.path import get_data_path, make_dir
from GEO_parsing.routines import get_gsm
from functions.save.table import save_table_dict_xlsx
import os
from tqdm import tqdm

GPL = '13534'
suffix = '06_16_21'

gses = ['GSE87640']

gsm_key = 'gsm'
gse_key = 'series_id'
source_key = 'source_name_ch1'
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
        chs_raw = gsm_data.metadata[characteristics_key]
        for ch in chs_raw:
            ch_split = ch.split(': ')
            chs_keys.update([ch_split[0]])

    gsms_passed = [True] * len(gsm_data_dict)

    chs = {}
    chs['geo_accession'] = []
    for key in chs_keys:
        chs[key] = []

    for gsm_id, gsm in enumerate(gsm_data_dict):

        gsm_data = gsm_data_dict[gsm]
        chs['geo_accession'].append(gsm_data.metadata['geo_accession'][0])
        chs_raw = gsm_data.metadata[characteristics_key]
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

    save_table_dict_xlsx(f'{path_tmp}/observables.xlsx', chs)
