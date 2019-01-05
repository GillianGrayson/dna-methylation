from source.infrastucture.load.cpg_data import *
from source.infrastucture.save.table import *
from sklearn.cluster import DBSCAN


def generate_table_cluster(config):
    attribute_dict = config.attribute_dict
    cpg_beta_dict = load_cpg_beta_dict(config)
    cpg_list = config.cpg_list

    target = attribute_dict[config.target]
    target_normed = [(float(x) - min(target)) / (float(max(target)) - float(min(target))) for x in target]

    print('len(cpg_list): ' + str(len(cpg_list)))

    if not bool(config.setup.params):
        config.setup.params = {
            'eps': 0.2,
            'min_samples': int(max(1, np.floor(len(target) * 0.01)))
        }

    cpg_names_passed = []
    number_of_clusters = []
    number_of_noise_points = []

    num_passed = 0

    for cpg in cpg_list:

        if cpg in cpg_beta_dict:

            if num_passed % 10000 == 0:
                print('cpg_id: ' + str(num_passed))

            betas = cpg_beta_dict[cpg]

            X = np.array([target_normed, betas]).T
            db = DBSCAN(eps=config.setup.params['eps'], min_samples=config.setup.params['min_samples']).fit(X)
            core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
            core_samples_mask[db.core_sample_indices_] = True
            labels = db.labels_
            curr_number_of_clusters = len(set(labels)) - (1 if -1 in labels else 0)
            curr_number_of_noise_points = list(labels).count(-1)

            cpg_names_passed.append(cpg)
            number_of_clusters.append(curr_number_of_clusters)
            number_of_noise_points.append(curr_number_of_noise_points)

            num_passed += 1

    order = np.argsort(list(map(abs, number_of_clusters)))[::-1]
    cpgs_sorted = list(np.array(cpg_names_passed)[order])
    number_of_clusters_sorted = list(np.array(number_of_clusters)[order])
    number_of_noise_points_sorted = list(np.array(number_of_noise_points)[order])

    table_dict = {
        'id': cpgs_sorted,
        'number_of_clusters': number_of_clusters_sorted,
        'number_of_noise_points': number_of_noise_points_sorted,
    }

    save_table_dict(config, table_dict)
