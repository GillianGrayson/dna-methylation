from source.config.attribute.types import *


class Attribute:

    def __init__(self,
                 obs,
                 name='attribute',
                 cells=Cells.any.value,
                 cells_name='cells',
                 ):
        self.name = name
        self.cells_name = cells_name
        self.cells = cells
        self.obs = obs

    def __str__(self):
        name = 'cells(' + self.cells + ')'
        for ob, value in self.obs.items():
            name += '_' + ob + '(' + value + ')'
        return name
