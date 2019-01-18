import abc
from lib.config.setup.types import *
import numpy as np


class GetStrategy(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_single_base(self, config, ids):
        pass

    def get_target(self, config, normed=False):
        target = config.attributes_dict[config.target]
        if normed:
            target_normed = [(float(x) - min(target)) / (float(max(target)) - float(min(target))) for x in target]
            target = target_normed
        return target


class CPGGetStrategy(GetStrategy):

    def get_single_base(self, config, ids):

        if config.setup.task is Task.table:
            rows = [config.base_dict[id] for id in ids]
            return config.base_data[np.ix_(config.attributes_indexes), rows]
