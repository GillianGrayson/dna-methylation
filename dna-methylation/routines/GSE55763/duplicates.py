from tqdm import tqdm
import numpy as np
import pandas as pd
import csv


def save_table_dict_csv(fn, table_dict):
    fn_csv = fn + '.csv'
    with open(fn_csv, 'w') as csvfile:
        writer = csv.DictWriter(csvfile,
                                fieldnames=table_dict.keys(),
                                lineterminator='\n')
        writer.writeheader()
        for id in range(0, len(list(table_dict.values())[0])):
            tmp_dict = {}
            for key, values in table_dict.items():
                tmp_dict[key] = values[id]
            writer.writerow(tmp_dict)

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def get_line_list(line):
    line_list = line.split('\t')
    for val_id in range(0, len(line_list)):
        line_list[val_id] = line_list[val_id].replace('"', '').rstrip()
    return line_list


fn_path = 'E:/YandexDisk/Work/pydnameth/GSE55763/'
fn_txt = fn_path + 'observables.txt'

f = open(fn_txt)
key_line = f.readline()
keys = key_line.split('\t')
keys = [x.rstrip() for x in keys]
keys.append('is_duplicate')

attributes_dict = {}
for key in keys:
    attributes_dict[key] = []

for line in f:
    values = line.split('\t')
    for key_id in range(0, len(keys)):
        key = keys[key_id]

        if key != 'is_duplicate':
            value = values[key_id].rstrip()
            if is_float(value):
                value = float(value)
                if value.is_integer():
                    attributes_dict[key].append(int(value))
                else:
                    attributes_dict[key].append(float(value))
            else:
                attributes_dict[key].append(value)

            if key == 'description':
                value = values[key_id].rstrip()
                if value == 'population_study_sample' or 'group_1' in value:
                    attributes_dict['is_duplicate'].append(0)
                else:
                    attributes_dict['is_duplicate'].append(1)

f.close()

save_table_dict_csv(fn_path + 'ololo', attributes_dict)
