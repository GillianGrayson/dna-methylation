import numpy as np
from tqdm import tqdm


class OTUCounts:

    def __init__(self,
                 otu_col_dict,
                 subject_row_dict,
                 normalized_T0,
                 normalized_T1,
                 rarified_T0,
                 rarified_T1,
                 raw_T0,
                 raw_T1,
                 ):
        self.otu_col_dict = otu_col_dict
        self.subject_row_dict = subject_row_dict
        self.normalized_T0 = normalized_T0
        self.normalized_T1 = normalized_T1
        self.rarified_T0 = rarified_T0
        self.rarified_T1 = rarified_T1
        self.raw_T0 = raw_T0
        self.raw_T1 = raw_T1


def load_otu_counts(fn, num_subjects):
    f = open(fn)
    key_line = f.readline()
    keys = key_line.split('\t')
    keys[-1] = keys[-1].rstrip()

    otu_col_dict = {}
    for key_id in range(3, len(keys)):
        otu_col_dict[keys[key_id]] = key_id - 3

    num_otus = len(otu_col_dict)

    subj_id = 0
    time_id = 1
    type_id = 2

    normalized_T0 = np.zeros((num_subjects, num_otus), dtype=np.float32)
    normalized_T1 = np.zeros((num_subjects, num_otus), dtype=np.float32)
    rarified_T0 = np.zeros((num_subjects, num_otus), dtype=np.float32)
    rarified_T1 = np.zeros((num_subjects, num_otus), dtype=np.float32)
    raw_T0 = np.zeros((num_subjects, num_otus), dtype=np.float32)
    raw_T1 = np.zeros((num_subjects, num_otus), dtype=np.float32)

    subject_row_dict = {}
    curr_row_id = 0
    subjects = []
    times = []
    for line in tqdm(f, mininterval=60.0, desc='betas_data creating'):
        line_list = line.split('\t')
        line_list[-1] = line_list[-1].rstrip()

        subject = line_list[subj_id]

        time = line_list[time_id]
        times.append(time)
        type = line_list[type_id]
        subjects.append(subject)
        otus = line_list[3::]
        otus = np.float32(otus)
        if len(otus) != num_otus:
            raise ValueError('Wrong number of otus in row')

        if  type == 'NormalisedCount' and time == 'T0':
            normalized_T0[curr_row_id] = otus
        elif type == 'RarifiedCount' and time == 'T0':
            rarified_T0[curr_row_id] = otus
        elif type == 'RawCount' and time == 'T0':
            raw_T0[curr_row_id] = otus
        elif  type == 'NormalisedCount' and time == 'T1':
            normalized_T1[curr_row_id] = otus
        elif type == 'RarifiedCount' and time == 'T1':
            rarified_T1[curr_row_id] = otus
        elif type == 'RawCount' and time == 'T1':
            raw_T1[curr_row_id] = otus

        if type == 'RawCount' and time == 'T1':
            subject_row_dict[subject] = curr_row_id
            curr_row_id += 1

    f.close()

    subjects = list(set(subjects))
    print('Number of subjects with otus:' + str(len(subjects)))
    print('Number of subjects with otus and only T0:' + str(times.count('T0')/3))
    print('Number of subjects with otus and only T1:' + str(times.count('T1')/3))

    otu_counts = OTUCounts(
        otu_col_dict,
        subject_row_dict,
        normalized_T0,
        normalized_T1,
        rarified_T0,
        rarified_T1,
        raw_T0,
        raw_T1
    )

    return otu_counts