from source.config.common import CommonTypes


class Cells:
    def __init__(self,
                 file_name,
                 types,
                 ):
        self.file_name = file_name
        self.types = types

    def __str__(self):
        name = 'cells('
        if isinstance(self.types, list):
            self.types.sort()
            name += '_'.join(self.types)
        elif isinstance(self.types, CommonTypes):
            name += self.types.value
        else:
            raise ValueError('Cells.types must be list or str')
        name += ')'
        return name


class Observables:
    def __init__(self,
                 file_name,
                 types,
                 ):
        self.file_name = file_name
        self.types = types

    def __str__(self):
        name = 'observables('
        if isinstance(self.types, dict):
            name +=  '_'.join([self.types[key] for key in self.types.keys()]) + ')'
        elif isinstance(self.types, CommonTypes):
            name += self.types.value
        else:
            raise ValueError('Observables.types must be list or str')
        name += ')'
        return name


class Attributes:
    def __init__(self,
                 observables,
                 cells,
                 ):
        self.observables = observables
        self.cells = cells

    def __str__(self):
        name = str(self.observables) + '_' + str(self.cells)
        return name
