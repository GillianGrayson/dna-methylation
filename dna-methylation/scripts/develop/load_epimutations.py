import pydnameth as pdm

data = pdm.Data(
    name='cpg_beta',
    path='',
    base='GSE87571'
)

pdm.epimutations_load_dev(data)