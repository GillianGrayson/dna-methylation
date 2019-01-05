from source.infrastucture.load.cpg_data import *
from source.infrastucture.load.table import *
from source.infrastucture.save.table import *
from itertools import combinations
from sklearn.model_selection import ShuffleSplit
from scipy import stats
from source.config.auxillary.clock import *
import sklearn.metrics as metrics
import statsmodels.api as sm
import math


def build_clock(clock):
    endog_data = clock.endog_data
    endog_name = clock.endog_names
    exog_data = clock.exog_data
    exog_names = clock.exog_names
    metrics_dict = clock.metrics_dict
    train_size = clock.train_size
    test_size = clock.test_size
    num_bootstrap_runs = clock.num_bootstrap_runs
    exog_num = clock.exog_num
    exog_num_comb = clock.exog_num_comb

    endog_dict = {endog_name: endog_data}
    endog_df = pd.DataFrame(endog_dict)

    if exog_num_comb > exog_num:
        exog_num_comb = exog_num

    exog_ids_all = combinations(list(range(0, exog_num)), exog_num_comb)

    R2_best = 0
    r_best = 0
    evs_best = 0
    mae_best = max(endog_data)

    num_comb = 0
    for exog_ids in exog_ids_all:
        num_comb += 1

        exog_dict = {}
        exog_arg_list = ['const']
        for exog_id in list(exog_ids):
            exog_dict[exog_names[exog_id]] = exog_data[exog_id]
            exog_arg_list += [exog_names[exog_id]]
        exog_df = pd.DataFrame(exog_dict)
        exog_df['const'] = 1

        reg_res = sm.OLS(endog=endog_df[endog_name], exog=exog_df[exog_arg_list]).fit()

        metrics_dict['summary'].append(reg_res.summary())

        rs = ShuffleSplit(num_bootstrap_runs, test_size, train_size)
        indexes = np.linspace(0, len(endog_data) - 1, len(endog_data), dtype=int).tolist()

        R2 = reg_res.rsquared
        r_test = 0.0
        evs_test = 0.0
        mae_test = 0.0

        bootstrap_id = 0
        for train_index, test_index in rs.split(indexes):

            endog_train_dict = {endog_name: list(np.array(endog_data)[train_index])}
            endog_train_df = pd.DataFrame(endog_train_dict)

            exog_train_dict = {}
            for exog_id in list(exog_ids):
                exog_train_dict[exog_names[exog_id]] = np.array(exog_data[exog_id]).T[train_index].T.tolist()
            exog_train_df = pd.DataFrame(exog_train_dict)
            exog_train_df['const'] = 1

            y_test = list(np.array(endog_data)[test_index])

            exog_test_dict = {}
            for exog_id in list(exog_ids):
                exog_test_dict[exog_names[exog_id]] = np.array(exog_data[exog_id]).T[test_index].T.tolist()
            exog_test_df = pd.DataFrame(exog_test_dict)
            exog_test_df['const'] = 1

            model = sm.OLS(endog=endog_train_df[endog_name], exog=exog_train_df[exog_arg_list]).fit()

            y_test_pred = model.get_prediction(exog=exog_test_df[exog_arg_list]).predicted_mean
            slope, intercept, r_value, p_value, std_err = stats.linregress(y_test_pred, y_test)
            r_test += r_value
            evs = metrics.explained_variance_score(y_test, list(y_test_pred))
            mae = metrics.mean_absolute_error(y_test, list(y_test_pred))
            evs_test += evs
            mae_test += mae

            bootstrap_id += 1

        r_test /= float(num_bootstrap_runs)
        evs_test /= float(num_bootstrap_runs)
        mae_test /= float(num_bootstrap_runs)

        if mae_test < mae_best:
            R2_best = R2
            r_best = r_test
            evs_best = evs_test
            mae_best = mae_test

        print('num_comb: ' + str(num_comb))

    metrics_dict['R2'].append(R2_best)
    metrics_dict['r_test'].append(r_best)
    metrics_dict['evs_test'].append(evs_best)
    metrics_dict['mae_test'].append(mae_best)


