from enum import Enum


class Experiment(Enum):
    base = 'base'
    advanced = 'advanced'


class Task(Enum):
    table = 'table'
    clock = 'clock'
    inside_gene = 'inside_gene'
    inside_bop = 'inside_bop'


class Method(Enum):
    linreg = 'linreg'
    variance_linreg = 'variance_linreg'
    anova = 'anova'
    manova = 'manova'
    polygon = 'polygon'
    classification = 'classification'
    cluster = 'cluster'
