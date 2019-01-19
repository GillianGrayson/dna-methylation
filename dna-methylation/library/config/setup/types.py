from enum import Enum
from library.setup.advanced.clock.clock import ClockExogType


class Experiment(Enum):
    base = 'base'
    advanced = 'advanced'
    plot = 'plot'


class Task(Enum):
    table = 'table'
    clock = 'clock'
    attributes = 'attributes'
    betas = 'betas'


class Method(Enum):
    linreg = 'linreg'
    variance_linreg = 'variance_linreg'
    cluster = 'cluster'
    histogram = 'histogram'
    scatter = 'scatter'


def get_metrics_keys(setup):
    metrics = []

    if setup.task is Task.table:

        if setup.method is Method.linreg:
            metrics = [
                'item',
                'aux',
                'R2',
                'intercept',
                'slope',
                'intercept_std',
                'slope_std',
                'intercept_p_value',
                'slope_p_value'
            ]
        elif setup.method is Method.variance_linreg:
            metrics = [
                'item',
                'aux',
                'R2',
                'intercept',
                'slope',
                'intercept_std',
                'slope_std',
                'intercept_p_value',
                'slope_p_value',
                'R2_var',
                'intercept_var',
                'slope_var',
                'intercept_std_var',
                'slope_std_var',
                'intercept_p_value_var',
                'slope_p_value_var'
            ]
        elif setup.method is Method.cluster:
            metrics = [
                'item',
                'number_of_clusters',
                'number_of_noise_points',
            ]

    elif setup.task is Task.clock:

        if setup.method is Method.linreg:
            metrics = [
                'item',
                'aux',
                'count',
                'R2',
                'r',
                'evs',
                'mae',
                'summary'
            ]

    return metrics

def get_main_metric(setup):
    metric = ()

    if setup.task is Task.table:

        if setup.method is Method.linreg:
            metric = ('R2', 'descending')
        elif setup.method is Method.variance_linreg:
            metric = ('R2_var', 'descending')

    return metric


def get_default_params(setup):
    params = {}

    if setup.task is Task.table:

        if setup.method is Method.cluster:
            params = {
                'eps': 0.2,
                'min_samples': 5
            }

    elif setup.task is Task.clock:

        if setup.method is Method.linreg:
            params = {
                'type': ClockExogType.all.value,
                'part': 0.25,
                'exogs': 100,
                'combs': 100,
                'runs': 100,
            }

    return params
