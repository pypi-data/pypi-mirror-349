import copy
import struct
from typing import List


def unpack(data: List, data_format, reversed=False):
    """
    :param data: 数据字节, 入参均是由modbus读取到的list[uint16]进行转换
    :param data_format:  数据格式
    :param reversed:  是否翻转大小端
    """
    cur_data = copy.deepcopy(data)
    data_format = data_format.lower()
    format_map = {
        "int8": "bb",
        "uint8": "BB",
        "int16": "h",
        "uint16": "H",
        "int32": "i",
        "uint32": "I",
        "int64": "q",
        "uint64": "Q",
        "float": "f",
    }
    if data_format not in format_map:
        raise Exception("暂不支持")
    pack_str = ("<" if reversed else ">") + "H" * len(cur_data)
    to_pack_data = struct.pack(pack_str, *cur_data)
    struct_format = ("<" if reversed else ">") + format_map[data_format]
    return struct.unpack(struct_format, to_pack_data)
