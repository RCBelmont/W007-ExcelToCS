import xlrd
import os
import logging
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
    p_value_l = []
    p_enumIdxDic = {}  # 枚举代码名称对应的索引号
    p_enumNameDic = {}  # 枚举的中文名称对应的代码名称


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


def get_property_name(line_values, idx):
    """

    :param line_values:
    :param idx:
    :return:
    """
    return line_values[idx].splitlines()[0]


def parse_head(first_line_values):
    """
    解析头信息
    :param first_line_values:
    :return:

    """
    result = {}
    for v in first_line_values:
        content_list = v.splitlines()
        list_length = len(content_list)
        if list_length < 2:
            raise Exception("数据格式异常")
        v_name = content_list[0]
        v_type = tag_to_type(content_list[1])
        p_obj = PropertyInfo()
        p_obj.p_name = v_name
        p_obj.p_type = v_type
        if v_type == Enum_CellType.ENUM:
            idx_dic = {}
            name_dic = {}
            parse_enum_def(content_list[2:], idx_dic, name_dic)
            p_obj.p_enumIdxDic = idx_dic
            p_obj.p_enumNameDic = name_dic
        result[v_name] = p_obj
    return result


def parse_sheet(sheet_dic, sheet_info):
    sheet_property = {}
    sheet_data = sheet_info.sheet_data
    row_num = sheet_data.nrows
    # 解析头部信息
    if row_num >= 2:
        first_line_values = sheet_data.row_values(0, 0, sheet_data.ncols)
        try:
            head_info_dic = parse_head(first_line_values)
            table_data = {}
            for i in range(2, row_num):
                line_values = sheet_data.row_values(i, 0, sheet_data.ncols)
                line_data = {}
                tid = None
                # 解析每一行信息
                for j in range(0, sheet_data.ncols):
                    p_name = get_property_name(first_line_values, j)
                    head_info = head_info_dic[p_name]

                    if head_info.p_type == Enum_CellType.TID:
                        tid = int(line_values[j])
                    # 回去当前名称的数据是否解析过，用于处理列表的情况
                    data = line_data.get(p_name, None)
                    if data is None:
                        # 创建一个新的数据对象，将表头对象的数据拷贝过来（类似继承）
                        data = PropertyInfo()
                        data.p_name = head_info.p_name
                        data.p_type = head_info.p_type
                        data.p_enumNameDic = head_info.p_enumNameDic
                        data.p_enumIdxDic = head_info.p_enumIdxDic
                        if data.p_type == Enum_CellType.ENUM:
                            enum_tex_name = line_values[j]
                            enum_code_name = head_info.p_enumNameDic[enum_tex_name]
                            enum_idx = head_info.p_enumIdxDic[enum_code_name]
                            data.p_value_l.append(enum_idx)
                        else:
                            data.p_value_l.append(line_values[j])
                        line_data[data.p_name] = data
                    else:
                        if data.p_type == Enum_CellType.ENUM:
                            enum_tex_name = line_values[j]
                            enum_code_name = head_info.p_enumNameDic[enum_tex_name]
                            enum_idx = head_info.p_enumIdxDic[enum_code_name]
                            data.p_value_l.append(enum_idx)
                        else:
                            data.p_value_l.append(line_values[j])
                # 将行数据放到tid为key的字典中
                if tid is not None:
                    table_data[tid] = line_data
        except Exception as err:
            logging.exception(err)
            print(sheet_info.file_name)
        except BaseException as e:
            print(e)

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
    raise Exception("找不到tag对应的类型" + tag)


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
                sheet_info = SheetInfo()
                sheet_info.sheet_name = sheet_name
                sheet_info.file_name = table
                sheet_info.sheet_data = sheet
                sheet_info_dic[sheet_name] = sheet_info
            else:
                print("表名重复：" + r.sheet_name + " 文件：" + r.file_name + " & " + table)

    for key in sheet_info_dic.keys():
        parse_sheet(sheet_info_dic, sheet_info_dic[key])

    return
