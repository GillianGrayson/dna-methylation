from routines.nuage.otu_counts import load_otu_counts
from routines.nuage.subjects import load_subject_info, T0_T1_subject_separation
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate

data_file_path = 'D:/Aaron/Bio/NU-Age/Data'

fn_subject_info = data_file_path + '/' + 'correct_subject_info.tsv'
subject_info_dict = load_subject_info(fn_subject_info)
T0_subject_dict, T1_subject_dict = T0_T1_subject_separation(subject_info_dict)
fn_otu_counts = data_file_path + '/' + 'OTUcounts.tsv'
otu_counts = load_otu_counts(fn_otu_counts)

subject_row_dict_T0 = otu_counts.subject_row_dict_T0
subject_row_dict_T1 = otu_counts.subject_row_dict_T1

otu_t0 = np.zeros((len(list(subject_row_dict_T0.keys())), len(list(otu_counts.otu_col_dict_T0.keys()))), dtype=np.float32)
otu_t1 = np.zeros((len(list(subject_row_dict_T1.keys())), len(list(otu_counts.otu_col_dict_T1.keys()))), dtype=np.float32)

common_otus = list(set(otu_counts.otu_col_dict_T0.keys()).intersection(set(otu_counts.otu_col_dict_T1.keys())))
common_otu_t0 = np.zeros((len(list(subject_row_dict_T0.keys())), len(common_otus)), dtype=np.float32)
common_otu_t1 = np.zeros((len(list(subject_row_dict_T1.keys())), len(common_otus)), dtype=np.float32)

otu_t0_id = 0
otu_t1_id = 0
otu_t0_col_dict = {}
otu_t1_col_dict = {}
for key in otu_counts.otu_col_dict_T0:
    otu_t0_col_dict[key] = otu_t0_id
    otu_t0[:, otu_t0_id] = otu_counts.normalized_T0[:, otu_counts.otu_col_dict_T0[key]]
    otu_t0_id += 1
for key in otu_counts.otu_col_dict_T1:
    otu_t1_col_dict[key] = otu_t1_id
    otu_t1[:, otu_t1_id] = otu_counts.normalized_T1[:, otu_counts.otu_col_dict_T1[key]]
    otu_t1_id += 1

otu_id = 0
otu_col_dict_common = {}
for key in otu_counts.otu_col_dict_T0:
    if key in otu_counts.otu_col_dict_T1:
        otu_col_dict_common[key] = otu_id
        common_otu_t0[:, otu_id] = otu_counts.normalized_T0[:, otu_counts.otu_col_dict_T0[key]]
        common_otu_t1[:, otu_id] = otu_counts.normalized_T1[:, otu_counts.otu_col_dict_T1[key]]
        otu_id += 1

subjects_t0 = []
controls_t0 = []
for person in list(subject_row_dict_T0.keys()):
    person_id = subject_info_dict['CODE'].index(person)
    if subject_info_dict['status'][person_id] == 'Subject':
        subjects_t0.append(person)
    if subject_info_dict['status'][person_id] == 'Control':
        controls_t0.append(person)
print('Number of Subjects at T0: ' + str(len(subjects_t0)))
print('Number of Controls at T0: ' + str(len(controls_t0)))

subjects_t1 = []
controls_t1 = []
for person in list(subject_row_dict_T1.keys()):
    person_id = subject_info_dict['CODE'].index(person)
    if subject_info_dict['status'][person_id] == 'Subject':
        subjects_t1.append(person)
    if subject_info_dict['status'][person_id] == 'Control':
        controls_t1.append(person)
print('Number of Subjects at T1: ' + str(len(subjects_t1)))
print('Number of Controls at T1: ' + str(len(controls_t1)))

otu_t0_subject = np.zeros((len(subjects_t0), len(list(otu_counts.otu_col_dict_T0.keys()))), dtype=np.float32)
otu_t0_control = np.zeros((len(controls_t0), len(list(otu_counts.otu_col_dict_T0.keys()))), dtype=np.float32)
otu_t1_subject = np.zeros((len(subjects_t1), len(list(otu_counts.otu_col_dict_T1.keys()))), dtype=np.float32)
otu_t1_control = np.zeros((len(controls_t1), len(list(otu_counts.otu_col_dict_T1.keys()))), dtype=np.float32)

common_otu_t0_subject = np.zeros((len(subjects_t0), len(common_otus)), dtype=np.float32)
common_otu_t0_control = np.zeros((len(controls_t0), len(common_otus)), dtype=np.float32)
common_otu_t1_subject = np.zeros((len(subjects_t1), len(common_otus)), dtype=np.float32)
common_otu_t1_control = np.zeros((len(controls_t1), len(common_otus)), dtype=np.float32)

for sub_id, sub in enumerate(subjects_t0):
    curr_otu_t0 = otu_t0[subject_row_dict_T0[sub], :]
    curr_otu_t0_common = common_otu_t0[subject_row_dict_T0[sub], :]

    otu_t0_subject[sub_id, :] = curr_otu_t0
    common_otu_t0_subject[sub_id, :] = curr_otu_t0_common

