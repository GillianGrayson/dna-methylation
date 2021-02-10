import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf


part = 'wo_noIntensity_detP_subset'
path = f'E:/YandexDisk/Work/pydnameth/unn_epic/all_data'

target_key = 'Sample_Group'
target_groups = ['C', 'T']
regression_features = ['Age', 'DNAmAge', 'DNAmAgeHannum', 'DNAmPhenoAge', 'DNAmGrimAge']

df_merged = pd.read_excel(f'{path}/part({part}).xlsx', converters={'ID': str}, engine='openpyxl')

with open(f'{path}/features_list.txt') as f:
    target_features = f.read().splitlines()

res_dict = {'metric': target_features}
res_dict['kw_p_value'] = []
res_dict['pb_p_value'] = []
for a in regression_features:
    res_dict[f'{a}_R2_C'] = []
    res_dict[f'{a}_p_value_C'] = []
    res_dict[f'{a}_R2_T'] = []
    res_dict[f'{a}_p_value_T'] = []

for m_id, m in enumerate(target_features):
    test_data = {}
    pb_x = {}
    for g_id, g in enumerate(target_groups):
        test_data[g] = df_merged.loc[df_merged[target_key] == g][m].to_list()
        pb_x[g] = [g_id] * len(test_data[g])

    _, kw_p_value = stats.kruskal(test_data[target_groups[0]],
                                  test_data[target_groups[1]])
    res_dict['kw_p_value'].append(kw_p_value)
    _, pb_p_value = stats.pointbiserialr(pb_x[target_groups[0]] + pb_x[target_groups[1]],
                                         test_data[target_groups[0]] + test_data[target_groups[1]])
    res_dict['pb_p_value'].append(pb_p_value)

    df_control = df_merged.loc[df_merged[target_key] == 'C']
    for a in regression_features:
        formula = f'{m} ~ {a}'
        reg_res = smf.ols(formula=formula, data=df_control).fit()
        pvalues = dict(reg_res.pvalues)
        res_dict[f'{a}_R2_C'].append(reg_res.rsquared)
        res_dict[f'{a}_p_value_C'].append(pvalues[a])

    df_disease = df_merged.loc[df_merged[target_key] == 'T']
    for a in regression_features:
        formula = f'{m} ~ {a}'
        reg_res = smf.ols(formula=formula, data=df_disease).fit()
        pvalues = dict(reg_res.pvalues)
        res_dict[f'{a}_R2_T'].append(reg_res.rsquared)
        res_dict[f'{a}_p_value_T'].append(pvalues[a])

res_df = pd.DataFrame(res_dict)
fn_save = f"{path}/result/single_association.xlsx"

res_df.to_excel(fn_save, index=False)