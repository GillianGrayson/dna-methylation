from tqdm import tqdm

def get_line_list(line):
    line_list = line.split('\t')
    for val_id in range(0, len(line_list)):
        line_list[val_id] = line_list[val_id].replace('"', '').rstrip()
    return line_list

fn_data = 'E:/YandexDisk/Work/pydnameth/GSE55763/betas'
fn_txt = fn_data + '.txt'

f = open(fn_txt)
header_line = f.readline()
headers = header_line.split('\t')
headers = [x.rstrip() for x in headers]
subjects = headers[1:len(headers)]

morphology_info = np.zeros(len(del_ids),
                           dtype=[('var1', int), ('var2', 'U50'), ('var3', int), ('var4', float),
                                  ('var5', int), ('var6', int), ('var7', int), ('var8', int)])
fmt = "%d %s %d %8e %d %d %d %d"

morphology_info['var1'] = del_ids
morphology_info['var2'] = names
morphology_info['var3'] = indexes
morphology_info['var4'] = values
morphology_info['var5'] = signs
morphology_info['var6'] = degrees
morphology_info['var7'] = branch_ids_0
morphology_info['var8'] = branch_ids_1

np.savetxt(data_file_name, morphology_info, fmt=fmt)

config.betas_data = np.zeros((num_cpgs, len(subjects)), dtype=np.float32)

cpg_id = 0
for line in tqdm(f, mininterval=60.0, desc='betas_data creating'):
    line_list = get_line_list(line)
    curr_data = list(map(np.float32, line_list[1::]))
    config.betas_data[cpg_id] = curr_data
    cpg_id += 1
f.close()

np.savez_compressed(fn_npz, data=config.betas_data)
