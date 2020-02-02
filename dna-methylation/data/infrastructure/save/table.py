import pandas as pd
import pickle


def save_table_dict_xlsx(fn, table_dict):
    fn_xlsx = fn
    df = pd.DataFrame(table_dict)
    writer = pd.ExcelWriter(fn_xlsx, engine='xlsxwriter')
    writer.book.use_zip64()
    df.to_excel(writer, index=False)
    writer.save()


def save_table_dict_pkl(fn, table_dict):
    fn_pkl = fn
    f = open(fn_pkl, 'wb')
    pickle.dump(table_dict, f, pickle.HIGHEST_PROTOCOL)
    f.close()
