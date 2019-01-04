from source.config.data.types import *
import socket
import os

"""
type can use only predefined enums
"""


class Data:

    def __init__(self,
                 name='cpg_beta',
                 type=DataType.cpg,
                 path='',
                 base=DataBase.GSE87571.value
                 ):
        self.name = name
        self.type = type
        self.path = path
        self.base = base

        if self.path == '' or os.path.isdir(self.path):
            host_name = socket.gethostname()
            if host_name == 'MSI':
                self.path = DataPath.local_1.value
            elif host_name == 'DESKTOP-K9VO2TI':
                self.data_path = DataPath.local_2.value
            elif host_name == 'DESKTOP-4BEQ7MS':
                self.path = DataPath.local_3.value
            elif host_name == 'master' or host_name[0:4] == 'node':
                self.path = DataPath.cluster.value

    def __str__(self):
        path = self.path + '/' + self.base + '/' + self.type.value
        return path

    def get_data_base_path(self):
        path = self.path + '/' + self.base
        return path