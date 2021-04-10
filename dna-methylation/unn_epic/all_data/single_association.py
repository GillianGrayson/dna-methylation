import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf


part = 'v2'
path = f'E:/YandexDisk/Work/pydnameth/unn_epic/all_data'

target_key = 'Group'
target_groups = ['Control', 'Disease']
features_type = 'immuno'
regression_features = ['DNAmAgeHannum', 'DNAmAge', 'DNAmPhenoAge', 'DNAmGrimAge', 'Age', 'PhenoAge', 'ImmunoAge', 'DNAmAgeHannumAA', 'DNAmAgeAA', 'DNAmPhenoAgeAA', 'DNAmGrimAgeAA', 'PhenoAgeAA', 'ImmunoAgeAA']

df_merged = pd.read_excel(f'{path}/table_part({part}).xlsx', converters={'ID': str}, engine='openpyxl')

with open(f'{path}/{features_type}.txt') as f:
    target_features = f.read().splitlines()

res_dict = {'metric': target_features}
res_dict['kw_p_value'] = []
res_dict['mw_p_value'] = []
res_dict['pb_p_value'] = []
for a in regression_features:
    #res_dict[f'{a}_R2_C'] = []
    #res_dict[f'{a}_p_value_C'] = []
    res_dict[f'{a}_pearson_r_C'] = []
    res_dict[f'{a}_pearson_p_value_C'] = []
    #res_dict[f'{a}_spearman_r_C'] = []
    #res_dict[f'{a}_spearman_p_value_C'] = []

    #res_dict[f'{a}_R2_T'] = []
    #res_dict[f'{a}_p_value_T'] = []
    res_dict[f'{a}_pearson_r_T'] = []
    res_dict[f'{a}_pearson_p_value_T'] = []
    #res_dict[f'{a}_spearman_r_T'] = []
    #res_dict[f'{a}_spearman_p_value_T'] = []


for m_id, m in enumerate(target_features):
    test_data = {}
    pb_x = {}
    for g_id, g in enumerate(target_groups):
        test_data[g] = df_merged.loc[df_merged[target_key] == g][m].to_list()
        pb_x[g] = [g_id] * len(test_data[g])

    _, kw_p_value = stats.kruskal(test_data[target_groups[0]],
                                  test_data[target_groups[1]])
    res_dict['kw_p_value'].append(kw_p_value)
    _, mw_p_value = stats.mannwhitneyu(test_data[target_groups[0]],
                                  test_data[target_groups[1]], alternative='two-sided')
    res_dict['mw_p_value'].append(mw_p_value)
    _, pb_p_value = stats.pointbiserialr(pb_x[target_groups[0]] + pb_x[target_groups[1]],
                                         test_data[target_groups[0]] + test_data[target_groups[1]])
    res_dict['pb_p_value'].append(pb_p_value)

    df_control = df_merged.loc[df_merged[target_key] == 'Control']
    for a in regression_features:
        formula = f'{m} ~ {a}'
        reg_res = smf.ols(formula=formula, data=df_control).fit()
        pvalues = dict(reg_res.pvalues)
        #res_dict[f'{a}_R2_C'].append(reg_res.rsquared)
        #res_dict[f'{a}_p_value_C'].append(pvalues[a])

        pearson_r, pearson_p_value = stats.pearsonr(df_control[m].to_list(), df_control[a].to_list())
        res_dict[f'{a}_pearson_r_C'].append(pearson_r)
        res_dict[f'{a}_pearson_p_value_C'].append(pearson_p_value)

        spearman_r, spearman_p_value = stats.spearmanr(df_control[m].to_list(), df_control[a].to_list())
        #res_dict[f'{a}_spearman_r_C'].append(spearman_r)
        #res_dict[f'{a}_spearman_p_value_C'].append(spearman_p_value)

    df_disease = df_merged.loc[df_merged[target_key] == 'Disease']
    for a in regression_features:
        formula = f'{m} ~ {a}'
        reg_res = smf.ols(formula=formula, data=df_disease).fit()
        pvalues = dict(reg_res.pvalues)
        #res_dict[f'{a}_R2_T'].append(reg_res.rsquared)
        #res_dict[f'{a}_p_value_T'].append(pvalues[a])

        pearson_r, pearson_p_value = stats.pearsonr(df_disease[m].to_list(), df_disease[a].to_list())
        res_dict[f'{a}_pearson_r_T'].append(pearson_r)
        res_dict[f'{a}_pearson_p_value_T'].append(pearson_p_value)

        spearman_r, spearman_p_value = stats.spearmanr(df_disease[m].to_list(), df_disease[a].to_list())
        #res_dict[f'{a}_spearman_r_T'].append(spearman_r)
        #res_dict[f'{a}_spearman_p_value_T'].append(spearman_p_value)

res_df = pd.DataFrame(res_dict)
fn_save = f"{path}/result/part({part})/{features_type}.xlsx"

res_df.to_excel(fn_save, index=False)