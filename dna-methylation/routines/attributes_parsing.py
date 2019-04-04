from os import listdir
from os.path import isfile, join
import csv

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

path = 'D:/YandexDisk/Work/pydnameth/E-MTAB-7309/raw'

fn_txt = path + '/E-MTAB-7309.sdrf.txt'

f = open(fn_txt)
key_line = f.readline()
header_keys = key_line.split('\t')
header_keys = [x.rstrip() for x in header_keys]

target_key = 'Array Data File'

keys = [
    'Source Name',
    'Characteristics[organism]',
    'Characteristics[individual]',
    'Characteristics[age]',
    'Unit[time unit]',
    'Characteristics[sex]',
    'Characteristics[organism part]',
    'Characteristics[cell type]',
    'Characteristics[disease]',
    'Characteristics[twin pair]',
    'Material Type',
    'Protocol REF',
    'Factor Value[individual]',
    'Slide',
    'Array',
    'Basename'
]

attributes_dict = {}
for key in keys:
    attributes_dict[key] = []


for line in f:
    values = line.split('\t')
    if not values[25].rstrip().endswith('Grn.idat'):
        for key_id in range(0, len(header_keys)):
            key = header_keys[key_id]
            value = values[key_id].rstrip()

            if key == target_key:
                parts = value.split('_')
                attributes_dict['Slide'].append(parts[0])
                attributes_dict['Array'].append(parts[1])
                attributes_dict['Basename'].append(parts[0] + '_' + parts[1])

            if key in keys:
                if is_float(value):
                    value = float(value)
                    if value.is_integer():
                        attributes_dict[key].append(int(value))
                    else:
                        attributes_dict[key].append(float(value))
                else:
                    attributes_dict[key].append(value)
f.close()

fn_csv = path + '/sample_sheet2.csv'
with open(fn_csv, 'w') as csvfile:
    writer = csv.DictWriter(csvfile,
                            fieldnames=attributes_dict.keys(),
                            lineterminator='\n')
    writer.writeheader()
    for id in range(0, len(list(attributes_dict.values())[0])):
        tmp_dict = {}
        for key, values in attributes_dict.items():
            tmp_dict[key] = values[id]
        writer.writerow(tmp_dict)

a = 1