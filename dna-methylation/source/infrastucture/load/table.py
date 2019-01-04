from source.infrastucture.path import *
import pandas as pd


def load_table_dict(config):
    fn = get_table_path(config) + '/' + config.setup.get_file_name() + '.xlsx'
    df = pd.read_excel(fn)
    tmp_dict = df.to_dict()
    table_dict = {}
    for key in tmp_dict:
        curr_dict = tmp_dict[key]
        table_dict[key] = list(curr_dict.values())
    return table_dict