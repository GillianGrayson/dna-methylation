import abc
from lib.config.setup.types import *
from lib.infrastucture.load.cpg import *
from lib.infrastucture.load.table import *


class LoadStrategy(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def load_base(self, config):
        pass

    @abc.abstractmethod
    def load_advanced(self, config):
        pass



class CPGLoadStrategy(LoadStrategy):

    def load_base(self, config):
        load_cpg(config)
        config.base_list = config.cpg_list
        config.base_dict = config.cpg_dict
        config.base_data = config.cpg_data

    def load_advanced(self, config):
        if config.setup.task is Task.table:
            config.advanced_data = load_table_dict(config)

