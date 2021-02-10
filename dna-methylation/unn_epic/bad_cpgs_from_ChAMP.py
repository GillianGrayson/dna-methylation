from functions.load.utils import get_line_list
from tqdm import tqdm


path = 'E:/YandexDisk/Work/pydnameth/unn_epic'

fn = f'{path}/betas_norm(fun)_part(final).txt'
f = open(fn)
f.readline()
cpgs_full = []
for line in tqdm(f, mininterval=5, desc='cpgs_full'):
    line_list = get_line_list(line)
    cpg = line_list[0]
    cpgs_full.append(cpg)
f.close()

fn = f'{path}/betas_norm(BMIQ)_part(final).txt'
f = open(fn)
f.readline()
cpgs_target = []
for line in tqdm(f, mininterval=5, desc='cpgs_target'):
    line_list = get_line_list(line)
    cpg = line_list[0]
    cpgs_target.append(cpg)
f.close()

bad_cpgs = list(set(cpgs_full) - set(cpgs_target))

with open(f'{path}/bad_cpgs_from_ChAMP.txt', 'w') as f:
    for item in bad_cpgs:
        f.write("%s\n" % item)