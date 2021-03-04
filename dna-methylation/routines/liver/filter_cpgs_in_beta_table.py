import numpy as np
import pandas as pd


path = "E:/YandexDisk/Work/pydnameth/liver"

bad_cpgs = np.loadtxt(f"{path}/bad_cpgs.txt", dtype=str).tolist()
df = pd.read_csv(f"{path}/betas.txt", delimiter = "\t", index_col=0)
all_cpgs = df.index.values
drop_cpgs = list(set.intersection(set(bad_cpgs), set(all_cpgs)))
df.drop(index = drop_cpgs, inplace=True)
df.to_csv(f'{path}/betas_filtered.csv', index=True)


