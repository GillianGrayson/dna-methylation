from routines.nuage.otu_counts import load_otu_counts
from routines.nuage.subjects import load_subject_info, T0_T1_subject_separation
from skbio.stats.ordination._principal_coordinate_analysis import pcoa

cpg_file_path = 'D:/YandexDisk/Work/nuage'

fn_subject_info = cpg_file_path + '/' + 'correct_subject_info.tsv'
subject_info_dict = load_subject_info(fn_subject_info)
T0_subject_dict, T1_subject_dict = T0_T1_subject_separation(subject_info_dict)
fn_otu_counts = cpg_file_path + '/' + 'OTUcounts.tsv'
otu_counts = load_otu_counts(fn_otu_counts, len(T0_subject_dict['CODE']))





a = 0




