from lib.infrastucture.load.annotations import *
from lib.infrastucture.load.excluded import *
from lib.infrastucture.load.attributes import *
from lib.config.annotations.subset import *
from lib.config.attributes.subset import *


class Config:

    def __init__(self,
                 data,
                 setup,
                 annotations,
                 attributes,
                 target
                 ):

        self.data = data
        self.setup = setup
        self.annotations = annotations
        self.attributes = attributes
        self.target = target

        self.cpg_gene_dict = {}
        self.cpg_bop_dict = {}
        self.gene_cpg_dict = {}
        self.gene_bop_dict = {}
        self.bop_cpg_dict = {}
        self.bop_gene_dict = {}

        self.cpg_list = []
        self.cpg_dict = {}
        self.cpg_data = []

        self.gene_list = []
        self.gene_dict = {}
        self.gene_data = []

        self.bop_list = []
        self.bop_dict = {}
        self.bop_data = []

        self.attributes_indexes = []

        self.excluded = load_excluded(self)

        self.annotations_dict = load_annotations_dict(self)
        subset_annotations(self)

        self.attributes_dict = load_attributes_dict(self)
        self.attributes_indexes = get_indexes(self)
        subset_attributes(self)
        self.cells_dict = load_cells_dict(self)
        subset_cells(self)
