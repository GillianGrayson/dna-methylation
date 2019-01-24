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


    def test_load_annotations_dict_num_elems(self):
        annotations_dict = load_annotations_dict(self.config)
        self.assertEqual(len(annotations_dict['ID_REF']), 300)


    def test_load_annotations_dict_num_keys(self):
        annotations_dict = load_annotations_dict(self.config)
        self.assertEqual(len(list(annotations_dict.keys())), 10)


    def test_load_annotations_dict_num_chrs(self):
        annotations_dict = load_annotations_dict(self.config)
        self.assertEqual(len(set(annotations_dict['CHR'])), 11)


    def test_load_annotations_dict_num_bops(self):
        annotations_dict = load_annotations_dict(self.config)
        self.assertEqual(len(set(annotations_dict['BOP'])), 82)


if __name__ == '__main__':
    unittest.main()