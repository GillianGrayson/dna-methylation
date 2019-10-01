from routines.nuage.otu_counts import load_otu_counts
from routines.nuage.subjects import load_subject_info, T0_T1_subject_separation
from routines.nuage.distances import spearman_dist
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

country_key = 'country'
country_vals = ['Italy', 'UK', 'Holland', 'Poland', 'France']
country_dict = {}

status_key = 'status'
status_vals = ['Subject', 'Control']
status_dict = {}

subject_row_dict_T0 = otu_counts.subject_row_dict_T0
subject_row_dict_T1 = otu_counts.subject_row_dict_T1

subjects_T0 = list(subject_row_dict_T0.keys())
countries = []
statuses = []
for code in subjects_T0:
    index = T0_subject_dict['CODE'].index(code)

    curr_country = T0_subject_dict[country_key][index]
    curr_status = T0_subject_dict[status_key][index]

    countries.append(curr_country)
    statuses.append(curr_status)

    if curr_country in country_dict:
        country_dict[curr_country].append(code)
    else:
        country_dict[curr_country] = [code]

    if curr_status in status_dict:
        status_dict[curr_status].append(code)
    else:
        status_dict[curr_status] = [code]

for country_val in country_vals:
    print('Number of subjects in ' + country_val + ' is: ' + str(len(country_dict[country_val])))
for status_val in status_vals:
    print('Number of subjects in ' + status_val + ' is: ' + str(len(status_dict[status_val])))


common_subjects = list(set(subject_row_dict_T0.keys()).intersection(set(subject_row_dict_T1.keys())))
country_metadata = {}
status_metadata = {}
for code in common_subjects:
    index = T0_subject_dict['CODE'].index(code)

    curr_country = T0_subject_dict[country_key][index]
    curr_status = T0_subject_dict[status_key][index]

    country_metadata[code] = {country_key: curr_country}
    status_metadata[code] = {status_key: curr_status}

country_metadata_df = pd.DataFrame.from_dict(country_metadata, orient='index')
status_metadata_df = pd.DataFrame.from_dict(status_metadata, orient='index')

distance_mtx = np.zeros((len(common_subjects), len(common_subjects)), dtype=np.float32)

for sub_id_1, sub_1 in tqdm(enumerate(common_subjects)):
    otu_1 = otu_counts.normalized_T0[subject_row_dict_T0[sub_1], :]

    for sub_id_2, sub_2 in enumerate(common_subjects):
        otu_2 = otu_counts.normalized_T0[subject_row_dict_T0[sub_2], :]

        curr_dist = spearman_dist(otu_1, otu_2)
        distance_mtx[sub_id_1, sub_id_2] = curr_dist

skbio_distance_matrix = DistanceMatrix(distance_mtx, common_subjects)
ord_result = pcoa(skbio_distance_matrix)
fig = ord_result.plot(df=status_metadata_df, column=status_key, title='PCoA', cmap='Set1', s=50)
fig.show()


# for country_val in country_vals[:1]:
#
#     target_codes = country_dict[country_val]
#     num_subjects = len(target_codes)
#
#     distance_mtx = np.zeros((num_subjects, num_subjects), dtype=np.float32)
#
#     for sub_id_1, sub_1 in tqdm(enumerate(target_codes)):
#         otu_1 = otu_counts.normalized_T0[subject_row_dict_T0[sub_1], :]
#
#         for sub_id_2, sub_2 in enumerate(target_codes):
#             otu_2 = otu_counts.normalized_T0[subject_row_dict_T0[sub_2], :]
#
#             curr_dist = spearman_dist(otu_1, otu_2)
#             distance_mtx[sub_id_1, sub_id_2] = curr_dist
#
#     skbio_distance_matrix = DistanceMatrix(distance_mtx)
#     ord_result = pcoa(skbio_distance_matrix)
#     ord_result
#     fig = ord_result.plot()
#     fig.show()
#
#     a = 0




