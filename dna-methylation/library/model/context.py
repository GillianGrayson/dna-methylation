from library.model.strategy.load import *
from library.model.strategy.get import *
from library.model.strategy.setup import *
from library.model.strategy.proc import *
from library.model.strategy.release import *
from library.model.strategy.save import *


class Context:

    def __init__(self,
                 config):

        if config.data.type == DataType.cpg:
            self.load_strategy = CPGLoadStrategy()
        elif config.data.type == DataType.attributes:
            self.load_strategy = AttributesLoadStrategy()

        if config.data.type == DataType.cpg:
            self.get_strategy = CPGGetStrategy()
        elif config.data.type == DataType.attributes:
            self.get_strategy = AttributesGetStrategy()

        if config.setup.task == Task.table:
            self.setup_strategy = TableSetUpStrategy(self.get_strategy)
        elif config.setup.task == Task.clock:
            self.setup_strategy = ClockSetUpStrategy(self.get_strategy)
        elif config.setup.task == Task.methylation:
            self.setup_strategy = MethylationSetUpStrategy(self.get_strategy)
        elif config.setup.task == Task.observables:
            self.setup_strategy = ObservablesSetUpStrategy(self.get_strategy)

        if config.setup.task == Task.table:
            self.proc_strategy = TableProcStrategy(self.get_strategy)
        elif config.setup.task == Task.clock:
            self.proc_strategy = ClockProcStrategy(self.get_strategy)
        elif config.setup.task == Task.methylation:
            self.proc_strategy = MethylationProcStrategy(self.get_strategy)
        elif config.setup.task == Task.observables:
            self.proc_strategy = ObservablesProcStrategy(self.get_strategy)

        if config.setup.task == Task.table:
            self.release_strategy = TableReleaseStrategy()
        elif config.setup.task == Task.clock:
            self.release_strategy = ClockReleaseStrategy()
        elif config.setup.task == Task.methylation:
            self.release_strategy = MethylationReleaseStrategy()
        elif config.setup.task == Task.observables:
            self.release_strategy = ObservablesReleaseStrategy()

        if config.setup.task == Task.table:
            self.save_strategy = TableSaveStrategy()
        elif config.setup.task == Task.clock:
            self.save_strategy = ClockSaveStrategy()
        elif config.setup.task == Task.methylation:
            self.save_strategy = MethylationSaveStrategy()
        elif config.setup.task == Task.observables:
            self.save_strategy = ObservablesSaveStrategy()

    def base_pipeline(self, config):
        self.load_strategy.load_base(config)
        self.setup_strategy.setup_base(config)
        self.proc_strategy.proc_base(config)
        self.release_strategy.release_base(config)
        self.save_strategy.save_base(config)

    def advanced_pipeline(self, config, configs_primary):
        self.load_strategy.load_advanced(config, configs_primary)
        self.setup_strategy.setup_advanced(config, configs_primary)
        self.proc_strategy.proc_advanced(config, configs_primary)
        self.release_strategy.release_advanced(config, configs_primary)
        self.save_strategy.save_advanced(config, configs_primary)

    def plot_pipeline(self, config, configs_primary):
        self.load_strategy.load_plot(config, configs_primary)
        self.setup_strategy.setup_plot(config, configs_primary)
        self.proc_strategy.proc_plot(config, configs_primary)
        self.release_strategy.release_plot(config, configs_primary)
        self.save_strategy.save_plot(config, configs_primary)
