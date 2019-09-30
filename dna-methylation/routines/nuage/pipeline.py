from routines.nuage.otu_counts import load_otu_counts
from routines.nuage.subjects import load_subject_info, T0_T1_subject_separation
#from skbio.stats.ordination._principal_coordinate_analysis import pcoa
import numpy as np

cpg_file_path = 'D:/YandexDisk/Work/nuage'

fn_subject_info = cpg_file_path + '/' + 'correct_subject_info.tsv'
subject_info_dict = load_subject_info(fn_subject_info)
T0_subject_dict, T1_subject_dict = T0_T1_subject_separation(subject_info_dict)
fn_otu_counts = cpg_file_path + '/' + 'OTUcounts.tsv'
otu_counts = load_otu_counts(fn_otu_counts, len(T0_subject_dict['CODE']))

target_key = 'country'
target_vals = ['Italy', 'UK', 'Holland', 'Poland', 'France']

subject_row_dict = otu_counts.subject_row_dict

for val in target_vals:
    subj_ids = [i for i, x in enumerate(T0_subject_dict[target_key]) if x == val]
    CODEs = [T0_subject_dict['CODE'][x] for x in subj_ids]

    distance_mtx = np.zeros((len(CODEs), len(CODEs)), dtype=np.float32)

    for sub_id_1, sub_1 in enumerate(CODEs):
        otu_1 = otu_counts.normalized_T0[subject_row_dict[sub_1], :]

        for sub_id_2, sub_2 in enumerate(CODEs):
            otu_2 = otu_counts.normalized_T0[subject_row_dict[sub_2], :]

            a = 1







a = 0




