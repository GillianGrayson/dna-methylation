import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
from numpy import unique


num_components = 2
features = ['DNAmAgeHannumAA', 'DNAmAgeAA', 'IEAA',  'DNAmPhenoAgeAA', 'DNAmGrimAgeAA', 'PhenoAgeAA', 'ImmunoAgeAA']

dbscan_eps = 0.5
dbscan_min_samples = 5

part = 'v2'
path = f'E:/YandexDisk/Work/pydnameth/unn_epic/all_data'
df = pd.read_excel(f'{path}/table_part({part}).xlsx', converters={'ID': str}, engine='openpyxl')
C_df = df.loc[df['Group'] == 'Control']
T_df = df.loc[df['Group'] == 'Disease']

with open(f'{path}/immuno.txt') as f:
    immuno_features = f.read().splitlines()

for f_id, f in enumerate(features):
    scaler = StandardScaler()
    data = df[f].to_numpy().reshape(-1, 1)
    train = C_df[f].to_numpy().reshape(-1, 1)
    scaler.fit(train)
    scaled = scaler.transform(data)
    df[f"{f}_scaled"] = scaled

scaled_features = [s + "_scaled" for s in features]
x = df.loc[:, features].values
x_immuno = df.loc[:, immuno_features].values

pca = PCA(n_components=num_components)
pca.fit(x)
pcs = pca.transform(x)

pca_dict = {'features': features}
for pc_id in range(0, pcs.shape[1]):
    pca_dict[f'PC{pc_id}'] = pca.components_[pc_id, :]

pca_df = pd.DataFrame(pca_dict)

tsne = TSNE(n_components=num_components)
tsnes = tsne.fit_transform(x)

pca_immuno = PCA(n_components=num_components)
pcs_immuno = pca_immuno.fit_transform(x_immuno)

scaled_pcs_features = []
for pc_id in range(0, pcs.shape[1]):
    pc = pcs[:, pc_id]
    df[f"AA_pc_{pc_id}"] = pc
    # pc_immuno = pcs_immuno[:, pc_id]
    # df[f"immuno_pc_{pc_id}"] = pc_immuno

    # scaler = StandardScaler()
    # data = pc.reshape(-1, 1)
    # scaled = scaler.fit_transform(data)
    # feature = f"AA_pc_{pc_id}_scaled"
    # scaled_pcs_features.append(feature)
    # df[feature] = scaled

# scaled_tsne_features = []
# for pc_id in range(0, pcs.shape[1]):
#     ts = tsnes[:, pc_id]
#     df[f"AA_tsne_{pc_id}"] = ts
#     scaler = StandardScaler()
#     data = ts.reshape(-1, 1)
#     scaled = scaler.fit_transform(data)
#     feature = f"AA_tsne_{pc_id}_scaled"
#     scaled_tsne_features.append(feature)
#     df[feature] = scaled

# x_pca = df.loc[:, features].values
# model_pca = DBSCAN(eps=dbscan_eps, min_samples=dbscan_min_samples)
# dbscan_pca_clusters = model_pca.fit_predict(x_pca)
# df['pca_dbscan'] = dbscan_pca_clusters
#
#
# x_tsne = df.loc[:, features].values
# model_tsne = DBSCAN(eps=dbscan_eps, min_samples=dbscan_min_samples)
# dbscan_tsne_clusters = model_tsne.fit_predict(x_tsne)
# df['tsne_dbscan'] = dbscan_tsne_clusters

df.to_excel(f'{path}/current_table.xlsx', index=False)

pca_df.to_excel(f'{path}/pca.xlsx', index=False)