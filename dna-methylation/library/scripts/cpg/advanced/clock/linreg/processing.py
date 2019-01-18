from lib.infrastucture.load.table import *
from lib.infrastucture.save.table import *
from lib.infrastucture.load.cpg import *
import math
from lib.setup.advanced.clock.clock import ClockExogType, Clock
from lib.setup.advanced.clock.linreg.processing import build_clock_linreg


def generate_clock_linreg(config_from, config_to):
    attributes_dict = config_to.attributes_dict
    betas = load_cpg(config_to)
    cpg_row_dict = config_to.cpg_row_dict
    cpg_list = config_to.cpg_list
    cpg_gene_dict = config_to.cpg_gene_dict

    target = attributes_dict[config_to.target]

    test_size = math.floor(len(target) * 0.25)
    train_size = len(target) - test_size

    table = load_table_dict(config_from)
    cpg_names_tmp = table['id']

    cpg_names = []
    cpg_values = []
    for cpg in cpg_names_tmp:
        if cpg in cpg_list:
            if cpg in cpg_row_dict:
                row_id = cpg_row_dict[cpg]
                cpg_names.append(cpg)
                cpg_values.append(betas[row_id])
                if len(cpg_names) >= train_size:
                    break

    if not bool(config_to.setup.params):
        config_to.setup.params = {
            'type': ClockExogType.all.value,
            'exogs': min(train_size, len(cpg_names)),
            'combs': min(train_size, len(cpg_names)),
            'runs': 100
        }

    type = config_to.setup.params['type']
    exogs = min(config_to.setup.params['exogs'], train_size, len(cpg_names))
    combs = min(config_to.setup.params['combs'], train_size, len(cpg_names))
    runs = config_to.setup.params['runs']

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

    if type is ClockExogType.all.value:

        for exog_id in range(0, exogs):
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
                          exog_num_comb=combs,
                          num_bootstrap_runs=runs)

            build_clock_linreg(clock)

    elif type is ClockExogType.deep.value:

        for exog_id in range(0, exogs):
            print('exog_id: ' + str(exog_id))

            metrics_dict['cpg'].append(exog_id + 1)
            metrics_dict['gene'].append(exog_id + 1)
            metrics_dict['count'].append(exog_id + 1)

            clock = Clock(endog_data=target,
                          endog_names=config_to.target,
                          exog_data=cpg_values[0:exogs + 1],
                          exog_names=cpg_names[0:exogs + 1],
                          metrics_dict=metrics_dict,
                          train_size=train_size,
                          test_size=test_size,
                          exog_num=exogs,
                          exog_num_comb=exog_id + 1,
                          num_bootstrap_runs=runs)

            build_clock_linreg(clock)

    elif type is ClockExogType.single.value:
        print('exog_num: ' + str(exogs))
        print('combs: ' + str(combs))

        metrics_dict['cpg'].append(combs)
        metrics_dict['gene'].append(combs)
        metrics_dict['count'].append(combs)

        clock = Clock(endog_data=target,
                      endog_names=config_to.target,
                      exog_data=cpg_values[0:exogs],
                      exog_names=cpg_names[0:exogs],
                      metrics_dict=metrics_dict,
                      train_size=train_size,
                      test_size=test_size,
                      exog_num=exogs,
                      exog_num_comb=combs,
                          num_bootstrap_runs=runs)

        build_clock_linreg(clock)

    elif type is ClockExogType.slide.value:
        print('exog_num: ' + str(exogs))
        print('combs: ' + str(combs))

        for exog_id in range(0, exogs, combs):
            print('exog_id: ' + str(exog_id))

            metrics_dict['cpg'].append(exog_id)
            metrics_dict['gene'].append(exog_id)
            metrics_dict['count'].append(combs)

            clock = Clock(endog_data=target,
                          endog_names=config_to.target,
                          exog_data=cpg_values[exog_id: exog_id + combs],
                          exog_names=cpg_names[exog_id: exog_id + combs],
                          metrics_dict=metrics_dict,
                          train_size=train_size,
                          test_size=test_size,
                          exog_num=combs,
                          exog_num_comb=combs,
                          num_bootstrap_runs=runs)

            build_clock_linreg(clock)

    save_table_dict(config_to, metrics_dict)
