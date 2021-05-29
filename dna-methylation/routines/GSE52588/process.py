from functools import reduce
import numpy as np
import pandas as pd
from sklearn.model_selection import RepeatedKFold, GridSearchCV
from sklearn.linear_model import ElasticNet
import os
import copy
from sklearn.metrics import mean_squared_error, mean_absolute_error
from functools import reduce
import os
import pickle
import tqdm


path = "E:/YandexDisk/Work/pydnameth/GSE52588"

pheno = pd.read_csv(f"{path}/GSE52588_samples.txt", delimiter = "\t", index_col='geo_accession')
pheno.index.name = "ID"
subjects = pheno.index.values.tolist()

data = np.load(f"{path}/GSE52588_beta_fn.npz")
X = data['X_all']
X_r = data['X_r']
X_r2 = data['X_r2']
all_cpg_names = data['all_cpg_names']
beta = pd.DataFrame(data=X, index=subjects, columns=all_cpg_names)
beta.index.name = "ID"

d = {'pheno': pheno, 'beta': beta}

f = open(f'{path}/data.pkl', 'wb')
pickle.dump(d, f, pickle.HIGHEST_PROTOCOL)
f.close()
