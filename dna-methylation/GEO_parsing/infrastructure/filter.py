import re
from functions.routines import is_float
import os
from functions.load.table import load_table_dict_xlsx, load_table_dict_pkl
from functions.save.table import save_table_dict_pkl, save_table_dict_xlsx
from tqdm import tqdm


def split_words(text):
    rgx = re.compile(r"((?:(?<!'|\w)(?:\w-?'?)+(?<!-))|(?:(?<='|\w)(?:\w-?'?)+(?=')))")
    return rgx.findall(text)


def only_words(words):
    passed_words = []
    for word in words:
        if not is_float(word):
            passed_words.append(word)
    return passed_words

def get_raw_dict(fn):
    fn_xlsx = f'{fn}.xlsx'
    fn_pkl = f'{fn}.pkl'
    if os.path.isfile(fn_pkl):
        gsm_raw_dict = load_table_dict_pkl(fn_pkl)
    else:
        gsm_raw_dict = load_table_dict_xlsx(fn_xlsx)
        save_table_dict_pkl(fn_pkl, gsm_raw_dict)
    return gsm_raw_dict

def get_gsm_dict(fn, gsm_raw_dict):
    gsms = gsm_raw_dict['gsm']
    fn_pkl = f'{fn}.pkl'
    if os.path.isfile(fn_pkl):
        gsm_dict = load_table_dict_pkl(fn_pkl)
    else:
        gsm_dict = {}
        for key in tqdm(gsm_raw_dict, desc='gsm_dict processing'):
            gsm_dict[key] = {}
            for index, gsm in enumerate(gsms):
                gsm_dict[key][gsm] = gsm_raw_dict[key][index]
        save_table_dict_pkl(fn_pkl, gsm_dict)
    return  gsm_dict

def get_gse_gsm_dict(fn, gsm_raw_dict, gsm_dict):
    gsms = gsm_raw_dict['gsm']
    # gse_gsms_dict
    fn_pkl = f'{fn}.pkl'
    if os.path.isfile(fn_pkl):
        gse_gsms_dict = load_table_dict_pkl(fn_pkl)
    else:
        gses = set()
        for gses_raw in gsm_raw_dict["series_id"]:
            gses_curr = gses_raw.split(',')
            for gse in gses_curr:
                gses.add(gse)
        gses = list(gses)
        gse_gsms_dict = {}
        for gse in gses:
            gse_gsms_dict[gse] = []

        for gsm in gsms:
            gses_raw = gsm_dict["series_id"][gsm]
            gses_curr = gses_raw.split(',')
            for gse in gses_curr:
                gse_gsms_dict[gse].append(gsm)

        save_table_dict_pkl(fn_pkl, gse_gsms_dict)

    return gse_gsms_dict