from library.infrastucture.load.cpg import *
from library.infrastucture.save.table import *
import statsmodels.api as sm


def generate_table_linreg(config):
    attributes_dict = config.attributes_dict
    betas = load_cpg(config)
    cpg_row_dict = config.cpg_row_dict
    cpg_list = config.cpg_list

    target = attributes_dict[config.target]

    print('len(cpg_list): ' + str(len(cpg_list)))

    cpg_names_passed = []
    R2s = []
    intercepts = []
    slopes = []
    intercepts_std_errors = []
    slopes_std_errors = []
    intercepts_p_values = []
    slopes_p_values = []

    num_passed = 0

    for cpg in cpg_list:

        if cpg in cpg_row_dict:
            row_id = cpg_row_dict[cpg]

            if num_passed % 10000 == 0:
                print('cpg_id: ' + str(num_passed))

            curr_betas = betas[row_id]
            x = sm.add_constant(target)

            results = sm.OLS(curr_betas, x).fit()

            cpg_names_passed.append(cpg)
            R2s.append(results.rsquared)
            intercepts.append(results.params[0])
            slopes.append(results.params[1])
            intercepts_std_errors.append(results.bse[0])
            slopes_std_errors.append(results.bse[1])
            intercepts_p_values.append(results.pvalues[0])
            slopes_p_values.append(results.pvalues[1])

            num_passed += 1


    order = np.argsort(list(map(abs, R2s)))[::-1]
    cpgs_sorted = list(np.array(cpg_names_passed)[order])
    R2s_sorted = list(np.array(R2s)[order])
    intercepts_sorted = list(np.array(intercepts)[order])
    slopes_sorted = list(np.array(slopes)[order])
    intercepts_std_errors_sorted = list(np.array(intercepts_std_errors)[order])
    slopes_std_errors_sorted = list(np.array(slopes_std_errors)[order])
    intercepts_p_values_sorted = list(np.array(intercepts_p_values)[order])
    slopes_p_values_sorted = list(np.array(slopes_p_values)[order])

    table_dict = {
        'id': cpgs_sorted,
        'R2': R2s_sorted,
        'intercept': intercepts_sorted,
        'slope': slopes_sorted,
        'intercept_std': intercepts_std_errors_sorted,
        'slope_std': slopes_std_errors_sorted,
        'intercept_p_value': intercepts_p_values_sorted,
        'slope_p_value': slopes_p_values_sorted
    }

    save_table_dict(config, table_dict)
