from source.config.annotation.types import *


class Annotation:

    def __init__(self,
                 name='annotation',
                 exclude=Exclude.none.value,
                 cross_reactive=CrossReactive.any.value,
                 snp=SNP.any.value,
                 chr=Chromosome.any.value,
                 gene_region=GeneRegion.any.value,
                 geo=Geo.any.value,
                 probe_class=ProbeClass.any.value
                 ):
        self.name = name
        self.exclude = exclude
        self.cross_reactive = cross_reactive
        self.snp = snp
        self.chr = chr
        self.gene_region = gene_region
        self.geo = geo
        self.probe_class = probe_class

    def __str__(self):
        return 'ex(' + self.exclude + ')' + '_' + \
               'CR(' + self.cross_reactive + ')' + '_' + \
               'SNP(' + self.snp+ ')' + '_' + \
               'chr(' + self.chr + ')' + '_' + \
               'gene(' + self.gene_region + ')' + '_' + \
               'geo(' + self.geo + ')' + '_' + \
               'class(' + self.probe_class + ')'
