def get_approach_1_hash(dataset):
    if dataset.type == 'betas':
        hash = {
            'GSE40279': '7875dff3886829397f5fbbbf9aaae009',
            'GSE87571': '8c357499960c0612f784ca7ed3fedb2c',
            'EPIC': '23298d48a2fbeb252cfdcb90cfa004a3',
            'GSE55763': '67553bd9c9801d1eeeba0dc2776db156'
        }
    else:
        raise ValueError(f'{dataset.type} is not supported')

    return hash[dataset.name]


def get_linreg_female_hash(dataset):
    if dataset.type == 'betas':
        hash = {
            'GSE40279': '6e5e9526',
            'GSE87571': '31efe635',
            'EPIC': '7383db3e',
            'GSE55763': '6a7442e0'
        }
    else:
        raise ValueError(f'{dataset.type} is not supported')

    return hash[dataset.name]


def get_linreg_male_hash(dataset):
    if dataset.type == 'betas':
        hash = {
            'GSE40279': '40e12959',
            'GSE87571': '3dd80109',
            'EPIC': '191c0e80',
            'GSE55763': '0a75a8f8'
        }
    else:
        raise ValueError(f'{dataset.type} is not supported')

    return hash[dataset.name]


def get_polygon_hash(dataset):
    if dataset.type == 'betas':
        hash = {
            'GSE40279': 'ebc9f2bd',
            'GSE87571': 'c5e6999a',
            'EPIC': 'f410e129',
            'GSE55763': 'fa723546'
        }
    else:
        raise ValueError(f'{dataset.type} is not supported')

    return hash[dataset.name]
