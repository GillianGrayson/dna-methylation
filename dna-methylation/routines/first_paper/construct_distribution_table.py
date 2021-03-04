import pandas as pd
import csv
from itertools import zip_longest

data_path = 'C:/Users/User/YandexDisk/pydnameth/variance/residuals/'
data_files = ['GSE40279.xlsx', 'GSE87571.xlsx', 'EPIC.xlsx', 'GSE55763.xlsx']

data_min = []

for data_file in data_files:
    print(data_file[:-5])
    curr_data = pd.read_excel(data_path + data_file)
    curr_r2_min = list(curr_data.r2_min)

    for id in range(0, len(curr_r2_min)):
        if curr_r2_min[id] == -1:
            curr_r2_min[id] = 0.0

    data_min.append([data_file[:-5]] + curr_r2_min)

with open(data_path + "R2_min.csv","w", newline='') as f:
    writer = csv.writer(f)
    for values in zip_longest(*data_min):
        writer.writerow(values)
