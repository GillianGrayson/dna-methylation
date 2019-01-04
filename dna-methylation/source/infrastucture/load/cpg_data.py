from source.infrastucture.path import *
import numpy as np
import os.path
import pickle


def get_line_list(line):
    line_list = line.split('\t')
    for val_id in range(0, len(line_list)):
        line_list[val_id] = line_list[val_id].replace('"', '').rstrip()
    return line_list


def load_cpg_beta_dict(config):
    fn = get_data_base_path(config) + '/' + config.data.name
    fn_txt = fn + '.txt'
    fn_pkl = fn + '.pkl'

    if os.path.isfile(fn_pkl):

        f = open(fn_pkl, 'rb')
        cpg_beta_dict = pickle.load(f)
        f.close()

    else:

        cpg_beta_dict = {}

        f = open(fn_txt)
        header_line = f.readline()
        headers = header_line.split('\t')
        headers = [x.rstrip() for x in headers]
        subjects = headers[1:len(headers)]

        num_cpgs = 0
        for line in f:
            line_list = get_line_list(line)
            cpg = line_list[0]
            betas = list(map(float, line_list[1::]))
            cpg_beta_dict[cpg] = betas
            num_cpgs += 1
            if num_cpgs % 10000 == 0:
                print('num_cpgs: ' + str(num_cpgs))
        f.close()

        f = open(fn_pkl, 'wb')
        pickle.dump(cpg_beta_dict, f, pickle.HIGHEST_PROTOCOL)
        f.close()

    for cpg, betas in cpg_beta_dict.items():
        cpg_beta_dict[cpg] = list(np.array(betas)[config.attribute_indexes])

    return cpg_beta_dict


