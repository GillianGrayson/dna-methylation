from source.infrastucture.path import *
import numpy as np
import os.path
import pickle


def get_line_list(line):
    line_list = line.split('\t')
    for val_id in range(0, len(line_list)):
        line_list[val_id] = line_list[val_id].replace('"', '').rstrip()
    return line_list


def load_betas(config):
    fn_cpg_row_dict = get_data_base_path(config) + '/' + 'cpg_row_dict.pkl'
    fn_beta = get_data_base_path(config) + '/' + config.data.name
    fn_beta_txt = fn_beta + '.txt'
    fn_beta_npz = fn_beta + '.npz'

    if os.path.isfile(fn_cpg_row_dict) and os.path.isfile(fn_beta_npz):

        f = open(fn_cpg_row_dict, 'rb')
        config.cpg_row_dict = pickle.load(f)
        f.close()

        data = np.load(fn_beta_npz)
        betas = data['betas']

    else:

        config.cpg_row_dict = {}

        f = open(fn_beta_txt)
        header_line = f.readline()
        cpg_id = 0
        for line in f:
            line_list = get_line_list(line)
            cpg = line_list[0]
            config.cpg_row_dict[cpg] = cpg_id
            cpg_id += 1
            if cpg_id % 10000 == 0:
                print('cpg_id: ' + str(cpg_id))
        f.close()

        f = open(fn_cpg_row_dict, 'wb')
        pickle.dump(config.cpg_row_dict, f, pickle.HIGHEST_PROTOCOL)
        f.close()

        num_cpgs = cpg_id

        f = open(fn_beta_txt)
        header_line = f.readline()
        headers = header_line.split('\t')
        headers = [x.rstrip() for x in headers]
        subjects = headers[1:len(headers)]

        betas = np.zeros((num_cpgs, len(subjects)))

        cpg_id = 0
        for line in f:
            line_list = get_line_list(line)
            curr_betas = list(map(float, line_list[1::]))
            betas[cpg_id] = curr_betas
            cpg_id += 1
            if cpg_id % 10000 == 0:
                print('cpg_id: ' + str(cpg_id))
        f.close()

        np.savez_compressed(fn_beta_npz, betas=betas)

    num_subjects = betas.shape[1]

    indexes_all = list(np.linspace(0, num_subjects - 1, num_subjects, dtype=int))
    indexes_target = config.attributes_indexes
    indexes_delete = list(set(indexes_all) - set(indexes_target))
    indexes_delete.sort()
    betas = np.delete(betas, indexes_delete, axis=1)

    return betas
