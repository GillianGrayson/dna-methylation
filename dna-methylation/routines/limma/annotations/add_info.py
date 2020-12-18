from paper.routines.infrastructure.load.annotations import load_annotations_dict
from paper.routines.data.human_plasma_proteome import *
from statsmodels.stats.multitest import multipletests
import copy


def add_info_to_dict(data_dict, cpg_key='CpG'):

    annotations_keys = ['CHR', 'MAPINFO', 'UCSC_REFGENE_NAME', 'UCSC_REFGENE_GROUP', 'RELATION_TO_UCSC_CPG_ISLAND']
    annotations_dict = load_annotations_dict()

    for key in annotations_keys:
        data_dict[key] = []

    for cpg in data_dict[cpg_key]:
        for key in annotations_keys:
            data_dict[key].append(annotations_dict[key][cpg])

    reject, pvals_corr, alphacSidak, alphacBonf = multipletests(
        data_dict['Sex_P.Value'],
        0.05,
        method='fdr_bh'
    )
    data_dict['Sex_P.Value_fdr_bh'] = pvals_corr

    reject, pvals_corr, alphacSidak, alphacBonf = multipletests(
        data_dict['Sex_P.Value'],
        0.05,
        method='bonferroni'
    )
    data_dict['Sex_P.Value_bf'] = pvals_corr

    reject, pvals_corr, alphacSidak, alphacBonf = multipletests(
        data_dict['Age_P.Value'],
        0.05,
        method='fdr_bh'
    )
    data_dict['Age_P.Value_fdr_bh'] = pvals_corr

    reject, pvals_corr, alphacSidak, alphacBonf = multipletests(
        data_dict['Age_P.Value'],
        0.05,
        method='bonferroni'
    )
    data_dict['Age_P.Value_bf'] = pvals_corr

    return data_dict