def generate_clock_linreg(config_from, config_to):
    attribute_dict = config_to.attribute_dict
    cpg_beta_dict = load_cpg_beta_dict(config_to)
    cpg_list = config_to.cpg_list
    cpg_gene_dict = config_to.cpg_gene_dict

    target = attribute_dict[config_to.target]

    test_size = math.floor(len(target) * 0.25)
    train_size = len(target) - test_size

    table = load_table_dict(config_from)
    cpg_names_tmp = table['id']

    cpg_names = []
    cpg_values = []
    for cpg in cpg_names_tmp:
        if cpg in cpg_list:
            cpg_names.append(cpg)
            cpg_values.append(cpg_beta_dict[cpg])
            if len(cpg_names) >= train_size:
                break

    if not bool(config_to.setup.params):
        config_to.setup.params = {
            'exog_type': ClockExogType.all.value,
            'exog_num': min(train_size, len(cpg_names)),
            'exog_num_comb': min(train_size, len(cpg_names))
        }

    exog_type = config_to.setup.params['exog_type']
    exog_num = min(config_to.setup.params['exog_num'], train_size, len(cpg_names))
    exog_num_comb = min(config_to.setup.params['exog_num_comb'], train_size, len(cpg_names))

    metrics_dict = {
        'cpg': [],
        'gene': [],
        'count': [],
        'R2': [],
        'r_test': [],
        'evs_test': [],
        'mae_test': [],
        'summary': []
    }

    if exog_type is ClockExogType.all.value:

        for exog_id in range(0, exog_num):
            print('exog_id: ' + str(exog_id))

            metrics_dict['cpg'].append(cpg_names[exog_id])
            metrics_dict['gene'].append(';'.join(cpg_gene_dict[cpg_names[exog_id]]))
            metrics_dict['count'].append(exog_id + 1)

            clock = Clock(endog_data=target,
                          endog_names=config_to.target,
                          exog_data=cpg_values[0:exog_id + 1],
                          exog_names=cpg_names[0:exog_id + 1],
                          metrics_dict=metrics_dict,
                          train_size=train_size,
                          test_size=test_size,
                          exog_num=exog_id + 1,
                          exog_num_comb=exog_num_comb)

            build_clock(clock)

    elif exog_type is ClockExogType.deep.value:

        for exog_id in range(0, exog_num):
            print('exog_id: ' + str(exog_id))

            metrics_dict['cpg'].append(exog_id + 1)
            metrics_dict['gene'].append(exog_id + 1)
            metrics_dict['count'].append(exog_id + 1)

            clock = Clock(endog_data=target,
                          endog_names=config_to.target,
                          exog_data=cpg_values[0:exog_num + 1],
                          exog_names=cpg_names[0:exog_num + 1],
                          metrics_dict=metrics_dict,
                          train_size=train_size,
                          test_size=test_size,
                          exog_num=exog_num,
                          exog_num_comb=exog_id + 1)

            build_clock(clock)

    elif exog_type is ClockExogType.single.value:
        print('exog_num: ' + str(exog_num))
        print('exog_num_comb: ' + str(exog_num_comb))

        metrics_dict['cpg'].append(exog_num_comb)
        metrics_dict['gene'].append(exog_num_comb)
        metrics_dict['count'].append(exog_num_comb)

        clock = Clock(endog_data=target,
                      endog_names=config_to.target,
                      exog_data=cpg_values[0:exog_num],
                      exog_names=cpg_names[0:exog_num],
                      metrics_dict=metrics_dict,
                      train_size=train_size,
                      test_size=test_size,
                      exog_num=exog_num,
                      exog_num_comb=exog_num_comb)

        build_clock(clock)

    elif exog_type is ClockExogType.slide.value:
        print('exog_num: ' + str(exog_num))
        print('exog_num_comb: ' + str(exog_num_comb))

        for exog_id in range(0, exog_num, exog_num_comb):
            print('exog_id: ' + str(exog_id))

            metrics_dict['cpg'].append(exog_id)
            metrics_dict['gene'].append(exog_id)
            metrics_dict['count'].append(exog_num_comb)

            clock = Clock(endog_data=target,
                          endog_names=config_to.target,
                          exog_data=cpg_values[exog_id: exog_id + exog_num_comb],
                          exog_names=cpg_names[exog_id: exog_id + exog_num_comb],
                          metrics_dict=metrics_dict,
                          train_size=train_size,
                          test_size=test_size,
                          exog_num=exog_num_comb,
                          exog_num_comb=exog_num_comb)

            build_clock(clock)

    save_table_dict(config_to, metrics_dict)
