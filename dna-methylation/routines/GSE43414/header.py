import re
import pandas as pd
import numpy as np


def convert_header(input_name, output_name):
    content = []
    with open(input_name) as f:
        for line in f:
            if line == "!series_matrix_table_begin":
                break
            content.append(line)

    df = pd.DataFrame()
    res = []
    for i, s in enumerate(content):
        if s[:8] != "!Sample_":
            continue
        s = s[8:]
        cur = re.findall(r'[^"\s]\S*|".+?"', s)
        cur = [x.strip('\"') for x in cur]

        if s[:16] == "characteristics_":
            column_name = re.findall(r'[^:]+', cur[1])[0]
            l = len(column_name) + 1
            cur = [x[l:].strip(" ") for x in cur]
            cur[0] = column_name

        cur = [x.replace(" ", "_") for x in cur]
        cur = [x[:-1] if len(x) > 0 and x[-1] == '.' else x for x in cur]

        res.append(cur)
        df[cur[0]] = cur[1:]

    for col_name in df.columns:
        cur = df[col_name].drop_duplicates()
        if len(cur) == 1:
            df = df.drop(col_name, axis=1)

    # subjects = list(df['title'])
    # subjects_corr = list(np.loadtxt('E:/YandexDisk/Work/pydnameth/GSE55763/subjects.txt', dtype=str))
    #
    # indexes = [subjects.index(x) for x in subjects_corr]
    #
    # for col_name in df.columns:
    #     cur = list(df[col_name])
    #     corr_cur = [cur[i] for i in indexes]
    #     df[col_name] = corr_cur

    df.to_csv(output_name + '.txt', sep="\t", index=False)
    df.to_csv(output_name + '.csv', sep=",", index=False)
    print
    res


input_name = "D:/YandexDisk/Work/pydnameth/GSE61256/tmp.txt"
output_name = "D:/YandexDisk/Work/pydnameth/GSE61256/tmp_1.txt"
convert_header(input_name, output_name)

