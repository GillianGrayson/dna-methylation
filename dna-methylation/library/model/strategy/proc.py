import abc
from library.config.setup.types import *
from library.config.data.types import *
import statsmodels.api as sm
import numpy as np
from sklearn.cluster import DBSCAN
from library.setup.advanced.clock.clock import ClockExogType, Clock
from library.setup.advanced.clock.linreg.processing import build_clock_linreg
import plotly.graph_objs as go
import colorlover as cl


class ProcStrategy(metaclass=abc.ABCMeta):

    def __init__(self, get_strategy):
        self.get_strategy = get_strategy

    @abc.abstractmethod
    def single_base(self, config, item):
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
    
    @abc.abstractmethod
    def proc_plot(self, config, configs_primary):
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

    def proc_plot(self, config, configs_primary):
        pass


class ClockProcStrategy(ProcStrategy):

    def single_base(self, config, item):
        pass

    def iterate_base(self, config):
        pass

    def proc_base(self, config):
        pass

    def proc_advanced(self, config, configs_primary):

        if config.setup.method is Method.linreg:

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

    def proc_plot(self, config, configs_primary):
        pass


class MethylationProcStrategy(ProcStrategy):

    def single_base(self, config, item):

        plot_data = []

        target = self.get_strategy.get_target(config)
        methylation = self.get_strategy.get_single_base(config, [item])[0]

        scatter = go.Scatter(
            x=target,
            y=methylation,
            name='_'.join([key + '(' + value + ')' for key, value in config.attributes.observables.types.items()]),
            mode='markers',
            marker=dict(
                opacity=0.75,
                size=15,
                color=cl.scales['8']['qual']['Set1'][config.plot_data['color_id']],
                line=dict(width=2)
            ),
        )
        plot_data.append(scatter)

        if config.setup.method is Method.linreg:

            target = self.get_strategy.get_target(config)
            x = sm.add_constant(target)
            y = self.get_strategy.get_single_base(config, [item])[0]

            results = sm.OLS(y, x).fit()

            intercept = results.params[0]
            slope = results.params[1]
            intercept_std = results.bse[0]
            slope_std = results.bse[1]

            x_min = np.min(target)
            x_max = np.max(target)
            y_min = slope * x_min + intercept
            y_max = slope * x_max + intercept
            slope_tmp = slope + 3.0 * slope_std
            y_tmp = slope_tmp * x_max + intercept
            y_diff = 3.0 * np.abs(intercept_std) + np.abs(y_tmp - y_max)
            y_min_up = y_min + y_diff
            y_min_down = y_min - y_diff
            y_max_up = y_max + y_diff
            y_max_down = y_max - y_diff

            scatter = go.Scatter(
                x=[x_min, x_max],
                y=[y_min, y_max],
                mode='lines',
                marker=dict(
                    color=cl.scales['8']['qual']['Set1'][config.plot_data['color_id']],
                    line=dict(width=8)
                ),
                showlegend=False
            )
            plot_data.append(scatter)

            scatter = go.Scatter(
                x=[x_min, x_max, x_max, x_min, x_min],
                y=[y_min_down, y_max_down, y_max_up, y_min_up, y_min_down],
                fill='tozerox',
                mode='lines',
                marker=dict(
                    opacity=0.75,
                    color=cl.scales['8']['qual']['Set1'][config.plot_data['color_id']],
                    line=dict(width=8)
                ),
                showlegend=False
            )
            plot_data.append(scatter)

        elif config.setup.method is Method.variance_linreg:

            target = self.get_strategy.get_target(config)
            x = sm.add_constant(target)
            y = self.get_strategy.get_single_base(config, [item])[0]

            results = sm.OLS(y, x).fit()

            intercept = results.params[0]
            slope = results.params[1]

            diffs = []
            for p_id in range(0, len(target)):
                curr_x = target[p_id]
                curr_y = y[p_id]
                pred_y = slope * curr_x + intercept
                diffs.append(abs(pred_y - curr_y))

            results_var = sm.OLS(diffs, x).fit()

            intercept_var = results_var.params[0]
            slope_var = results_var.params[1]

            x_min = np.min(target)
            x_max = np.max(target)
            y_min = slope * x_min + intercept
            y_max = slope * x_max + intercept
            y_min_var = slope_var * x_min + intercept_var
            y_max_var = slope_var * x_max + intercept_var

            scatter = go.Scatter(
                x=[x_min, x_max],
                y=[y_min, y_max],
                mode='lines',
                marker=dict(
                    color=cl.scales['8']['qual']['Set1'][config.plot_data['color_id']],
                    line=dict(width=8)
                ),
                showlegend=False
            )
            plot_data.append(scatter)

            scatter = go.Scatter(
                x=[x_min, x_max, x_max, x_min, x_min],
                y=[y_min - y_min_var, y_max - y_max_var, y_max + y_max_var, y_min + y_min_var, y_min - y_min_var],
                fill='tozerox',
                mode='lines',
                marker=dict(
                    opacity=0.75,
                    color=cl.scales['8']['qual']['Set1'][config.plot_data['color_id']],
                    line=dict(width=4)
                ),
                showlegend=False
            )
            plot_data.append(scatter)


        elif config.setup.method is Method.cluster:

            pass

        return plot_data

    def iterate_base(self, config):
        pass

    def proc_base(self, config):
        pass

    def proc_advanced(self, config, configs_primary):
        pass

    def proc_plot(self, config, configs_primary):

        if config.setup.method is Method.scatter:

            item = config.setup.params['item']
            plot_data = []
            for config_primary in configs_primary:
                config_primary.plot_data = {
                    'color_id': configs_primary.index(config_primary)
                }
                curr_plot_data = self.single_base(config_primary, item)
                plot_data += curr_plot_data

            config.plot_data['data'] = plot_data
