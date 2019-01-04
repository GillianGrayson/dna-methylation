from source.config.setup.types import *


"""
All levels can use only predefined enums
"""


class Setup:

    def __init__(self,
                 experiment,
                 task,
                 method,
                 params,
                 suffix
                 ):
        self.experiment = experiment
        self.task = task
        self.method = method
        self.params = params
        self.suffix = suffix

    def __str__(self):
        path = self.experiment.value + '/' + self.task.value + '/' + self.method.value
        return path

    def get_file_name(self):
        fn = ''
        if bool(self.params):
            params_keys = list(self.params.keys())
            if len(params_keys) > 0:
                params_keys.sort()
                fn += '_'.join([key + '(' + str(self.params[key]) + ')' for key in params_keys])

        if self.suffix != '':
            fn += '_' + self.suffix

        if fn == '':
            fn = 'default'

        return fn

