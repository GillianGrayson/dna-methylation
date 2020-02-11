import os.path
import pickle
import pandas as pd


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


def load_table_dict_pkl(fn):
    if os.path.isfile(fn):
        f = open(fn, 'rb')
        table_dict = pickle.load(f)
        f.close()
        return table_dict
    else:
        raise IOError(f'No such file: {fn}')
