from enum import Enum
import socket
import pandas as pd
import os.path

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

class DataPath(Enum):
    local_1 = 'D:/YandexDisk'
    local_2 = 'E:/YandexDisk'
    local_3 = 'C:/Users/User/YandexDisk'

def get_lehallier_data_path():
    host_name = socket.gethostname()

    if host_name == 'MSI':
        path = DataPath.local_1.value + '/Work'
    elif host_name == 'DESKTOP-K9VO2TI':
        path = DataPath.local_2.value + '/Work'
    elif host_name == 'DESKTOP-4BEQ7MS':
        path = DataPath.local_3.value
    else:
        raise ValueError("Unsupported host_name: " + host_name)

    path += '/pydnameth/articles/inflammatory_clock'

    return path

def get_sex_specific_data_path():
    host_name = socket.gethostname()

    if host_name == 'MSI':
        path = DataPath.local_1.value + '/Work'
    elif host_name == 'DESKTOP-K9VO2TI':
        path = DataPath.local_2.value + '/Work'
    elif host_name == 'DESKTOP-4BEQ7MS':
        path = DataPath.local_3.value
    else:
        raise ValueError("Unsupported host_name: " + host_name)

    path += '/pydnameth/draft/tables/sex_specific/betas/v6'

    return path

def load_table_dict_xlsx(fn):
    if os.path.isfile(fn):
        df = pd.read_excel(fn)
        tmp_dict = df.to_dict()
        table_dict = {}
        for key in tmp_dict:
            curr_dict = tmp_dict[key]
            table_dict[key] = list(curr_dict.values())
        return table_dict
    else:
        raise IOError(f'No such file: {fn}')