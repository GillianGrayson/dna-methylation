from source.infrastucture.load.cpg_data import *
from source.infrastucture.save.table import *
import statsmodels.api as sm


def generate_table_linreg(config):
    attribute_dict = config.attribute_dict
    cpg_beta_dict = load_cpg_beta_dict(config)
    cpg_list = config.cpg_list

    target = attribute_dict[config.target]

    print('len(cpg_list): ' + str(len(cpg_list)))

    if not bool(config.setup.params):
        config.setup.params = {
            'out_limit': 0.0,
            'out_sigma': 0.0
        }

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

        if cpg in cpg_beta_dict:

            if num_passed % 10000 == 0:
                print('cpg_id: ' + str(num_passed))

            betas = cpg_beta_dict[cpg]

            x = sm.add_constant(target)
            results = sm.OLS(betas, x).fit()

            if np.isclose(config.setup.params['out_limit'], 0.0):

                cpg_names_passed.append(cpg)
                R2s.append(results.rsquared)
                intercepts.append(results.params[0])
                slopes.append(results.params[1])
                intercepts_std_errors.append(results.bse[0])
                slopes_std_errors.append(results.bse[1])
                intercepts_p_values.append(results.pvalues[0])
                slopes_p_values.append(results.pvalues[1])

                num_passed += 1

            else:

                slope_plus = results.params[1] + config.setup.params['out_sigma'] * results.bse[1]
                intercept_plus = results.params[0] + config.setup.params['out_sigma'] * results.bse[0]

                slope = results.params[1]
                intercept = results.params[0]

                max_diff = ((slope_plus * max(target) + intercept_plus) - (slope * max(target) + intercept))

                passed_ids = []
                for p_id in range(0, len(target)):
                    curr_x = target[p_id]
                    curr_y = betas[p_id]
                    pred_y = results.params[1] * curr_x + results.params[0]
                    if abs(pred_y - curr_y) < max_diff:
                        passed_ids.append(p_id)

                if len(passed_ids) > np.floor(len(betas) * config.setup.params['out_limit']):

                    values_good = list(np.array(betas)[passed_ids])
                    attributes_good = list(np.array(target)[passed_ids])

                    x = sm.add_constant(attributes_good)
                    results = sm.OLS(values_good, x).fit()

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
