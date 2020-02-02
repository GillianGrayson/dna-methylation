import GEOparse
from data.infrastructure.path import get_data_path
from data.infrastructure.load.table import load_table_dict_xlsx, load_table_dict_pkl
from data.infrastructure.save.table import save_table_dict_pkl
import os
from tqdm import tqdm


GPL = '13534'
gsm_key = 'gsm'
geo_key = 'series_id'

fn_xlsx = f'{get_data_path()}/GPL{GPL}/GPL{GPL}_gsm_table.xlsx'
fn_pkl = f'{get_data_path()}/GPL{GPL}/GPL{GPL}_gsm_table.pkl'
if os.path.isfile(fn_pkl):
    gsm_raw_dict = load_table_dict_pkl(fn_pkl)
else:
    gsm_raw_dict = load_table_dict_xlsx(fn_xlsx)
    save_table_dict_pkl(fn_pkl, gsm_raw_dict)

gsms = gsm_raw_dict[gsm_key]

# data_dict_passed
fn_pkl = f'{get_data_path()}/GPL{GPL}/GPL{GPL}_dict.pkl'
if os.path.isfile(fn_pkl):
    gsm_dict = load_table_dict_pkl(fn_pkl)
else:
    gsm_dict = {}
    for key in tqdm(gsm_raw_dict, desc='gsm_dict processing'):
        gsm_dict[key] = {}
        for index, gsm in enumerate(gsms):
            gsm_dict[key][gsm] = gsm_raw_dict[key][index]
    save_table_dict_pkl(fn_pkl, gsm_dict)


# geo_gsms_dict
fn_pkl = f'{get_data_path()}/GPL{GPL}/geo_gsms_dict.pkl'
if os.path.isfile(fn_pkl):
    geo_gsms_dict = load_table_dict_pkl(fn_pkl)
else:
    geos = set()
    for geo_raw in gsm_raw_dict[geo_key]:
        geos_curr = geo_raw.split(',')
        for geo in geos_curr:
            geos.add(geo)
    geos = list(geos)

    geo_gsms_dict = {}
    for geo in geos:
        geo_gsms_dict[geo] = []

    for gsm in gsms:
        geo_raw = gsm_dict[geo_key][gsm]
        geos_curr = geo_raw.split(',')
        for geo in geos_curr:
            geo_gsms_dict[geo].append(gsm)




    save_table_dict_pkl(fn_pkl, gsm_dict)



a = 0




gse = GEOparse.get_GEO(geo="GSM1343050", destdir="./")

a = 0