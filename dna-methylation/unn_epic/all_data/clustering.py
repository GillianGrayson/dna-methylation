import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
from numpy import unique


num_components = 3
features = ['DNAmAgeHannumAA', 'DNAmAgeAA', 'DNAmPhenoAgeAA', 'DNAmGrimAgeAA', 'PhenoAgeAA', 'ImmunoAgeAA']

dbscan_eps = 0.5
dbscan_min_samples = 5

part = 'v2'
path = f'E:/YandexDisk/Work/pydnameth/unn_epic/all_data'
df = pd.read_excel(f'{path}/table_part({part}).xlsx', converters={'ID': str}, engine='openpyxl')
C_df = df.loc[df['Group'] == 'Control']
T_df = df.loc[df['Group'] == 'Disease']

for f_id, f in enumerate(features):
    scaler = StandardScaler()
    data = df[f].to_numpy().reshape(-1, 1)
    scaled = scaler.fit_transform(data)
    df[f"{f}_scaled"] = scaled

scaled_features = [s + "_scaled" for s in features]
x = df.loc[:, scaled_features].values

pca = PCA(n_components=num_components)
pcs = pca.fit_transform(x)

tsne = TSNE(n_components=num_components)
tsnes = tsne.fit_transform(x)

scaled_pcs_features = []
for pc_id in range(0, pcs.shape[1]):
    pc = pcs[:, pc_id]
    df[f"AA_pc_{pc_id}"] = pc
    scaler = StandardScaler()
    data = pc.reshape(-1, 1)
    scaled = scaler.fit_transform(data)
    feature = f"AA_pc_{pc_id}_scaled"
    scaled_pcs_features.append(feature)
    df[feature] = scaled

scaled_tsne_features = []
for pc_id in range(0, pcs.shape[1]):
    ts = tsnes[:, pc_id]
    df[f"AA_tsne_{pc_id}"] = ts
    scaler = StandardScaler()
    data = ts.reshape(-1, 1)
    scaled = scaler.fit_transform(data)
    feature = f"AA_tsne_{pc_id}_scaled"
    scaled_tsne_features.append(feature)
    df[feature] = scaled

x_pca = df.loc[:, scaled_pcs_features].values
model_pca = DBSCAN(eps=dbscan_eps, min_samples=dbscan_min_samples)
dbscan_pca_clusters = model_pca.fit_predict(x_pca)
df['pca_dbscan'] = dbscan_pca_clusters


x_tsne = df.loc[:, scaled_tsne_features].values
model_tsne = DBSCAN(eps=dbscan_eps, min_samples=dbscan_min_samples)
dbscan_tsne_clusters = model_tsne.fit_predict(x_tsne)
df['tsne_dbscan'] = dbscan_tsne_clusters

df.to_excel(f'{path}/current_table.xlsx', index=False)