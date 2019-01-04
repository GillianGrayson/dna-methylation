import os.path
from source.config.data.types import *


def get_data_base_path(config):
    return config.data.get_data_base_path()


def get_cache_path(config):
    path = get_data_base_path(config) + '/' + \
           DataType.cache.value + '/' + \
           str(config.annotation)

    if not os.path.exists(path):
        os.makedirs(path)

    return path


def get_table_path(config):
    path = str(config.data) + '/' + \
           str(config.setup) + '/' + \
           str(config.annotation) + '/' + \
           str(config.attribute)

    if not os.path.exists(path):
        os.makedirs(path)

    return path
