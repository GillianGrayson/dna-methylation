from functools import reduce
import numpy as np
import pandas as pd
from sklearn.model_selection import RepeatedKFold, GridSearchCV
from sklearn.linear_model import ElasticNet
import os
import copy
from sklearn.metrics import mean_squared_error, mean_absolute_error
import pickle


path = f"E:/YandexDisk/Work/pydnameth/lists"

cpgs_agena = np.loadtxt(F"{path}/agena/cpgs(17).txt", dtype='str')

cpgs_horvath = np.loadtxt(F"{path}/epigenetic_clock/DNAmAge.txt", dtype='str')

cpgs_ds_1_1 = np.loadtxt(F"{path}/down_syndrome/kw_dataset_1.txt", dtype='str')
cpgs_ds_1_2 = np.loadtxt(F"{path}/down_syndrome/meta.txt", dtype='str')
cpgs_ds_1_3 = np.loadtxt(F"{path}/down_syndrome/lin_dataset_3.txt", dtype='str')
cpgs_ds_2_1 = np.loadtxt(F"{path}/down_syndrome/anova_all_classes.txt", dtype='str')

num_agena_ds_1_1 = len(set(cpgs_agena).intersection(set(cpgs_ds_1_1)))
num_agena_ds_1_2 = len(set(cpgs_agena).intersection(set(cpgs_ds_1_2)))
num_agena_ds_1_3 = len(set(cpgs_agena).intersection(set(cpgs_ds_1_3)))
num_agena_ds_2_1 = len(set(cpgs_agena).intersection(set(cpgs_ds_2_1)))

num_horvath_ds_1_1 = len(set(cpgs_horvath).intersection(set(cpgs_ds_1_1)))
num_horvath_ds_1_2 = len(set(cpgs_horvath).intersection(set(cpgs_ds_1_2)))
num_horvath_ds_1_3 = len(set(cpgs_horvath).intersection(set(cpgs_ds_1_3)))
num_horvath_ds_2_1 = len(set(cpgs_horvath).intersection(set(cpgs_ds_2_1)))

ololo = 1
