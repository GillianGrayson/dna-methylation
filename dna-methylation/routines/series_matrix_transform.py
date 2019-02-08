import re
import pandas as pd


def convert_header(input_name, output_name):
    content = []
    with open(input_name) as f:
        for line in f:
            if line == "!series_matrix_table_begin":
                break
            content.append(line)

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
        res.append(cur)

    res_dict = {}
    for col_id in range(0, len(res)):
        res_dict[res[col_id][0]] = res[col_id][1::]

    df = pd.DataFrame(res_dict)
    writer = pd.ExcelWriter(output_name, engine='xlsxwriter')
    df.to_excel(writer, index=False)
    writer.save()

input_name = 'series_matrix.txt'
output_name = 'observables.xlsx'
convert_header(input_name, output_name)

