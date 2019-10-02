import xlrd
import os
import logging
from enum import Enum

export_path = "../UnityProject/TableExportTest/Assets"

class SheetInfo:
    sheet_name = ""
    file_name = ""
    table_name = ""
    tid_list = []
    name_tid_dic = {}
    prop_dic = {}
    sheet_data: xlrd.sheet.Sheet
    line_data = {}

    def __init__(self):
        return


class Enum_CellType(Enum):
    INT = 0
    FLOAT = 1
    STRING = 2
    ENUM = 3
    NAME = 4
    TID = 5
    LINK = 6


class PropInfo:
    p_name = ""
    p_type = Enum_CellType
    p_enumIdxDic = {}  # 枚举代码名称对应的索引号
    p_enumNameDic = {}  # 枚举的中文名称对应的代码名称
    p_link_sheet = ""


class PropBox(PropInfo):
    p_value_list = []

    def __init__(self, prop_info: PropInfo):
        p_name = prop_info.p_name
        p_type = prop_info.p_type
        p_enumIdxDic = prop_info.p_enumIdxDic
        p_enumNameDic = prop_info.p_enumNameDic
        p_link_sheet = prop_info.p_link_sheet


def parse_enum_def(enum_content_list, idx_dic, name_dic):
    """

    :param enum_content_list:
    :param idx_dic:
    :param name_dic:
    :return:
    """
    idx = 0
    for v in enum_content_list:
        line_content_l = v.split(':')
        code_name = line_content_l[0]
        text_name = line_content_l[1]
        idx_dic[code_name] = idx
        name_dic[text_name] = code_name
        idx += 1
    return


def get_table_name(sheet_data: xlrd.sheet.Sheet):
    """
    直接获取table_name。表格的第一行第一列
    :param sheet_data:
    :return:
    """
    cell_content = sheet_data.cell_value(0, 0)
    return cell_content.splitlines()[0]


def get_tid_list(sheet_data: xlrd.sheet.Sheet):
    """
    获取tid列表
    :param sheet_data:
    :return:
    """
    value_list = sheet_data.col_values(0, 2, sheet_data.nrows)
    for i in range(0, len(value_list)):
        value_list[i] = int(value_list[i])
    return value_list


def get_head_line(sheet_data: xlrd.sheet.Sheet):
    """
    获取第一行cell数据列表
    :param sheet_data:
    :return:
    """
    return sheet_data.row_values(0, 0, sheet_data.ncols)


def get_name_to_tid_dic(sheet_data: xlrd.sheet.Sheet):
    """
    获取名称到tid的映射，如果没有名称则返回空字典
    :param sheet_data:
    :return:
    """
    head_values = get_head_line(sheet_data)
    ret_dic = {}
    tid_list = get_tid_list(sheet_data)
    for cell_value in head_values:
        type = get_prop_type(cell_value)
        if type is Enum_CellType.NAME:
            col = head_values.index(cell_value)
            name_list = sheet_data.col_values(col, 2, sheet_data.nrows)
            for i in range(0, len(name_list)):
                ret_dic[name_list[i]] = tid_list[i]
    return ret_dic


def get_prop_type(cell_vale):
    """
    解析属性类型
    :param cell_vale: 单元格value
    :return:
    """
    type_string = cell_vale.splitlines()[1]
    return tag_to_type(type_string)


def get_property_name(sheet_data: xlrd.sheet.Sheet, idx):
    """

    :param line_values:
    :param idx:
    :return:
    """
    head_line = get_head_line(sheet_data)
    return head_line[idx].splitlines()[0]


def parse_head(sheet_data: xlrd.sheet.Sheet):
    """
    解析头信息
    :param sheet_data:
    :return:

    """
    first_line_values = get_head_line(sheet_data)
    result = {}
    for v in first_line_values:
        content_list = v.splitlines()
        list_length = len(content_list)
        if list_length < 2:
            raise Exception("数据格式异常")
        v_name = content_list[0]
        v_type = tag_to_type(content_list[1])
        p_obj = PropInfo()
        p_obj.p_name = v_name
        p_obj.p_type = v_type
        if v_type == Enum_CellType.ENUM:
            idx_dic = {}
            name_dic = {}
            parse_enum_def(content_list[2:], idx_dic, name_dic)
            p_obj.p_enumIdxDic = idx_dic
            p_obj.p_enumNameDic = name_dic
        elif v_type == Enum_CellType.LINK:
            p_obj.p_link_sheet = content_list[2]
        result[v_name] = p_obj
    return result


