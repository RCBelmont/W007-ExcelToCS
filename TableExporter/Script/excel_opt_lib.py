import xlrd
import os
from enum import Enum


class SheetInfo:
    sheet_name = ""
    file_name = ""
    sheet_data = xlrd.sheet.Sheet

    def __init__(self):
        return


class Enum_CellType(Enum):
    INT = 0
    FLOAT = 1
    STRING = 2
    ENUM = 3
    NAME = 4
    TID = 5


class PropertyInfo:
    p_name = ""
    p_type = Enum_CellType
    p_isList = False
    p_enumDic = {}


def parse_sheet(sheetDic, sheetInfo):
    sheetProperty = {}
    sheetData = sheetInfo.sheet_data
    rowNum = sheetData.nrows
    ##解析头部信息
    if rowNum >= 2:
        headValues = sheetData.row_values(0, 0, sheetData.ncols)
        for v in headValues:
            lines = v.splitlines()
            print(tag_to_type(lines[1]))
    return


def tag_to_type(tag):
    if tag == "[Int]":
        return Enum_CellType.INT
    if tag == "[Float]":
        return Enum_CellType.FLOAT
    if tag == "[Name]":
        return Enum_CellType.NAME
    if tag == "[Tid]":
        return Enum_CellType.TID
    if tag == "[String]":
        return Enum_CellType.STRING
    raise Exception("抛出一个异常")


def process_tables():
    table_list = []
    for root, dirs, files in os.walk("Tables"):
        for file in files:
            if file.endswith(".xlsx"):
                table_list.append(root + "/" + file)

    sheet_info_dic = {}

    for table in table_list:
        table_data = xlrd.open_workbook(table)
        sheet_names = table_data.sheet_names()
        for sheet_name in sheet_names:
            r = sheet_info_dic.get(sheet_name, None)
            if r == None:
                sheet = table_data.sheet_by_name(sheet_name)
                sheetInfo = SheetInfo()
                sheetInfo.sheet_name = sheet_name
                sheetInfo.file_name = table
                sheetInfo.sheet_data = sheet
                sheet_info_dic[sheet_name] = sheetInfo
            else:
                print("表名重复：" + r.sheet_name + " 文件：" + r.file_name + " & " + table)

    for key in sheet_info_dic.keys():
        parse_sheet(sheet_info_dic, sheet_info_dic[key])

    return
