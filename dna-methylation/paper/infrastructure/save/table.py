import pandas as pd


def save_table_dict_xlsx(fn, table_dict):
    fn_xlsx = fn + '.xlsx'
    df = pd.DataFrame(table_dict)
    writer = pd.ExcelWriter(fn_xlsx, engine='xlsxwriter')
    writer.book.use_zip64()
    df.to_excel(writer, index=False)
    writer.save()