def parse_sheet(sheet_dic, key):
    curr_sheet_info = sheet_dic[key]
    sheet_data = curr_sheet_info.sheet_data
    line_data_dic = {}
    for i in range(2, sheet_data.nrows):
        line_data = {}
        line_values = sheet_data.row_values(i, 0, sheet_data.ncols)
        tid = int(line_values[0])
        for j in range(1, len(line_values)):
            value = line_values[j]
            property_name = get_property_name(sheet_data, j)
            prop_box = line_data.get(property_name, None)
            if prop_box is None:
                prop_info = curr_sheet_info.prop_dic[property_name]
                prop_box = PropBox(prop_info)
                line_data[property_name] = prop_box;
            if prop_box.p_type is Enum_CellType.TID:
                prop_box.p_value_list.append(int(value))
            elif prop_box.p_type is Enum_CellType.ENUM:
                code_name = prop_info.p_enumNameDic[value]
                enum_idx = prop_info.p_enumIdxDic[code_name]
                prop_box.p_value_list.append(int(enum_idx))
            elif prop_box.p_type is Enum_CellType.LINK:
                link_sheet_info = sheet_dic[prop_box.p_link_sheet]
                link_tid = link_sheet_info.name_tid_dic[value]
                prop_box.p_value_list.append(int(link_tid))
            else:
                prop_box.p_value_list.append(value)
        line_data_dic[tid] = line_data
    curr_sheet_info.line_data = line_data_dic
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
    if tag == "[Enum]":
        return Enum_CellType.ENUM
    if tag == "[Link]":
        return Enum_CellType.LINK
    raise Exception("找不到tag对应的类型" + tag)


def process_tables():
    table_list = []
    for root, dirs, files in os.walk("Tables"):
        for file in files:
            if file.endswith(".xlsx") and not file.startswith("~$"):
                table_list.append(root + "/" + file)

    sheet_name_dic = {}
    table_name_dic = {}
    # 预解析表，用于检查sheet名，table名是否重复以及表关联信息缓存
    for table in table_list:
        table_data = xlrd.open_workbook(table)
        sheet_names = table_data.sheet_names()
        for sheet_name in sheet_names:
            r = sheet_name_dic.get(sheet_name, None)
            if r is None:
                sheet_data = table_data.sheet_by_name(sheet_name)
                if sheet_data.nrows > 2:
                    table_name = get_table_name(sheet_data)
                    r1 = table_name_dic.get(table_name, None)
                    if r1 is None:
                        sheet_info = SheetInfo()
                        sheet_info.sheet_name = sheet_name
                        sheet_info.file_name = table
                        sheet_info.table_name = table_name
                        sheet_info.sheet_data = sheet_data
                        tid_list = get_tid_list(sheet_data)
                        sheet_info.tid_list = tid_list
                        sheet_info.name_tid_dic = get_name_to_tid_dic(sheet_data)
                        sheet_info.prop_dic = parse_head(sheet_data)
                        sheet_name_dic[sheet_name] = sheet_info
                        table_name_dic[table_name] = sheet_info
                    else:
                        print(
                            "table名称重复!! sheet:" + r1.sheet_name + " & " + sheet_name + " 文件：" + r1.file_name + " & " + table)
            else:
                print(
                    "sheet名称重复!! sheet:" + r1.sheet_name + "&" + sheet_name + " 文件：" + r1.file_name + " & " + table)

    # 解析表数据
    for key in sheet_name_dic.keys():
        parse_sheet(sheet_name_dic, key)

    full_path = export_path+"/TableExport"
    if os.path.exists(full_path):
        __import__('shutil').rmtree(full_path)
    os.makedirs(full_path)

    file = open(full_path + "/test.cs", 'x')
    file.write("AAAABBBBsss")
    file.close()


    return
