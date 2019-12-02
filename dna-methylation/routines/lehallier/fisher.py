import numpy as np
from scipy import stats as stats


def perform_fisher(x, n, m, N):
    contingency_table = [[x, m - x], [n - x, N - n - m + x]]
    print(contingency_table)
    a = np.sum(contingency_table, axis=0)
    b = np.sum(contingency_table, axis=1)
    if np.sum(a) == np.sum(b):
        print('contingency_table is ok')
    oddsratio, pvalue = stats.fisher_exact(contingency_table)
    print(f'oddsratio: {oddsratio}')
    print(f'pvalue: {pvalue}')