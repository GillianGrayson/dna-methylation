import numpy as np
import pandas as pd

file_name = 'levine.xlsx'

main_df = pd.read_excel(file_name)

data_dict = {}
data_dict['Albumin'] = list(main_df.Albumin)
data_dict['Creatinine'] = list(main_df.Creatinine)
data_dict['Glucose_serum'] = list(main_df.Glucose_serum)
data_dict['C_reactive_protein_log'] = np.log(list(main_df.C_reactive_protein_log))
data_dict['Lymphocyte_percent'] = list(main_df.Lymphocyte_percent)
data_dict['Mean_red_cell_volume'] = list(main_df.Mean_red_cell_volume)
data_dict['Red_cell_distribution_width'] = list(main_df.Red_cell_distribution_width)
data_dict['Alkaline_phosphatase'] = list(main_df.Alkaline_phosphatase)
data_dict['White_blood_cell_count'] = list(main_df.White_blood_cell_count)
data_dict['Age'] = list(main_df.Age)

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
phenotypic_age = np.zeros(len(data_dict['Age']))

for sub_id in range(0, len(data_dict['Age'])):

    for key in coeff_dict:
        linear_combinations[sub_id] += coeff_dict[key] * data_dict[key][sub_id]
    linear_combinations[sub_id] += const

    mortality_score[sub_id] = 1 - np.exp(-np.exp(linear_combinations[sub_id]) * (np.exp(120 * gamma) - 1) / gamma)

    phenotypic_age[sub_id] = 141.50225 + np.log(-0.00553 * np.log(1 - mortality_score[sub_id])) / 0.090165


a = 1