import unittest
from definitions import ROOT_DIR
from library.model.main import *

class TestLoadAnnotations(unittest.TestCase):

    def setUp(self):
        target = 'age'
        data = Data(
            name='cpg_beta',
            type=DataType.cpg,
            path=ROOT_DIR + '\\test',
            base='fixtures'
        )

        setup = Setup(
            experiment='',
            task='',
            method='',
            params={}
        )

        annotations = Annotations(
            name='annotations',
            exclude=CommonTypes.none.value,
            cross_reactive=CrossReactive.exclude.value,
            snp=SNP.exclude.value,
            chr=Chromosome.non_gender.value,
            gene_region=GeneRegion.yes.value,
            geo=CommonTypes.any.value,
            probe_class=CommonTypes.any.value
        )

        observables = Observables(
            file_name='observables',
            types={'gender': 'vs'}
        )

        cells = Cells(
            file_name='cells',
            types=CommonTypes.any.value
        )

        attributes = Attributes(
            observables=observables,
            cells=cells
        )

        self.config = Config(
            data=data,
            setup=setup,
            annotations=annotations,
            attributes=attributes,
            target=target
        )


    def test_pass_indexes_num_elems(self):
        self.config.attributes.observables.types = {'gender': CommonTypes.any.value}
        self.config.attributes_dict = load_attributes_dict(self.config)
        indexes = pass_indexes(self.config, 'gender', CommonTypes.any.value, CommonTypes.any.value)
        self.assertEqual(len(indexes), 729)


    def test_pass_indexes_num_f(self):
        self.config.attributes.observables.types = {'gender': 'F'}
        self.config.attributes_dict = load_attributes_dict(self.config)
        indexes = pass_indexes(self.config, 'gender', 'F', CommonTypes.any.value)
        self.assertEqual(len(indexes), 388)


    def test_pass_indexes_num_m(self):
        self.config.attributes.observables.types = {'gender': 'M'}
        self.config.attributes_dict = load_attributes_dict(self.config)
        indexes = pass_indexes(self.config, 'gender', 'M', CommonTypes.any.value)
        self.assertEqual(len(indexes), 341)


    def test_get_indexes_num_elems(self):
        self.config.attributes.observables.types = {'gender': CommonTypes.any.value}
        self.config.attributes_dict = load_attributes_dict(self.config)
        indexes = get_indexes(self.config)
        self.assertEqual(len(indexes), 729)


    def test_get_indexes_num_f(self):
        self.config.attributes.observables.types = {'gender': 'F'}
        self.config.attributes_dict = load_attributes_dict(self.config)
        indexes = get_indexes(self.config)
        self.assertEqual(len(indexes), 388)


    def test_get_indexes_num_m(self):
        self.config.attributes.observables.types = {'gender': 'M'}
        self.config.attributes_dict = load_attributes_dict(self.config)
        indexes = get_indexes(self.config)
        self.assertEqual(len(indexes), 341)


if __name__ == '__main__':
    unittest.main()