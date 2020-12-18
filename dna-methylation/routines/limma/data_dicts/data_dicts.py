def get_data_dicts(path, datasets, keys_load, keys_save):

    data_dicts = {}
    for ds_id, dataset in enumerate(datasets):

        curr_load_path = f'{dataset.path}/{dataset.name}/{dataset.type}/table/{method}/{hash_fun(dataset)}'
        data_dict = load_table_dict_pkl(f'{curr_load_path}/default.pkl')

        data_dicts[dataset.name] = defaultdict(list)

        num_cpgs = len(data_dict[keys_load[dataset.name][0]])

        for cpg_id in tqdm(range(0, num_cpgs), desc=f'{dataset.name} processing'):
            for key_id, key in enumerate(keys_save):
                data_dicts[dataset.name][key].append(data_dict[keys_load[dataset.name][key_id]][cpg_id])

    return data_dicts
