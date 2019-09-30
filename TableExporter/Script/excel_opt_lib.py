import xlrd
import os


def process_tables():
    table_list = []
    for root, dirs, files in os.walk("Tables"):
        for file in files:
            print(file)
            if file.endswith(".xlsx"):
                table_list.append(root + "/" + file)
    for table in table_list:
        table_data = xlrd.open_workbook(table)
        sheet_names = table_data.sheet_names()
        for sheet_name in sheet_names:
            sheet = table_data.sheet_by_name(sheet_name)
            print(sheet.ncols)

    return
