from tqdm import tqdm
import numpy as np

def get_line_list(line):
    line_list = line.split('\t')
    for val_id in range(0, len(line_list)):
        line_list[val_id] = line_list[val_id].replace('"', '').rstrip()
    return line_list

fn_path = 'D:/YandexDisk/Work/pydnameth/GSE61256/'
fn_txt = fn_path + 'betas.txt'

num_lines = 438216


f = open(fn_txt)
header_line = f.readline()
headers = header_line.split('\t')
headers = [x.rstrip().replace('"', '') for x in headers]

betas_indexes = [0] + list(range(1, len(headers)))
betas_cols = [headers[i] for i in betas_indexes]
betas_cols[0] = 'ID_REF'
num_cols = len(betas_cols)

np.savetxt(fn_path + 'subjects.txt', np.asarray(betas_cols[1::]), fmt='%s')

row_id = 0
betas_arr = np.zeros(num_lines, dtype=object)
betas_arr[row_id] = '\t'.join(betas_cols)

total_NA_cpgs = 0
NA_indexes = np.zeros(num_cols)

row_id += 1
for line in tqdm(f, mininterval=60.0, desc='betas_dict creating'):
    line_list = get_line_list(line)
    betas_cols = [line_list[i] for i in betas_indexes]

    if '' in betas_cols:
        total_NA_cpgs += 1
        NA_indexes_curr = [i for i, x in enumerate(betas_cols) if x == '']
        for NA_index in NA_indexes_curr:
            NA_indexes[NA_index] += 1
    else:
        betas_arr[row_id] = '\t'.join(betas_cols)
        row_id += 1

f.close()

print(f'total_NA_cpgs: {total_NA_cpgs}')
print(f'num_rows: {row_id}')
np.savetxt(fn_path + 'NA_indexes.txt', NA_indexes, fmt='%d')

np.savetxt(fn_path + 'betas11.txt', betas_arr, fmt='%s')
