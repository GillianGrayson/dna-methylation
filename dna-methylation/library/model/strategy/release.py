import abc
import numpy as np
from library.config.setup.types import *

class ReleaseStrategy(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def release(self, config):
        pass


class TableReleaseStrategy(ReleaseStrategy):

    def release(self, config):
        (key, direction) = get_main_metric(config.setup)

        order = list(np.argsort(config.metrics[key]))
        if direction == 'descending':
            order.reverse()

        for key, value in config.metrics.items():
            config.metrics[key] = list(np.array(value)[order])


class ClockReleaseStrategy(ReleaseStrategy):

    def release(self, config):
        pass