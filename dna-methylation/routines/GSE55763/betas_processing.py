from tqdm import tqdm

def get_line_list(line):
    line_list = line.split('\t')
    for val_id in range(0, len(line_list)):
        line_list[val_id] = line_list[val_id].replace('"', '').rstrip()
    return line_list

fn_data = 'D:/YandexDisk/Work/pydnameth/GSE55763/betas'
fn_txt = fn_data + '.txt'

f = open(fn_txt)
header_line = f.readline()
headers = header_line.split('\t')
headers = [x.rstrip() for x in headers]
subjects = headers[1:len(headers)]

config.betas_data = np.zeros((num_cpgs, len(subjects)), dtype=np.float32)

cpg_id = 0
for line in tqdm(f, mininterval=60.0, desc='betas_data creating'):
    line_list = get_line_list(line)
    curr_data = list(map(np.float32, line_list[1::]))
    config.betas_data[cpg_id] = curr_data
    cpg_id += 1
f.close()

np.savez_compressed(fn_npz, data=config.betas_data)
