import GEOparse
import numpy as np
from GEO_parsing.infrastructure.filter import split_words, only_words, get_raw_dict, get_gsm_dict, get_gse_gsm_dict
from GEO_parsing.infrastructure.path import get_data_path, make_dir
from GEO_parsing.routines import get_gsm
from functions.load.table import load_table_dict_xlsx, load_table_dict_pkl
from functions.save.table import save_table_dict_pkl, save_table_dict_xlsx
from functions.routines import is_float
import os
from tqdm import tqdm
import re
from distutils.dir_util import copy_tree


GPL = '13534'
suffix = '06_16_21'

num_subj = 200

gsm_raw_dict = get_raw_dict( f'{get_data_path()}/GPL{GPL}/gsm_table_{suffix}')
gsm_dict = get_gsm_dict(f'{get_data_path()}/GPL{GPL}/GPL{GPL}_gsm_dict', gsm_raw_dict)
gse_gsms_dict = get_gse_gsm_dict(f'{get_data_path()}/GPL{GPL}/gse_gsms_dict', gsm_raw_dict, gsm_dict)

fn = f'{get_data_path()}/GPL{GPL}/bad_words.txt'
f = open(fn)
bad_words = set(f.read().splitlines())
f.close()

fn = f'{get_data_path()}/GPL{GPL}/target_chs.txt'
f = open(fn)
target_chs = set(f.read().splitlines())
f.close()

gsms = gsm_raw_dict["gsm"]

gses = sorted(gse_gsms_dict.keys(),  key=lambda s: len(gse_gsms_dict.get(s)),  reverse=True)

np.savetxt(f'{get_data_path()}/GPL{GPL}/gses.txt', gses, fmt='%s')

source_unique_words = set()
ch_unique_words = set()

gse_gsms_passed_dict = {}
gse_passed_dict = {}
gse_good_ones = []

for gse_id, gse in tqdm(enumerate(gses)):

    if len(gse_gsms_dict[gse]) < num_subj:
        break

    path_tmp = f'{get_data_path()}/GPL{GPL}/tmp'
    make_dir(path_tmp)

    curr_gsms = gse_gsms_dict[gse]

    # Init characteristics dicts
    gsm = curr_gsms[0]
    try:
        gsm_data = get_gsm(gsm, path_tmp, is_remove=True)
    except GEOparse.GEOparse.NoEntriesException:
        continue
    chs_raw = gsm_data.metadata["characteristics_ch1"]
    chs_keys = set()
    for ch in chs_raw:
        ch_split = ch.split(': ')
        chs_keys.update([ch_split[0]])

    intersection = chs_keys.intersection(target_chs)

    if len(intersection) > 0:

        print(f'{gse} is passed!')

        path_all = f'{get_data_path()}/GPL{GPL}/all/{gse_id}_{gse}'
        path_passed = f'{get_data_path()}/GPL{GPL}/passed/{gse_id}_{gse}'
        make_dir(path_all)

        curr_gsms = gse_gsms_dict[gse]

        # Init characteristics dicts
        gsms_exist = []
        gsm_data_dict = {}
        chs_keys = set()
        for gsm_id, gsm in enumerate(curr_gsms):
            try:
                gsm_data = get_gsm(gsm, f'{path_all}/gsms')
                gsm_data_dict[gsm] = gsm_data
            except GEOparse.GEOparse.NoEntriesException:
                os.remove(f'{path_all}/gsms/{gsm}.txt')
                continue
            gsms_exist.append(gsm)
            chs_raw = gsm_data.metadata["characteristics_ch1"]
            for ch in chs_raw:
                ch_split = ch.split(': ')
                chs_keys.update([ch_split[0]])

        curr_gsms = gsms_exist
        gsms_passed = [True] * len(curr_gsms)

        chs = {}
        chs['geo_accession'] = []
        chs['title'] = []
        chs['source_name'] = []
        ch_unique_words.update(chs_keys)
        for key in chs_keys:
            chs[key] = []

        for gsm_id, gsm in enumerate(curr_gsms):

            gsm_data = gsm_data_dict[gsm]

            gsm_is_passed = True

            chs['geo_accession'].append(gsm_data.metadata['geo_accession'][0])
            chs['title'].append(gsm_data.metadata['title'][0])
            chs['source_name'].append(gsm_data.metadata['source_name_ch1'][0])

            sources = gsm_data.metadata["source_name_ch1"]
            for source in sources:
                if isinstance(source, str):
                    sources_words = set(only_words(split_words(source.lower())))
                    source_unique_words.update(sources_words)
                    if len(bad_words.intersection(sources_words)) > 0:
                        gsm_is_passed = False

            chs_raw = gsm_data.metadata["characteristics_ch1"]
            exist_chs = []
            for ch in chs_raw:
                ch_split = ch.split(': ')
                if ch_split[0] not in exist_chs:
                    exist_chs.append(ch_split[0])
                    ch_value = ': '.join(ch_split[1::])
                    chs[ch_split[0]].append(ch_value)
                    separate_words = set(only_words(split_words(ch_value.lower())))
                    ch_unique_words.update(separate_words)
                    if len(bad_words.intersection(separate_words)) > 0:
                       gsm_is_passed = False
            missed_chs = list(chs_keys.difference(exist_chs))
            for ch in missed_chs:
                chs[ch].append('NA')

            gsms_passed[gsm_id] = gsm_is_passed

        save_table_dict_xlsx(f'{path_all}/observables.xlsx', chs)

        chs_keys_set = set()
        for ch_key in chs_keys:
            separate_words = set(only_words(split_words(ch_key.lower())))
            chs_keys_set.update(separate_words)

        gse_gsms_passed_dict[gse] = gsms_passed
        if len(gsms_passed) == gsms_passed.count(False):
            gse_passed_dict[gse] = False
        else:
            all_here = True
            for target_ch in target_chs:
                curr_tar_chs = target_ch.split(' ')
                if len(chs_keys_set.intersection(set(curr_tar_chs))) == 0:
                    all_here = False
                    break
            if all_here:
                gse_passed_dict[gse] = True
            else:
                gse_passed_dict[gse] = False

        if gse_passed_dict[gse]:
            make_dir(path_passed)
            copy_tree(path_all, path_passed)


all_unique_words = list(source_unique_words.union(ch_unique_words))
with open(f'{get_data_path()}/GPL{GPL}/unique_words.txt', 'w') as f:
    for item in all_unique_words:
        f.write('%s\n' % item)
