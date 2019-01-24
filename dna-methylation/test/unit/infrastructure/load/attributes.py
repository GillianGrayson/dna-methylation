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
            types={}
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


    def test_load_attributes_dict_num_elems(self):
        attributes_dict = load_attributes_dict(self.config)
        self.assertEqual(len(attributes_dict['age']), 729)


    def test_load_attributes_dict_num_keys(self):
        attributes_dict = load_attributes_dict(self.config)
        self.assertEqual(len(list(attributes_dict.keys())), 2)


    def test_load_attributes_dict_age_range(self):
        attributes_dict = load_attributes_dict(self.config)
        self.assertEqual(max(attributes_dict['age']) - min(attributes_dict['age']), 80)


if __name__ == '__main__':
    unittest.main()