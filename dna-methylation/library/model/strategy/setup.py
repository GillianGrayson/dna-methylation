import abc
from library.config.setup.types import *
import math


class SetupStrategy(metaclass=abc.ABCMeta):

    def __init__(self, get_strategy):
        self.get_strategy = get_strategy

    @abc.abstractmethod
    def setup_base(self, config):
        pass

    @abc.abstractmethod
    def setup_advanced(self, config, configs_primary):
        pass

    @abc.abstractmethod
    def setup_plot(self, config, configs_primary):
        pass


    def setup_params(self, config):
        if not bool(config.setup.params):
            config.setup.params = get_default_params(config.setup)

    def setup_metrics(self, config):
        config.metrics = {}
        for key in get_metrics_keys(config.setup):
            config.metrics[key] = []


class TableSetUpStrategy(SetupStrategy):

    def setup_base(self, config):
        self.setup_params(config)
        self.setup_metrics(config)
        config.experiment_data = config.base_data

    def setup_advanced(self, config, configs_primary):
        pass

    def setup_plot(self, config, configs_primary):
        pass


class ClockSetUpStrategy(SetupStrategy):

    def setup_base(self, config):
        pass

    def setup_advanced(self, config, configs_primary):
        self.setup_params(config)
        self.setup_metrics(config)

        max_size = len(config.attributes_dict[config.target])
        test_size = math.floor(max_size *config.setup.params['part'])
        train_size = max_size - test_size

        # In clock task only first base config matters
        table = configs_primary[0].advanced_data
        items = table['item'][0:max_size]
        values = self.get_strategy.get_single_base(config, items)

        config.experiment_data = {
            'items': items,
            'values': values,
            'test_size': test_size,
            'train_size': train_size
        }

    def setup_plot(self, config, configs_primary):
        pass


class MethylationSetUpStrategy(SetupStrategy):

    def setup_base(self, config):
        pass

    def setup_advanced(self, config, configs_primary):
        pass

    def setup_plot(self, config, configs_primary):
        self.setup_params(config)
        self.setup_metrics(config)
        config.experiment_data = config.base_data


class ObservablesSetUpStrategy(SetupStrategy):

    def setup_base(self, config):
        pass

    def setup_advanced(self, config, configs_primary):
        pass

    def setup_plot(self, config, configs_primary):
        self.setup_params(config)
        self.setup_metrics(config)
        config.experiment_data = []