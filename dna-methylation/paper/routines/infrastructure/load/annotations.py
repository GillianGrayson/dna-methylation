from paper.routines.infrastructure.path import get_data_path


def load_annotations_dict():
    fn = f'{get_data_path()}/GSE87571/annotations.txt'

    f = open(fn)
    key_line = f.readline()
    keys = key_line.split('\t')
    keys = [x.rstrip() for x in keys]
    keys = keys[1::]

    annotations_dict = {}
    for key in keys:
        annotations_dict[key] = {}

    for line in f:
        values = line.split('\t')
        cpg = values[0]
        for key_id, key in enumerate(keys):
            values_for_key = values[key_id + 1].rstrip()
            annotations_dict[key][cpg] = values_for_key
    f.close()

    return annotations_dict