from datetime import datetime

from solax_py_library.smart_scene.core.condition.base import BaseCondition
from solax_py_library.smart_scene.types.condition import DateConditionItemData, DateConditionType


class DateCondition(BaseCondition):
    def __init__(self):
        super().__init__()
        self.value = {}

    def update_value(self):
        """获取time 类型需要的数据"""
        now = datetime.now()
        self.hour = now.hour
        self.minute = now.minute

    def meet_func(self, data: DateConditionItemData, ctx):
        if data.childType == DateConditionType.time:
            """判断是否满足日期时间类条件"""
            date = data.childData.data[0]
            hour = int(date.split(":")[0])
            minute = int(date.split(":")[1])
            if hour == self.hour and minute == self.minute:
                return True
        return False
