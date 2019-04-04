from os import listdir
from os.path import isfile, join
import csv

path = 'D:/YandexDisk/Work/pydnameth/GSE87571/raw/input_data'

sample_ids = []
slides = []
arrays = []
base_names = []

for fn in listdir(path):
    if isfile(join(path, fn)):
        parts = fn.split('_')
        if parts[-1] == 'Red.idat':
            sample_ids.append(parts[0])
            slides.append(parts[1])
            arrays.append(parts[2])
            base_names.append(parts[1] + '_' + parts[2])

table_dict = {
    'Sample_ID': sample_ids,
    'Slide': slides,
    'Array': arrays,
    'Basename': base_names
}

fn_csv = path + '/sample_sheet.csv'
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
