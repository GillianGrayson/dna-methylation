import abc
from library.config.setup.types import *
from library.config.data.types import *
import statsmodels.api as sm
import numpy as np
from sklearn.cluster import DBSCAN
from library.setup.advanced.clock.clock import ClockExogType, Clock
from library.setup.advanced.clock.linreg.processing import build_clock_linreg


class ProcStrategy(metaclass=abc.ABCMeta):

    def __init__(self, get_strategy):
        self.get_strategy = get_strategy

    @abc.abstractmethod
    def single_base(self, config, id):
        pass

    @abc.abstractmethod
    def iterate_base(self, config):
        pass

    @abc.abstractmethod
    def proc_base(self, config):
        pass

    @abc.abstractmethod
    def proc_advanced(self, config, configs_primary):
        pass


class TableProcStrategy(ProcStrategy):

    def single_base(self, config, item):

        if config.setup.method is Method.linreg:

            target = self.get_strategy.get_target(config)
            x = sm.add_constant(target)
            y = self.get_strategy.get_single_base(config, [item])[0]

            results = sm.OLS(y, x).fit()

            config.metrics['item'].append(item)
            config.metrics['aux'].append(';'.join(config.cpg_gene_dict[item]))
            config.metrics['R2'].append(results.rsquared)
            config.metrics['intercept'].append(results.params[0])
            config.metrics['slope'].append(results.params[1])
            config.metrics['intercept_std'].append(results.bse[0])
            config.metrics['slope_std'].append(results.bse[1])
            config.metrics['intercept_p_value'].append(results.pvalues[0])
            config.metrics['slope_p_value'].append(results.pvalues[1])

        elif config.setup.method is Method.variance_linreg:

            target = self.get_strategy.get_target(config)
            x = sm.add_constant(target)
            y = self.get_strategy.get_single_base(config, [item])[0]

            results = sm.OLS(y, x).fit()

            config.metrics['item'].append(item)
            config.metrics['aux'].append(';'.join(config.cpg_gene_dict[item]))
            config.metrics['R2'].append(results.rsquared)
            config.metrics['intercept'].append(results.params[0])
            config.metrics['slope'].append(results.params[1])
            config.metrics['intercept_std'].append(results.bse[0])
            config.metrics['slope_std'].append(results.bse[1])
            config.metrics['intercept_p_value'].append(results.pvalues[0])
            config.metrics['slope_p_value'].append(results.pvalues[1])

            diffs = []
            for p_id in range(0, len(target)):
                curr_x = target[p_id]
                curr_y = y[p_id]
                pred_y = results.params[1] * curr_x + results.params[0]
                diffs.append(abs(pred_y - curr_y))

            results_var = sm.OLS(diffs, x).fit()

            config.metrics['R2_var'].append(results_var.rsquared)
            config.metrics['intercept_var'].append(results_var.params[0])
            config.metrics['slope_var'].append(results_var.params[1])
            config.metrics['intercept_std_var'].append(results_var.bse[0])
            config.metrics['slope_std_var'].append(results_var.bse[1])
            config.metrics['intercept_p_value_var'].append(results_var.pvalues[0])
            config.metrics['slope_p_value_var'].append(results_var.pvalues[1])

        elif config.setup.method is Method.cluster:

            x = self.get_strategy.get_target(config, True)
            y = self.get_strategy.get_single_base(config, [item])[0]

            X = np.array([x, y]).T
            db = DBSCAN(eps=config.setup.params['eps'], min_samples=config.setup.params['min_samples']).fit(X)
            core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
            core_samples_mask[db.core_sample_indices_] = True
            labels = db.labels_
            number_of_clusters = len(set(labels)) - (1 if -1 in labels else 0)
            number_of_noise_points = list(labels).count(-1)

            config.metrics['item'].append(item)
            config.metrics['number_of_clusters'].append(number_of_clusters)
            config.metrics['number_of_noise_points'].append(number_of_noise_points)

    def iterate_base(self, config):

        if config.data.type is DataType.cpg:

            for item in config.base_list:
                if item in config.base_dict:
                    self.single_base(config, item)

    def proc_base(self, config):

        if config.setup.task is Task.table:
            self.iterate_base(config)

    def proc_advanced(self, config, configs_primary):
        pass


class ClockProcStrategy(ProcStrategy):

    def single_base(self, config, id):
        pass

    def iterate_base(self, config):
        pass

    def proc_base(self, config):
        pass

    def proc_advanced(self, config, configs_primary):
        if config.setup.task is Task.table:
            self.iterate_base(config)

        elif config.setup.task is Task.clock:

            items = config.experiment_data['items']
            values = config.experiment_data['values']
            test_size = config.experiment_data['test_size']
            train_size = config.experiment_data['train_size']

            target = self.get_strategy.get_target(config)

            type = config.setup.params['type']
            exogs = min(config.setup.params['exogs'], train_size)
            combs = min(config.setup.params['combs'], train_size)
            runs = config.setup.params['runs']

            if type is ClockExogType.all.value:

                for exog_id in range(0, exogs):

                    config.metrics['item'].append(items[exog_id])
                    config.metrics['aux'].append(';'.join(config.cpg_gene_dict[items[exog_id]]))
                    config.metrics['count'].append(exog_id + 1)

                    clock = Clock(endog_data=target,
                                  endog_names=config.target,
                                  exog_data=values[0:exog_id + 1],
                                  exog_names=items[0:exog_id + 1],
                                  metrics_dict=config.metrics,
                                  train_size=train_size,
                                  test_size=test_size,
                                  exog_num=exog_id + 1,
                                  exog_num_comb=combs,
                                  num_bootstrap_runs=runs)

                    build_clock_linreg(clock)

            elif type is ClockExogType.deep.value:

                for exog_id in range(0, exogs):

                    config.metrics['cpg'].append(exog_id + 1)
                    config.metrics['gene'].append(exog_id + 1)
                    config.metrics['count'].append(exog_id + 1)

                    clock = Clock(endog_data=target,
                                  endog_names=config.target,
                                  exog_data=values[0:exogs + 1],
                                  exog_names=items[0:exogs + 1],
                                  metrics_dict=config.metrics,
                                  train_size=train_size,
                                  test_size=test_size,
                                  exog_num=exogs,
                                  exog_num_comb=exog_id + 1,
                                  num_bootstrap_runs=runs)

                    build_clock_linreg(clock)

            elif type is ClockExogType.single.value:

                config.metrics['cpg'].append(combs)
                config.metrics['gene'].append(combs)
                config.metrics['count'].append(combs)

                clock = Clock(endog_data=target,
                              endog_names=config.target,
                              exog_data=values[0:exogs],
                              exog_names=items[0:exogs],
                              metrics_dict=config.metrics,
                              train_size=train_size,
                              test_size=test_size,
                              exog_num=exogs,
                              exog_num_comb=combs,
                              num_bootstrap_runs=runs)

                build_clock_linreg(clock)

            elif type is ClockExogType.slide.value:

                for exog_id in range(0, exogs, combs):

                    config.metrics['cpg'].append(exog_id)
                    config.metrics['gene'].append(exog_id)
                    config.metrics['count'].append(combs)

                    clock = Clock(endog_data=target,
                                  endog_names=config.target,
                                  exog_data=items[exog_id: exog_id + combs],
                                  exog_names=values[exog_id: exog_id + combs],
                                  metrics_dict=config.metrics,
                                  train_size=train_size,
                                  test_size=test_size,
                                  exog_num=combs,
                                  exog_num_comb=combs,
                                  num_bootstrap_runs=runs)

                    build_clock_linreg(clock)
