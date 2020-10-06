from routines.limma.annotations.load import load_annotations_dict
from routines.limma.annotations.subset import subset_annotations
from routines.limma.annotations.annotations import Annotations
from routines.limma.annotations.excluded import load_excluded
import os.path


path = 'E:/YandexDisk/Work/pydnameth/limma'

datasets = ['GSE87571', 'GSE74193', 'liver']
data_type = 'm'

annotations = Annotations(
    name='annotations',
    type='450k',
    exclude='bad_cpgs',
    select_dict={
        'CHR': ['-X', '-Y']
    }
)

dataset_path_dict = {
    'GSE87571': 'E:/YandexDisk/Work/pydnameth/GSE87571',
    'GSE74193': 'E:/YandexDisk/Work/pydnameth/tissues/brain(DLPFC)/GSE74193',
    'liver': 'E:/YandexDisk/Work/pydnameth/liver'
}

for dataset in datasets:
    ds_path = dataset_path_dict[dataset]
    annotations_dict = load_annotations_dict(f'{ds_path}/annotations')
    excluded = load_excluded(f'{ds_path}/bad_cpgs')
    subset_path = f'{path}/{dataset}'
    if not os.path.exists(subset_path):
        os.makedirs(subset_path)
    subset = subset_annotations(annotations, annotations_dict, excluded, subset_path)

    a = 0
