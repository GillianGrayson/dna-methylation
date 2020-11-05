
def save_list(l, path):
    with open(f'{path}.txt', 'w') as f:
        for item in l:
            f.write("%s\n" % item)