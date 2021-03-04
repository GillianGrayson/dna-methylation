import pickle

cpg_file_path = ''
cpg_file_name = '../cpgs.txt'
f = open(cpg_file_path + cpg_file_name, 'r')
cpgs = [line.rstrip('\n') for line in f]
f.close()

databases_path = 'C:/Users/User/YandexDisk/pydnameth/'
databases = ['GSE40279', 'GSE87571', 'EPIC', 'GSE55763']
betas_dict_file_name = 'betas_dict.pkl'
databases_paths = [databases_path + database + '\\' + betas_dict_file_name for database in databases]

for database in databases_paths:
    f = open(database, 'rb')
    betas_dict = pickle.load(f)
    f.close()

    curr_cpgs = list(betas_dict.keys())
    cpgs = list(set(cpgs) & set(curr_cpgs))

save_path = 'D:/Aaron/Bio/variance/v2/'
save_name = '_'.join(databases)
f = open(save_path + 'cpgs_' + save_name + '.txt', 'w')
for cpg in cpgs:
    f.write("%s\n" % cpg)
f.close()
