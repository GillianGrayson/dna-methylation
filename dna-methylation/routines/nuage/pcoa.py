from routines.nuage.otu_counts import load_otu_counts
from routines.nuage.subjects import load_subject_info, T0_T1_subject_separation
from routines.nuage.figures import plot_pcoa
from tqdm import tqdm
from skbio.stats.ordination._principal_coordinate_analysis import pcoa
from skbio.stats.distance._base import DistanceMatrix
import numpy as np
import pandas as pd

cpg_file_path = 'D:/YandexDisk/Work/nuage'

fn_subject_info = cpg_file_path + '/' + 'correct_subject_info.tsv'
subject_info_dict = load_subject_info(fn_subject_info)
T0_subject_dict, T1_subject_dict = T0_T1_subject_separation(subject_info_dict)
fn_otu_counts = cpg_file_path + '/' + 'OTUcounts.tsv'
otu_counts = load_otu_counts(fn_otu_counts)

subject_row_dict_T0 = otu_counts.subject_row_dict_T0
subject_row_dict_T1 = otu_counts.subject_row_dict_T1

country_key = 'country'
country_vals = ['Italy', 'UK', 'Holland', 'Poland', 'France']
country_dict = {}

status_key = 'status'
status_vals = ['Subject', 'Control']
status_dict = {}

common_subjects = list(set(subject_row_dict_T0.keys()).intersection(set(subject_row_dict_T1.keys())))
metadata = {}
for code in common_subjects:
    index = T0_subject_dict['CODE'].index(code)

    curr_country = T0_subject_dict[country_key][index]
    curr_status = T0_subject_dict[status_key][index]

    metadata[code] = {country_key: curr_country, status_key: curr_status}

    if curr_country in country_dict:
        country_dict[curr_country].append(code)
    else:
        country_dict[curr_country] = [code]

    if curr_status in status_dict:
        status_dict[curr_status].append(code)
    else:
        status_dict[curr_status] = [code]

metadata_df = pd.DataFrame.from_dict(metadata, orient='index')

distance_mtx = np.zeros((len(common_subjects), len(common_subjects)), dtype=np.float32)

for sub_id_1, sub_1 in tqdm(enumerate(common_subjects)):
    otu_1 = otu_counts.normalized_T0[subject_row_dict_T0[sub_1], :]

    for sub_id_2, sub_2 in enumerate(common_subjects):
        otu_2 = otu_counts.normalized_T0[subject_row_dict_T0[sub_2], :]

        curr_dist = np.power(np.linalg.norm(otu_1-otu_2), 2)
        distance_mtx[sub_id_1, sub_id_2] = curr_dist

check_mtx = np.allclose(distance_mtx, distance_mtx.T, rtol=1e-05, atol=1e-08)

skbio_distance_matrix = DistanceMatrix(distance_mtx, common_subjects)
ord_result = pcoa(skbio_distance_matrix)

plot_pcoa(ord_result, common_subjects, status_key, status_dict)
fig = ord_result.plot(df=metadata_df, column=status_key, title='PCoA', cmap='Set1', s=50)
fig.show()

plot_pcoa(ord_result, common_subjects, country_key, country_dict)
fig = ord_result.plot(df=metadata_df, column=country_key, title='PCoA', cmap='Set1', s=50)
fig.show()