for sub_id, sub in enumerate(controls_t0):
    curr_otu_t0 = otu_t0[subject_row_dict_T0[sub], :]
    curr_otu_t0_common = common_otu_t0[subject_row_dict_T0[sub], :]

    otu_t0_control[sub_id, :] = curr_otu_t0
    common_otu_t0_control[sub_id, :] = curr_otu_t0_common

for sub_id, sub in enumerate(subjects_t1):
    curr_otu_t1 = otu_t1[subject_row_dict_T1[sub], :]
    curr_otu_t1_common = common_otu_t1[subject_row_dict_T1[sub], :]

    otu_t1_subject[sub_id, :] = curr_otu_t1
    common_otu_t1_subject[sub_id, :] = curr_otu_t1_common

for sub_id, sub in enumerate(controls_t1):
    curr_otu_t1 = otu_t1[subject_row_dict_T1[sub], :]
    curr_otu_t1_common = common_otu_t1[subject_row_dict_T1[sub], :]

    otu_t1_control[sub_id, :] = curr_otu_t1
    common_otu_t1_control[sub_id, :] = curr_otu_t1_common

otu_t0_subject_df = pd.DataFrame(otu_t0_subject, subjects_t0, list(otu_t0_col_dict.keys()))
otu_t0_control_df = pd.DataFrame(otu_t0_control, controls_t0, list(otu_t0_col_dict.keys()))
otu_t1_subject_df = pd.DataFrame(otu_t1_subject, subjects_t1, list(otu_t1_col_dict.keys()))
otu_t1_control_df = pd.DataFrame(otu_t1_control, controls_t1, list(otu_t1_col_dict.keys()))

common_otu_t0_subject_df = pd.DataFrame(common_otu_t0_subject, subjects_t0, list(otu_col_dict_common.keys()))
common_otu_t0_control_df = pd.DataFrame(common_otu_t0_control, controls_t0, list(otu_col_dict_common.keys()))
common_otu_t1_subject_df = pd.DataFrame(common_otu_t1_subject, subjects_t1, list(otu_col_dict_common.keys()))
common_otu_t1_control_df = pd.DataFrame(common_otu_t1_control, controls_t1, list(otu_col_dict_common.keys()))

subj_control_t1_df = otu_t1_subject_df.append(otu_t1_control_df)
classes_subj_control_t1 = ['Subject',] * len(subjects_t1) + ['Control',] * len(controls_t1)
factor = pd.factorize(classes_subj_control_t1)
y = factor[0]
clf_subj_control_t1 = RandomForestClassifier(n_estimators=500)
output_subj_control_t1 = cross_validate(clf_subj_control_t1, subj_control_t1_df, y, cv=5, scoring='accuracy', return_estimator=True)
accuracy = np.mean(output_subj_control_t1['test_score'])
print('Accuracy Subject T1 vs Control T1: ' + str(accuracy))

subj_control_t0_df = otu_t0_subject_df.append(otu_t0_control_df)
classes_subj_control_t0 = ['Subject',] * len(subjects_t0) + ['Control',] * len(controls_t0)
factor = pd.factorize(classes_subj_control_t0)
y = factor[0]
clf_subj_control_t0 = RandomForestClassifier(n_estimators=500)
output_subj_control_t0 = cross_validate(clf_subj_control_t0, subj_control_t0_df, y, cv=5, scoring='accuracy', return_estimator=True)
accuracy = np.mean(output_subj_control_t0['test_score'])
print('Accuracy Subject T0 vs Control T0: ' + str(accuracy))

subj_t0_t1_df = common_otu_t0_subject_df.append(common_otu_t1_subject_df)
classes_subj_t0_t1 = ['T0',] * len(subjects_t0) + ['T1',] * len(subjects_t1)
factor = pd.factorize(classes_subj_t0_t1)
y = factor[0]
clf_subj_t0_t1 = RandomForestClassifier(n_estimators=500)
output_subj_t0_t1 = cross_validate(clf_subj_t0_t1, subj_t0_t1_df, y, cv=5, scoring='accuracy', return_estimator=True)
accuracy = np.mean(output_subj_t0_t1['test_score'])
print('Accuracy Subject T0 vs Subject T1: ' + str(accuracy))

control_t0_t1_df = common_otu_t0_control_df.append(common_otu_t1_control_df)
classes_control_t0_t1 = ['T0',] * len(controls_t0) + ['T1',] * len(controls_t1)
factor = pd.factorize(classes_control_t0_t1)
y = factor[0]
clf_control_t0_t1 = RandomForestClassifier(n_estimators=500)
output_control_t0_t1 = cross_validate(clf_control_t0_t1, control_t0_t1_df, y, cv=5, scoring='accuracy', return_estimator=True)
accuracy = np.mean(output_control_t0_t1['test_score'])
print('Accuracy Control T0 vs Control T1: ' + str(accuracy))
