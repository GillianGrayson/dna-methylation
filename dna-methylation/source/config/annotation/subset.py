from source.infrastucture.path import *
from source.config.annotation.conditions import *
import os.path
import pickle
import numpy as np


def subset_annotations(config):
    cpg_list_fn = get_cache_path(config) + '/' + 'cpg_list.pkl'
    cpg_gene_dict_fn = get_cache_path(config) + '/' + 'cpg_gene_dict.pkl'
    cpg_bop_dict_fn = get_cache_path(config) + '/' + 'cpg_bop_dict.pkl'
    gene_cpg_dict_fn = get_cache_path(config) + '/' + 'gene_cpg_dict.pkl'
    gene_bop_dict_fn = get_cache_path(config) + '/' + 'gene_bop_dict.pkl'
    bop_cpg_dict_fn = get_cache_path(config) + '/' + 'bop_cpg_dict.pkl'
    bop_gene_dict_fn = get_cache_path(config) + '/' + 'bop_gene_dict.pkl'

    is_pkl = True

    if os.path.isfile(cpg_list_fn):
        f = open(cpg_list_fn, 'rb')
        config.cpg_list = pickle.load(f)
        f.close()
    else:
        is_pkl = False

    if os.path.isfile(cpg_gene_dict_fn):
        f = open(cpg_gene_dict_fn, 'rb')
        config.cpg_gene_dict = pickle.load(f)
        f.close()
    else:
        is_pkl = False

    if os.path.isfile(cpg_bop_dict_fn):
        f = open(cpg_bop_dict_fn, 'rb')
        config.cpg_bop_dict = pickle.load(f)
        f.close()
    else:
        is_pkl = False

    if os.path.isfile(gene_cpg_dict_fn):
        f = open(gene_cpg_dict_fn, 'rb')
        config.gene_cpg_dict = pickle.load(f)
        f.close()
    else:
        is_pkl = False

    if os.path.isfile(gene_bop_dict_fn):
        f = open(gene_bop_dict_fn, 'rb')
        config.gene_bop_dict = pickle.load(f)
        f.close()
    else:
        is_pkl = False

    if os.path.isfile(bop_cpg_dict_fn):
        f = open(bop_cpg_dict_fn, 'rb')
        config.bop_cpg_dict = pickle.load(f)
        f.close()
    else:
        is_pkl = False

    if os.path.isfile(bop_gene_dict_fn):
        f = open(bop_gene_dict_fn, 'rb')
        config.bop_gene_dict = pickle.load(f)
        f.close()
    else:
        is_pkl = False

    if not is_pkl:

        config.cpg_list = []
        config.cpg_gene_dict = {}
        config.cpg_bop_dict = {}
        config.gene_cpg_dict = {}
        config.gene_bop_dict = {}
        config.bop_cpg_dict = {}
        config.bop_gene_dict = {}

        cpgs = config.annotation_dict[AnnotationKey.cpg.value]
        genes = config.annotation_dict[AnnotationKey.gene.value]
        bops = config.annotation_dict[AnnotationKey.bop.value]
        map_infos = config.annotation_dict[AnnotationKey.map_info.value]
        for id in range(0, len(cpgs)):

            if id % 10000 == 0:
                print('id: ' + str(id))

            curr_ann_dict = {}
            for key in config.annotation_dict:
                curr_ann_dict[key] = config.annotation_dict[key][id]

            if check_conditions(config, curr_ann_dict):

                cpg = cpgs[id]
                gene_raw = genes[id]
                curr_genes = list(set(gene_raw.split(';')))
                bop = bops[id]

                config.cpg_list.append(cpg)

                config.cpg_gene_dict[cpg] = curr_genes

                config.cpg_bop_dict[cpg] = bop

                for gene in curr_genes:
                    if gene in config.gene_cpg_dict:
                        config.gene_cpg_dict[gene].append(cpg)
                    else:
                        config.gene_cpg_dict[gene] = [cpg]

                for gene in curr_genes:
                    if gene in config.gene_bop_dict:
                        config.gene_bop_dict[gene].append(bop)
                    else:
                        config.gene_bop_dict[gene] = [bop]

                if len(bop) > 0:
                    if bop in config.bop_cpg_dict:
                        config.bop_cpg_dict[bop].append(cpg)
                    else:
                        config.bop_cpg_dict[bop] = [cpg]

                config.bop_gene_dict[bop] = curr_genes

        # Sorting cpgs by map_info in gene dict
        for curr_gene, curr_cpgs in config.gene_cpg_dict.items():
            curr_map_infos = []
            for curr_cpg in curr_cpgs:
                cpg_index = cpgs.index(curr_cpg)
                curr_map_infos.append(int(map_infos[cpg_index]))
            order = np.argsort(curr_map_infos)
            curr_cpgs_sorted = list(np.array(curr_cpgs)[order])
            config.gene_cpg_dict[curr_gene] = curr_cpgs_sorted

        # Sorting cpgs by map_info in bop dict
        for curr_bop, curr_cpgs in config.bop_cpg_dict.items():
            curr_map_infos = []
            for curr_cpg in curr_cpgs:
                cpg_index = cpgs.index(curr_cpg)
                curr_map_infos.append(int(map_infos[cpg_index]))
            order = np.argsort(curr_map_infos)
            curr_cpgs_sorted = list(np.array(curr_cpgs)[order])
            config.bop_cpg_dict[curr_bop] = curr_cpgs_sorted

        f = open(cpg_list_fn, 'wb')
        pickle.dump(config.cpg_list, f, pickle.HIGHEST_PROTOCOL)
        f.close()

        f = open(cpg_gene_dict_fn, 'wb')
        pickle.dump(config.cpg_gene_dict, f, pickle.HIGHEST_PROTOCOL)
        f.close()

        f = open(cpg_bop_dict_fn, 'wb')
        pickle.dump(config.cpg_bop_dict, f, pickle.HIGHEST_PROTOCOL)
        f.close()

        f = open(gene_cpg_dict_fn, 'wb')
        pickle.dump(config.gene_cpg_dict, f, pickle.HIGHEST_PROTOCOL)
        f.close()

        f = open(gene_bop_dict_fn, 'wb')
        pickle.dump(config.gene_bop_dict, f, pickle.HIGHEST_PROTOCOL)
        f.close()

        f = open(bop_cpg_dict_fn, 'wb')
        pickle.dump(config.bop_cpg_dict, f, pickle.HIGHEST_PROTOCOL)
        f.close()

        f = open(bop_gene_dict_fn, 'wb')
        pickle.dump(config.bop_gene_dict, f, pickle.HIGHEST_PROTOCOL)
        f.close()
