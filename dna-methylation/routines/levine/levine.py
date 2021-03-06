import numpy as np
import pandas as pd
import statsmodels.api as sm
import scipy.stats as ss
from scipy.stats import shapiro, normaltest
from statsmodels.stats.stattools import jarque_bera, omni_normtest, durbin_watson
import plotly.express as px
import plotly
import colorlover as cl
import plotly.graph_objs as go
import os.path


file_name = 'levine.xlsx'

main_df = pd.read_excel(file_name, dtype={'date': str})

data_dict = {}
data_dict['Albumin'] = list(main_df.Albumin)
data_dict['Creatinine'] = list(main_df.Creatinine)
data_dict['Glucose_serum'] = list(main_df.Glucose_serum)
data_dict['C_reactive_protein_log'] = np.log10(list(main_df.C_reactive_protein_log * 10))
data_dict['Lymphocyte_percent'] = list(main_df.Lymphocyte_percent)
data_dict['Mean_red_cell_volume'] = list(main_df.Mean_red_cell_volume)
data_dict['Red_cell_distribution_width'] = list(main_df.Red_cell_distribution_width)
data_dict['Alkaline_phosphatase'] = list(main_df.Alkaline_phosphatase)
data_dict['White_blood_cell_count'] = list(main_df.White_blood_cell_count)
data_dict['Age'] = list(main_df.Age)

data_dict['date'] = list(main_df.date)
data_dict['Name'] = list(main_df.Name)

coeff_dict = {}
coeff_dict['Albumin'] = -0.0336
coeff_dict['Creatinine'] = 0.0095
coeff_dict['Glucose_serum'] = 0.1953
coeff_dict['C_reactive_protein_log'] = 0.0954
coeff_dict['Lymphocyte_percent'] = -0.0120
coeff_dict['Mean_red_cell_volume'] = 0.0268
coeff_dict['Red_cell_distribution_width'] = 0.3306
coeff_dict['Alkaline_phosphatase'] = 0.0019
coeff_dict['White_blood_cell_count'] = 0.0554
coeff_dict['Age'] = 0.0804
const = -19.9067
gamma = 0.0077

linear_combinations = np.zeros(len(data_dict['Age']))
mortality_score = np.zeros(len(data_dict['Age']))
mortality_score_1_year = np.zeros(len(data_dict['Age']))
mortality_score_2_year = np.zeros(len(data_dict['Age']))
phenotypic_age = np.zeros(len(data_dict['Age']))

for sub_id in range(0, len(data_dict['Age'])):

    for key in coeff_dict:
        linear_combinations[sub_id] += coeff_dict[key] * data_dict[key][sub_id]
    linear_combinations[sub_id] += const

    mortality_score[sub_id] = 1 - np.exp(-np.exp(linear_combinations[sub_id]) * (np.exp(120 * gamma) - 1) / gamma)

    mortality_score_1_year[sub_id] = 1 - np.exp(-np.exp(linear_combinations[sub_id]) * (np.exp(12 * gamma) - 1) / gamma)
    mortality_score_2_year[sub_id] = 1 - np.exp(-np.exp(linear_combinations[sub_id]) * (np.exp(24 * gamma) - 1) / gamma)

    phenotypic_age[sub_id] = 141.50225 + np.log(-0.00553 * np.log(1 - mortality_score[sub_id])) / 0.090165

np.savetxt('mortality_score_log10_deci.txt', mortality_score, fmt='%.2f')
np.savetxt('phenotypic_age_log10_deci.txt', phenotypic_age, fmt='%.2f')
np.savetxt('mortality_score_1_year_log10_deci.txt', mortality_score_1_year, fmt='%.2f')
np.savetxt('mortality_score_2_year_log10_deci.txt', mortality_score_2_year, fmt='%.2f')

x = sm.add_constant(data_dict['Age'])

results = sm.OLS(phenotypic_age, x).fit()

residuals = results.resid

jb, jbpv, skew, kurtosis = jarque_bera(results.wresid)
omni, omnipv = omni_normtest(results.wresid)

res_mean = np.mean(residuals)
res_std = np.std(residuals)

_, normality_p_value_shapiro = shapiro(residuals)
_, normality_p_value_dagostino = normaltest(residuals)

metrics_dict = {}
metrics_dict['R2'] = results.rsquared
metrics_dict['R2_adj'] = results.rsquared_adj
metrics_dict['f_stat'] = results.fvalue
metrics_dict['prob(f_stat)'] = results.f_pvalue
metrics_dict['log_likelihood'] = results.llf
metrics_dict['AIC'] = results.aic
metrics_dict['BIC'] = results.bic
metrics_dict['omnibus'] = omni
metrics_dict['prob(omnibus)'] = omnipv
metrics_dict['skew'] = skew
metrics_dict['kurtosis'] = kurtosis
metrics_dict['durbin_watson'] = durbin_watson(results.wresid)
metrics_dict['jarque_bera'] = jb
metrics_dict['prob(jarque_bera)'] = jbpv
metrics_dict['cond_no'] = results.condition_number
metrics_dict['normality_p_value_shapiro'] = normality_p_value_shapiro
metrics_dict['normality_p_value_dagostino'] = normality_p_value_dagostino
metrics_dict['intercept'] = results.params[0]
metrics_dict['slope'] = results.params[1]
metrics_dict['intercept_std'] = results.bse[0]
metrics_dict['slope_std'] = results.bse[1]
metrics_dict['intercept_p_value'] = results.pvalues[0]
metrics_dict['slope_p_value'] = results.pvalues[1]

t_stat, p_val = ss.ttest_ind(phenotypic_age, data_dict['Age'], nan_policy='omit')
p_val_left_sided = ss.t.cdf(t_stat, len(phenotypic_age) + len(data_dict['Age']) - 2)
p_val_right_sided = ss.t.sf(t_stat, len(phenotypic_age) + len(data_dict['Age']) - 2)

age_acc = phenotypic_age - data_dict['Age']

xs = data_dict['date']
ys = age_acc
colors = []
for name in data_dict['Name']:
    if 'M' in name:
        colors.append('mother')
    elif 'S' in name:
        colors.append('sister')
    elif 'F' in name:
        colors.append('father')
    elif 'B' in name:
        colors.append('brother')
    else:
        colors.append('subject')

plot_dict = {'xs': xs, 'ys': ys, 'status': colors}
df = pd.DataFrame(plot_dict)

iris = px.data.iris()
scatter = px.scatter(df, x="xs", y="ys", color="status", labels={'xs':'date', 'ys':'age acceleration'})

layout = go.Layout(
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=0
    )
)

fig = go.Figure(data=scatter, layout=layout)

plotly.offline.plot(fig, filename='date.html', auto_open=False, show_link=True)
plotly.io.write_image(fig, 'date.png')
plotly.io.write_image(fig, 'date.pdf')
