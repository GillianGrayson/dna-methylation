import pandas as pd
import numpy as np

fn_850k = f'E:/YandexDisk/Work/pydnameth/articles/epigenetic_clock/cpgs_850K.txt'
fn_unn_epic = f'E:/YandexDisk/Work/pydnameth/articles/epigenetic_clock/cpgs_unn_epic_new.txt'
fn_levine = f'E:/YandexDisk/Work/pydnameth/articles/epigenetic_clock/Levine_2018/cpgs.txt'

with open(fn_850k) as f:
    cpgs_850k = set(f.read().splitlines())

with open(fn_unn_epic) as f:
    cpgs_unn_epic = set(f.read().splitlines())

with open(fn_levine) as f:
    cpgs_levine = set(f.read().splitlines())


I = set.intersection(cpgs_850k, cpgs_unn_epic, cpgs_levine)

a = 1