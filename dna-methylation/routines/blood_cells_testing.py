import pickle
import statsmodels.api as sm
import numpy as np
from scipy.stats import norm

data_path = 'C:/Users/User/YandexDisk/pydnameth/'
data_base = 'GSE40279'

cells_file_name = 'cells_horvath_calculator'
observables_file_name = 'observables'

f = open(data_path + data_base + '/' + cells_file_name + '.pkl', 'rb')
cells = pickle.load(f)
f.close()

f = open(data_path + data_base + '/' + observables_file_name + '.pkl', 'rb')
observables = pickle.load(f)
f.close()

keys = list(cells.keys())

cells_f = {}
cells_m = {}

for key in keys:
    cells_f[key] = []
    cells_m[key] = []

ages_f = []
ages_m = []

for i in range(0, len(observables['gender'])):
    if observables['gender'][i] is 'F':
        ages_f.append(observables['age'][i])
        for key in keys:
            cells_f[key].append(cells[key][i])
    elif observables['gender'][i] is 'M':
        ages_m.append(observables['age'][i])
        for key in keys:
            cells_m[key].append(cells[key][i])

metrics_f = {}
metrics_m = {}
metrics_common = {}

for key in keys:
    metrics_f[key] = {'slope': [],
                      'slope_std': [],
                      'r2': [],
                      'p_val': 0.0}
    metrics_m[key] = {'slope': [],
                      'slope_std': [],
                      'r2': [],
                      'p_val': 0.0}
    metrics_common[key] = {'p_value': 0.0,
                           'z_value': 0.0}

for cell_type in keys:
    targets_f = ages_f
    x_f = sm.add_constant(targets_f)
    y_f = cells_f[cell_type]

    results_f = sm.OLS(y_f, x_f).fit()

    targets_m = ages_m
    x_m = sm.add_constant(targets_m)
    y_m = cells_m[cell_type]

    results_m = sm.OLS(y_m, x_m).fit()

    r2_f = results_f.rsquared
    slope_f = results_f.params[1]
    slope_std_f = results_f.bse[1]
    p_val_f = results_f.f_pvalue

    metrics_f[cell_type]['slope'] = slope_f
    metrics_f[cell_type]['slope_std'] = slope_std_f
    metrics_f[cell_type]['r2'] = r2_f
    metrics_f[cell_type]['p_val'] = p_val_f

    r2_m = results_m.rsquared
    slope_m = results_m.params[1]
    slope_std_m = results_m.bse[1]
    p_val_m = results_m.f_pvalue

    metrics_m[cell_type]['slope'] = slope_m
    metrics_m[cell_type]['slope_std'] = slope_std_m
    metrics_m[cell_type]['r2'] = r2_m
    metrics_m[cell_type]['p_val'] = p_val_m

    std_errors = [slope_std_f / np.sqrt(len(ages_f)), slope_std_m / np.sqrt(len(ages_m))]
    z_value = (slope_f - slope_m) / np.sqrt(sum([std_error * std_error for std_error in std_errors]))
    p_value = norm.sf(abs(z_value)) * 2.0

    metrics_common[cell_type]['z_value'] = z_value
    metrics_common[cell_type]['p_value'] = p_value

for key in keys:
    print(key, '\n',
          'R2 F: ', metrics_f[key]['r2'], '\n',
          'R2 M: ', metrics_m[key]['r2'], '\n',
          'p-val F: ', metrics_f[key]['p_val'], '\n',
          'p-val M: ', metrics_m[key]['p_val'], '\n',
          'Z-test p-value: ', metrics_common[key]['p_value'])