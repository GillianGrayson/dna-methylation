import pandas as pd
import statsmodels.formula.api as smf

y_name = 'Age'
ages = ['DNAmAgeHannum', 'DNAmAge', 'DNAmPhenoAge', 'DNAmGrimAge', 'PhenoAge', 'ImmunoAge']
part = 'v2'
target_part = 'Control'

path = f'E:/YandexDisk/Work/pydnameth/unn_epic/all_data'
df_merged = pd.read_excel(f'{path}/table_part({part}).xlsx', converters={'ID': str}, engine='openpyxl')
C_df = df_merged.loc[df_merged['Group'] == 'Control']
T_df = df_merged.loc[df_merged['Group'] == 'Disease']

for a in ages:
    formula = f"{a} ~ {y_name}"
    model = smf.ols(formula=formula, data=C_df).fit()
    y_pred = model.predict(df_merged)
    df_merged[f"{a}AA"] = df_merged[a] - y_pred

df_merged.to_excel(f'{path}/current_table.xlsx', index=False)

