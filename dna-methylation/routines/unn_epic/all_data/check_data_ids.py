import pandas as pd
import numpy as np

path = f'E:/YandexDisk/Work/pydnameth/unn_epic/all_data/markers/IDs.xlsx'

df = pd.read_excel(path)

DNAm = df['ID_DNAm'].values
DNAm = DNAm[~pd.isnull(DNAm)]
BioChem = df['ID_BioChem'].values
BioChem = BioChem[~pd.isnull(BioChem)]
Multiplex = df['ID_Multiplex'].values
Multiplex = Multiplex[~pd.isnull(Multiplex)]

BioChem_missed = list(set(DNAm) - set(BioChem))
Multiplex_missed = list(set(DNAm) - set(Multiplex))

print(f'BioChem_missed:')
print(*BioChem_missed, sep='\n')

print(f'Multiplex_missed:')
print(*Multiplex_missed, sep='\n')

inter = set.intersection(set(DNAm), set(BioChem), set(Multiplex))
print(f'intersection: {len(inter)}')

