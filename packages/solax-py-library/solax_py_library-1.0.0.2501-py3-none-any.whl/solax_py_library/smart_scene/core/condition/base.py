class BaseCondition(object):
    def __init__(self):
        # 子条件类型
        self.child_type_list = []
        # 各子条件的值
        self.value = {}
        # 判断是否满足条件的子条件-判断函数的映射
        self.meet_func_dict = {}

    def update_value(self):
        """更新条件值"""
        ...
