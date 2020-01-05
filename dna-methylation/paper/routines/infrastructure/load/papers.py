from paper.routines.infrastructure.path import get_data_path


def load_papers_dict():
    fn = f'{get_data_path()}/draft/intersection'

    papers_dict = {}
    papers = ['inoshita', 'singmann', 'yousefi']
    for paper in papers:

        fn_curr = f'{fn}/{paper}.txt'
        f = open(fn_curr)
        cpgs = f.read().splitlines()
        f.close()
        papers_dict[paper] = {}
        for cpg in cpgs:
            papers_dict[paper][cpg] = 1

    return papers_dict
