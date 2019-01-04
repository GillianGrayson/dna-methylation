from source.config.annotation.types import *


def exclude_condition(config, annotation_dict):
    cpg = annotation_dict[AnnotationKey.cpg.value]
    if cpg in config.excluded:
        return False
    else:
        return True


def cross_reactive_condition(config, annotation_dict):
    target = config.annotation.cross_reactive
    value = annotation_dict[AnnotationKey.cross_reactive.value]

    match = True
    if target == CrossReactive.exclude.value:
        if int(value) == 1:
            match = False

    return match


def snp_condition(config, annotation_dict):
    target = config.annotation.snp
    snp = annotation_dict[AnnotationKey.Probe_SNPs.value]
    snp_10 = annotation_dict[AnnotationKey.Probe_SNPs_10.value]

    match = True
    if target == SNP.exclude.value:
        if snp != '' or snp_10 != '':
            match = False

    return match


def chromosome_condition(config, annotation_dict):
    target = config.annotation.chr
    chr = annotation_dict[AnnotationKey.chr.value]

    match = False
    if target == Chromosome.any.value:
        match = True
    elif target == Chromosome.non_gender.value:
        if chr != Chromosome.X.value and chr != Chromosome.Y.value:
            match = True
    elif target == Chromosome.X.value:
        if chr == Chromosome.X.value:
            match = True
    elif target == Chromosome.Y.value:
        if chr == Chromosome.Y.value:
            match = True
    else:
        if chr == target:
            match = True

    return match


def gene_region_condition(config, annotation_dict):
    target = config.annotation.gene_region
    gene = annotation_dict[AnnotationKey.gene.value]

    match = False
    if target == GeneRegion.any.value:
        match = True
    elif target == GeneRegion.yes.value:
        if len(gene) > 0:
            match = True
    elif target == GeneRegion.no.value:
        if len(gene) == 0:
            match = True

    return match


def geo_condition(config, annotation_dict):
    target = config.annotation.geo
    geo = annotation_dict[AnnotationKey.geo.value]

    match = False
    if target == Geo.any.value:
        match = True
    else:
        keys_preset = [x.value for x in Geo]
        possible_geos = []
        if target in keys_preset:
            if target == Geo.islands.value:
                possible_geos.append('Island')
            elif target == Geo.shores.value:
                possible_geos.append('N_Shore')
                possible_geos.append('S_Shore')
            elif target == Geo.shores_s.value:
                possible_geos.append('S_Shore')
            elif target == Geo.shores_n.value:
                possible_geos.append('N_Shore')
            elif target == Geo.islands_shores.value:
                possible_geos.append('Island')
                possible_geos.append('N_Shore')
                possible_geos.append('S_Shore')
        else:
            possible_geos.append(target)

        if geo in possible_geos:
            match = True

    return match


def probe_class_condition(config, annotation_dict):
    target = config.annotation.probe_class
    probe_class = annotation_dict[AnnotationKey.probe_class.value]

    match = False
    if target == ProbeClass.any.value:
        match = True
    else:
        keys_preset = [x.value for x in ProbeClass]
        if target in keys_preset:
            if target is ProbeClass.class_ab.value:
                classes = [ProbeClass.class_a.value,
                           ProbeClass.class_b.value]
                if probe_class in classes:
                    match = True
            if target == probe_class:
                match = True
        else:
            if target == probe_class:
                match = True

    return match


def cpg_name_condition(annotation_dict):
    cpg = annotation_dict[AnnotationKey.cpg.value]
    if len(cpg) > 0:
        return True
    else:
        return False


def check_conditions(config, annotation_dict):
    match = False
    if exclude_condition(config, annotation_dict):
        if cross_reactive_condition(config, annotation_dict):
            if snp_condition(config, annotation_dict):
                if chromosome_condition(config, annotation_dict):
                    if gene_region_condition(config, annotation_dict):
                        if geo_condition(config, annotation_dict):
                            if probe_class_condition(config, annotation_dict):
                                if cpg_name_condition(annotation_dict):
                                    match = True
    return match
