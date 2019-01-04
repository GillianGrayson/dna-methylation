from source.config.attribute.types import *
import numpy as np


def get_attribute_indexes(config, target, variable, common):
    passed_indexes = []
    attributes = config.attribute_dict[target]
    if variable == common:
        passed_indexes = list(range(0, len(attributes)))
    else:
        for index in range(0, len(attributes)):
            if variable == attributes[index]:
                passed_indexes.append(index)
    return passed_indexes


def get_indexes(config):
    indexes = list(range(0, len(list(config.attribute_dict.values())[0])))

    for obs, value in config.attribute.obs.items():
        common = 'any'
        if obs in config.attribute_dict:
            passed_indexes = get_attribute_indexes(config, obs, value, common)
            indexes = list(set(indexes).intersection(passed_indexes))

    indexes.sort()

    return indexes


def subset_attributes(config):
    for key in config.attribute_dict:
        values = config.attribute_dict[key]
        config.attribute_dict[key] = list(np.array(values)[config.attribute_indexes])


def subset_cells(config):
    for key in config.cells_dict:
        values = config.cells_dict[key]
        config.cells_dict[key] = list(np.array(values)[config.attribute_indexes])
