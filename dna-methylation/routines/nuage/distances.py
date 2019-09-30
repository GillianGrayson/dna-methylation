import numpy as np


def spearman_dist(data_1, data_2):
    res = 0.0
    for i in range(len(data_1)):
        res += np.power((data_1[i] - data_2[i]), 2)
    return res