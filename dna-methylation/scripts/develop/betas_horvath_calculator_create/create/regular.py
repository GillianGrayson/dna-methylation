import pydnameth as pdm

data = pdm.Data(
    path='',
    base='GSE87571'
)

pdm.betas_horvath_calculator_create_regular(data)
