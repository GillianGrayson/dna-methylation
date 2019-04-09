import os.path

source_path = '/common/home/yusipov_i/Work/dna-methylation/dna-methylation'
source_name = 'scripts.develop.load_epimutations'

os.system('sbatch ./submit.sh' + ' ' + source_path + ' ' + source_name)
