from lib.model.strategy.load import *
from lib.model.strategy.get import *
from lib.model.strategy.setup import *
from lib.model.strategy.proc import *
from lib.model.strategy.release import *
from lib.model.strategy.save import *


class Context:

    def __init__(self,
                 config):

        if config.data.type == DataType.cpg:
            self.load_strategy = CPGLoadStrategy()

        if config.data.type == DataType.cpg:
            self.get_strategy = CPGGetStrategy()

        if config.setup.task == Task.table:
            self.setup_strategy = TableSetUpStrategy()
        elif config.setup.task == Task.clock:
            self.setup_strategy = ClockSetUpStrategy()

        if config.setup.task == Task.table:
            self.proc_strategy = TableProcStrategy(self.get_strategy)
        elif config.setup.task == Task.clock:
            self.proc_strategy = ClockProcStrategy(self.get_strategy)

        if config.setup.task == Task.table:
            self.release_strategy = TableReleaseStrategy()
        elif config.setup.task == Task.clock:
            self.release_strategy = ClockReleaseStrategy()

        if config.setup.task == Task.table:
            self.save_strategy = TableSaveStrategy()
        elif config.setup.task == Task.clock:
            self.save_strategy = ClockSaveStrategy()

    def base_pipeline(self, config):
        self.load_strategy.load_base(config)
        self.setup_strategy.setup_base(config)
        self.proc_strategy.proc_base(config)
        self.release_strategy.release(config)
        self.save_strategy.save(config)

    def advanced_pipeline(self, config, configs_primary):
        self.load_strategy.load_base(config)
        for config_primary in configs_primary:
            self.load_strategy.load_advanced(config_primary)
        self.setup_strategy.setup_advanced(config, configs_primary)
        self.proc_strategy.proc_base(config)
        self.release_strategy.release(config)
        self.save_strategy.save(config)

    def plot_pipeline(self, config, configs_primary):
        self.load_strategy.load_base(config)
        for config_primary in configs_primary:
            self.load_strategy.load_advanced(config_primary)
        self.setup_strategy.setup_advanced(config, configs_primary)
        self.proc_strategy.proc_base(config)
        self.release_strategy.release(config)
        self.save_strategy.save(config)

