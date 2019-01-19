import abc
from library.infrastucture.load.cpg import *
from library.infrastucture.save.table import *

class SaveStrategy(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def save(self, config):
        pass


class TableSaveStrategy(SaveStrategy):

    def save(self, config):
        save_table_dict(config, config.metrics)


class ClockSaveStrategy(SaveStrategy):

    def save(self, config):
        save_table_dict(config, config.metrics)