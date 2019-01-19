from library.model.context import *

def base_experiment(config):
    context = Context(config)
    context.base_pipeline(config)

def advanced_experiment(config, configs_primary):
    context = Context(config)
    context.advanced_pipeline(config, configs_primary)