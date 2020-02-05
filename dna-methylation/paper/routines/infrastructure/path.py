from enum import Enum
import socket


class DataPath(Enum):
    local_1 = 'D:/YandexDisk/Work/pydnameth'
    local_2 = 'E:/YandexDisk/Work/pydnameth'
    local_3 = 'C:/Users/User/YandexDisk/pydnameth'
    local_4 = 'E:/YandexDisk/pydnameth'


def get_data_path():
    host_name = socket.gethostname()

    if host_name == 'MSI':
        path = DataPath.local_1.value
    elif host_name == 'DESKTOP-K9VO2TI':
        path = DataPath.local_2.value
    elif host_name == 'DESKTOP-4BEQ7MS':
        path = DataPath.local_3.value
    elif host_name == 'DESKTOP-7H2CNDR':
        path = DataPath.local_4.value
    else:
        raise ValueError("Unsupported host_name: " + host_name)

    return path
