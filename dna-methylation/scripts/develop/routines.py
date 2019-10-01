def get_data_params(data_base):

    if data_base == 'E-MTAB-7309' or data_base == 'E-MTAB-7309-FILTERED':
        data_params = {
            'norm': 'quantile',
        }
    else:
        data_params = None

    return data_params


def get_observables_list(data_base):

    if data_base == 'GSE55763':
        observables_list = [
            {'gender': 'F', 'is_duplicate': '0', 'age': (35, 100)},
            {'gender': 'M', 'is_duplicate': '0', 'age': (35, 100)}
        ]
    elif data_base == 'GSE64244':
        observables_list = [
            {'disease_status': 'Turner_syndrome_45,X_(Maternal)'},
            {'disease_status': 'Turner_syndrome_45,X_(Paternal)'}
        ]
    elif data_base == 'GSE43414':
        observables_list = [
            {'source_tissue': 'cerebellum', 'Sex': 'FEMALE'},
            {'source_tissue': 'cerebellum', 'Sex': 'MALE'}
        ]
    elif data_base == 'GSE88890':
        observables_list = [
            {'gender': 'F'},
            {'gender': 'M'}
        ]
    elif data_base == 'GSE41826':
        observables_list = [
            {'Sex': 'Female'},
            {'Sex': 'Male'}
        ]
    elif data_base == 'E-MTAB-7309':
        observables_list = [
            {'sex': 'female'},
            {'sex': 'male'}
        ]
    elif data_base == 'E-MTAB-7309-FILTERED':
        observables_list = [
            {'sex': 'female'},
            {'sex': 'male'}
        ]
    elif data_base == 'GSE61256':
        observables_list = [
            {'Sex': 'female'},
            {'Sex': 'male'}
        ]
    elif data_base == 'control':
        observables_list = [
            {'Sex': 'F'},
            {'Sex': 'M'}
        ]
    elif data_base == 'centenarian':
        observables_list = [
            {'Sex': 'F'},
            {'Sex': 'M'}
        ]
    elif data_base == 'down':
        observables_list = [
            {'Sex': 'F'},
            {'Sex': 'M'}
        ]
    elif data_base == 'offspring':
        observables_list = [
            {'Sex': 'F'},
            {'Sex': 'M'}
        ]
    else:
        observables_list = [
            {'gender': 'F'},
            {'gender': 'M'}
        ]

    return observables_list


def get_target(data_base):
    if data_base == 'GSE55763':
        target = 'age'
    elif data_base == 'GSE64244':
        target = 'age'
    elif data_base == 'GSE43414':
        target = 'age.brain'
    elif data_base == 'GSE88890':
        target = 'age'
    elif data_base == 'GSE41826':
        target = 'age'
    elif data_base == 'E-MTAB-7309':
        target = 'age'
    elif data_base == 'E-MTAB-7309-FILTERED':
        target = 'age'
    elif data_base == 'GSE61256':
        target = 'age'
    elif data_base == 'control':
        target = 'Age'
    elif data_base == 'centenarian':
        target = 'Age'
    elif data_base == 'down':
        target = 'Age'
    elif data_base == 'offspring':
        target = 'Age'
    else:
        target = 'age'

    return target