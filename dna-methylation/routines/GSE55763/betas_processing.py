from tqdm import tqdm
import numpy as np

def get_line_list(line):
    line_list = line.split('\t')
    for val_id in range(0, len(line_list)):
        line_list[val_id] = line_list[val_id].replace('"', '').rstrip()
    return line_list

fn_path = 'E:/YandexDisk/Work/pydnameth/GSE55763/'
fn_txt = fn_path + 'betas_raw.txt'

num_lines = 473865
num_cpgs = num_lines - 1

f = open(fn_txt)
header_line = f.readline()
headers = header_line.split('\t')
headers = [x.rstrip() for x in headers]

betas_indexes = [0] + list(range(1, len(headers), 2))
pvals_indexes = [0] + list(range(2, len(headers), 2))
betas_cols = [headers[i] for i in betas_indexes]
pvals_cols = [headers[i] for i in betas_indexes]
num_cols = len(betas_cols)

np.savetxt(fn_path + 'subjects.txt', np.asarray(betas_cols[1::]), fmt='%s')

row_id = 0
betas_arr = np.zeros(num_lines, dtype=object)
betas_arr[row_id] = '\t'.join(betas_cols)
pvals_arr = np.zeros(num_lines, dtype=object)
pvals_arr[row_id] = '\t'.join(pvals_cols)

row_id += 1
for line in tqdm(f, mininterval=60.0, desc='betas_dict creating'):
    line_list = get_line_list(line)
    betas_cols = [line_list[i] for i in betas_indexes]
    pvals_cols = [line_list[i] for i in pvals_indexes]
    betas_arr[row_id] = '\t'.join(betas_cols)
    pvals_arr[row_id] = '\t'.join(pvals_cols)
    row_id += 1
f.close()

np.savetxt(fn_path + 'betas.txt', betas_arr, fmt='%s')
np.savetxt(fn_path + 'pvals.txt', pvals_arr, fmt='%s')
