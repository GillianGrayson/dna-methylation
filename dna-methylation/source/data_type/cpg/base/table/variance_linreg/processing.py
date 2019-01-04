from source.infrastucture.load.cpg_data import *
from source.infrastucture.save.table import *
import statsmodels.api as sm


def generate_table_variance_linreg(config):
    attribute_dict = config.attribute_dict
    cpg_beta_dict = load_cpg_beta_dict(config)
    cpg_list = config.cpg_list

    target = attribute_dict[config.target]

    print('len(cpg_list): ' + str(len(cpg_list)))

    cpg_names_passed = []

    R2s = []
    intercepts = []
    slopes = []
    intercepts_std_errors = []
    slopes_std_errors = []
    intercepts_p_values = []
    slopes_p_values = []

    R2s_var = []
    intercepts_var = []
    slopes_var = []
    intercepts_std_errors_var = []
    slopes_std_errors_var = []
    intercepts_p_values_var = []
    slopes_p_values_var = []

    num_passed = 0

    for cpg in cpg_list:

        if cpg in cpg_beta_dict:

            if num_passed % 10000 == 0:
                print('cpg_id: ' + str(num_passed))

            betas = cpg_beta_dict[cpg]

            x = sm.add_constant(target)
            results = sm.OLS(betas, x).fit()

            cpg_names_passed.append(cpg)
            R2s.append(results.rsquared)
            intercepts.append(results.params[0])
            slopes.append(results.params[1])
            intercepts_std_errors.append(results.bse[0])
            slopes_std_errors.append(results.bse[1])
            intercepts_p_values.append(results.pvalues[0])
            slopes_p_values.append(results.pvalues[1])

            diffs = []
            for p_id in range(0, len(target)):
                curr_x = target[p_id]
                curr_y = betas[p_id]
                pred_y = results.params[1] * curr_x + results.params[0]
                diffs.append(abs(pred_y - curr_y))

            results_var = sm.OLS(diffs, x).fit()
            R2s_var.append(results_var.rsquared)
            intercepts_var.append(results_var.params[0])
            slopes_var.append(results_var.params[1])
            intercepts_std_errors_var.append(results_var.bse[0])
            slopes_std_errors_var.append(results_var.bse[1])
            intercepts_p_values_var.append(results_var.pvalues[0])
            slopes_p_values_var.append(results_var.pvalues[1])

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
    R2s_var_sorted = list(np.array(R2s_var)[order])
    intercepts_var_sorted = list(np.array(intercepts_var)[order])
    slopes_var_sorted = list(np.array(slopes_var)[order])
    intercepts_std_errors_var_sorted = list(np.array(intercepts_std_errors_var)[order])
    slopes_std_errors_var_sorted = list(np.array(slopes_std_errors_var)[order])
    intercepts_p_values_var_sorted = list(np.array(intercepts_p_values_var)[order])
    slopes_p_values_var_sorted = list(np.array(slopes_p_values_var)[order])

    table_dict = {
        'id': cpgs_sorted,
        'R2': R2s_sorted,
        'intercept': intercepts_sorted,
        'slope': slopes_sorted,
        'intercept_std': intercepts_std_errors_sorted,
        'slope_std': slopes_std_errors_sorted,
        'intercept_p_value': intercepts_p_values_sorted,
        'slope_p_value': slopes_p_values_sorted,
        'R2_var': R2s_var_sorted,
        'intercept_var': intercepts_var_sorted,
        'slope_var': slopes_var_sorted,
        'intercept_std_var': intercepts_std_errors_var_sorted,
        'slope_std_var': slopes_std_errors_var_sorted,
        'intercept_p_value_var': intercepts_p_values_var_sorted,
        'slope_p_value_var': slopes_p_values_var_sorted
    }

    save_table_dict(config, table_dict)
