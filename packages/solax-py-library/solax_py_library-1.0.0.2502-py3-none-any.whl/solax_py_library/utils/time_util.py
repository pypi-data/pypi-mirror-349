def trans_str_time_to_index(now_time, minute=15):
    """将时间按照minute切换为索引，时间格式为 %H-%M"""
    time_list = [int(i) for i in now_time.split(":")]
    time_int = time_list[0] * 4 + time_list[1] // minute
    return time_int
