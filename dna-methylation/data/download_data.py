import GEOparse
from GEOparse.utils import download_from_url
from data.routines.routines import is_float
from data.infrastructure.path import get_data_path, make_dir
from data.infrastructure.load.table import load_table_dict_xlsx, load_table_dict_pkl
from data.infrastructure.save.table import save_table_dict_pkl, save_table_dict_xlsx, save_table_dict_csv
import os
from tqdm import tqdm
import re
import gzip
import shutil
import ntpath
from distutils.dir_util import copy_tree


def split_words(text):
    rgx = re.compile(r"((?:(?<!'|\w)(?:\w-?'?)+(?<!-))|(?:(?<='|\w)(?:\w-?'?)+(?=')))")
    return rgx.findall(text)

def only_words(words):
    passed_words = []
    for word in words:
        if not is_float(word):
            passed_words.append(word)
    return passed_words


GPL = '13534'
suffix = '03_03_20'

gsm_key = 'gsm'
gse_key = 'series_id'
source_key = 'source_name_ch1'
characteristics_key = 'characteristics_ch1'

target_dir = f'{get_data_path()}/GPL{GPL}/filtered/brain'

fn_xlsx = f'{get_data_path()}/GPL{GPL}/GPL{GPL}_gsm_table_{suffix}.xlsx'
fn_pkl = f'{get_data_path()}/GPL{GPL}/GPL{GPL}_gsm_table_{suffix}.pkl'
if os.path.isfile(fn_pkl):
    gsm_raw_dict = load_table_dict_pkl(fn_pkl)
else:
    gsm_raw_dict = load_table_dict_xlsx(fn_xlsx)
    save_table_dict_pkl(fn_pkl, gsm_raw_dict)

gsms = gsm_raw_dict[gsm_key]

# data_dict_passed
fn_pkl = f'{get_data_path()}/GPL{GPL}/GPL{GPL}_gsm_dict.pkl'
if os.path.isfile(fn_pkl):
    gsm_dict = load_table_dict_pkl(fn_pkl)
else:
    gsm_dict = {}

    for key in tqdm(gsm_raw_dict, desc='gsm_dict processing'):
        gsm_dict[key] = {}
        for index, gsm in enumerate(gsms):
            gsm_dict[key][gsm] = gsm_raw_dict[key][index]

    save_table_dict_pkl(fn_pkl, gsm_dict)

# gse_gsms_dict
fn_pkl = f'{get_data_path()}/GPL{GPL}/gse_gsms_dict.pkl'
if os.path.isfile(fn_pkl):
    gse_gsms_dict = load_table_dict_pkl(fn_pkl)
else:
    gses = set()
    for gses_raw in gsm_raw_dict[gse_key]:
        gses_curr = gses_raw.split(',')
        for gse in gses_curr:
            gses.add(gse)
    gses = list(gses)

    gse_gsms_dict = {}
    for gse in gses:
        gse_gsms_dict[gse] = []

    for gsm in gsms:
        gses_raw = gsm_dict[gse_key][gsm]
        gses_curr = gses_raw.split(',')
        for gse in gses_curr:
            gse_gsms_dict[gse].append(gsm)

    save_table_dict_pkl(fn_pkl, gse_gsms_dict)


gses = [f.name for f in os.scandir(target_dir) if f.is_dir()]
gses.sort()
gses = gses[::-1]

gse_gsms_passed_dict = {}
gse_passed_dict = {}

for gse in tqdm(gses):

    path_data = f'{target_dir}/{gse}/raw_data'
    make_dir(path_data)

    gsms = gse_gsms_dict[gse]
    gsms_exist = []

    base_names = {}

    chs_keys = set()
    for gsm_id, gsm in enumerate(gsms):
        try:
            while True:
                try:
                    gsm_data = GEOparse.get_GEO(geo=gsm, destdir=f'{path_data}', include_data=True, how="")
                    if len(gsm_data.metadata['supplementary_file']) > 0:
                        tail = ''
                        for supp_file in gsm_data.metadata['supplementary_file']:
                            head, tail = ntpath.split(supp_file)
                            download_from_url(supp_file, f'{path_data}/{tail}')
                            with gzip.open( f'{path_data}/{tail}', 'rb') as f_in:
                                with open( f'{path_data}/{tail[:-3]}', 'wb') as f_out:
                                    shutil.copyfileobj(f_in, f_out)
                            os.remove(f'{path_data}/{tail}')
                        base_names[gsm] = os.path.splitext(tail)[0]
                except ValueError:
                    continue
                except ConnectionError:
                    continue
                break
        except GEOparse.GEOparse.NoEntriesException:
            os.remove(f'{path_data}/{gsm}.txt')
            continue
        gsms_exist.append(gsm)
        chs_raw = gsm_data.metadata[characteristics_key]
        for ch in chs_raw:
            ch_split = ch.split(': ')
            chs_keys.update([ch_split[0]])

    gsms = gsms_exist
    gsms_passed = [True] * len(gsms)

    chs = {}
    chs['geo_accession'] = []
    chs['base_name'] = []
    for key in chs_keys:
        chs[key] = []

    for gsm_id, gsm in enumerate(gsms):
        chs['base_name'] = base_names[gsm]

        gsm_data = GEOparse.get_GEO(geo=gsm, destdir=f'{path_data}', include_data=False, how="")

        gsm_is_passed = True

        chs['geo_accession'].append(gsm_data.metadata['geo_accession'][0])

        chs_raw = gsm_data.metadata[characteristics_key]
        exist_chs = []
        for ch in chs_raw:
            ch_split = ch.split(': ')
            if ch_split[0] not in exist_chs:
                exist_chs.append(ch_split[0])
                ch_value = ': '.join(ch_split[1::])
                chs[ch_split[0]].append(ch_value)

        missed_chs = list(chs_keys.difference(exist_chs))
        for ch in missed_chs:
            chs[ch].append('NA')

        gsms_passed[gsm_id] = gsm_is_passed

    save_table_dict_csv(f'{path_data}/observables', chs)
