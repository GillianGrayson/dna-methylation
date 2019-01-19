import abc
from library.config.setup.types import *
from library.infrastucture.load.cpg import *
from library.infrastucture.load.table import *


class LoadStrategy(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def load_base(self, config):
        pass

    @abc.abstractmethod
    def load_advanced(self, config):
        pass

    @abc.abstractmethod
    def inherit_base(self, source_config, target_config):
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

    def inherit_base(self, config_source, config_target):
        config_target.base_list = config_source.base_list
        config_target.base_dict = config_source.base_dict
        config_target.base_data = config_source.base_data
