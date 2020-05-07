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


def get_approach_3_hash(dataset):
    if dataset.type == 'residuals':
        hash = {
            'GSE40279': 'bf0b9f92e948a257329262816ce3d202',
            'GSE87571': '7c468ca8212428806c727d3e2a836662',
            'EPIC': 'a64c0b99b7e097c668e8300e29ad693f',
            'GSE55763': '01f9edb1330453690b493c5a17624c6c',
            'liver': '81f11bc49cb451091c552dce079bb478'
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


def get_ss_hash(dataset):
    if dataset.type == 'residuals':
        hash = {
            'GSE40279': 'f6796cdb',
            'GSE87571': '960bd640',
            'EPIC': '1a502535',
            'GSE55763': 'fb0b2483',
            'liver': 'ded0cd22'
        }
    else:
        raise ValueError(f'{dataset.type} is not supported')

    return hash[dataset.name]


def get_ar_hash(dataset):
    if dataset.type == 'residuals':
        hash = {
            'GSE40279': '5c6afd44',
            'GSE87571': '6af05523',
            'EPIC': '018fad6b',
            'GSE55763': 'c7e956c1',
            'liver': 'b1f058b7'
        }
    else:
        raise ValueError(f'{dataset.type} is not supported')

    return hash[dataset.name]