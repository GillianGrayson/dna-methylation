from library.config.data.data import *
from library.config.setup.setup import *
from library.config.annotations.annotations import *
from library.config.attributes.attributes import *
from library.config.config import *
from library.model.context import *

def base_experiment(config):
    config.initialize()
    context = Context(config)
    context.base_pipeline(config)

def advanced_experiment(config, configs_primary):
    config.initialize()
    for config_primary in configs_primary:
        config_primary.initialize()
    context = Context(config)
    context.advanced_pipeline(config, configs_primary)

def plot_experiment(config, configs_primary):
    config.initialize()
    for config_primary in configs_primary:
        config_primary.initialize()
    context = Context(config)
    context.plot_pipeline(config, configs_primary)