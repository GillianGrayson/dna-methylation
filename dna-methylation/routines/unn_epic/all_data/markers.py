import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf


part = 'wo_noIntensity_detP'
path = 'E:/YandexDisk/Work/pydnameth/unn_epic'

metrics_type = 'MULTIPLEX_20_11_2020_xtd'
target_key = 'Sample_Group'
target_groups = ['C', 'T']
age_names = ['Age', 'DNAmAge', 'DNAmAgeHannum', 'DNAmPhenoAge', 'DNAmGrimAge']

fn_obs = f'{path}/observables_part({part}).csv'
fn_horvath = f'{path}/horvath/data/betas_horvath_calculator_norm_fun_part_{part}.output.csv'
fn_metrics = f'{path}/markers/{metrics_type}.xlsx'

df_obs = pd.read_csv(fn_obs)
df_horvath = pd.read_csv(fn_horvath)
df_metrics = pd.read_excel(fn_metrics)

ids_obs = df_obs['ID'].to_list()
ids = df_metrics['ID'].to_list()

metrics = df_metrics.columns.values.tolist()[1::]

not_in_df_metrics = list(set(ids_obs) - set(ids))
print(f'not_in_df_metrics: {not_in_df_metrics}')

df_full = pd.merge(df_horvath, df_metrics, on='ID')

res_dict = {'metric': metrics}
res_dict['kw_p_value'] = []
res_dict['pb_p_value'] = []
for a in age_names:
    res_dict[f'{a}_R2'] = []
    res_dict[f'{a}_p_value'] = []

for m_id, m in enumerate(metrics):
    test_data = {}
    pb_x = {}
    for g_id, g in enumerate(target_groups):
        test_data[g] = df_full.loc[df_full[target_key] == g][m].to_list()
        pb_x[g] = [g_id] * len(test_data[g])

    _, kw_p_value = stats.kruskal(test_data[target_groups[0]],
                                  test_data[target_groups[1]])
    res_dict['kw_p_value'].append(kw_p_value)
    _, pb_p_value = stats.pointbiserialr(pb_x[target_groups[0]] + pb_x[target_groups[1]],
                                         test_data[target_groups[0]] + test_data[target_groups[1]])
    res_dict['pb_p_value'].append(pb_p_value)

    df_control = df_full.loc[df_full[target_key] == 'C']
    for a in age_names:
        formula = f'{m} ~ {a}'
        reg_res = smf.ols(formula=formula, data=df_control).fit()
        pvalues = dict(reg_res.pvalues)
        res_dict[f'{a}_R2'].append(reg_res.rsquared)
        res_dict[f'{a}_p_value'].append(pvalues[a])

res_df = pd.DataFrame(res_dict)
fn_save = f'{path}/markers/{metrics_type}_tests.xlsx'

res_df.to_excel(fn_save)