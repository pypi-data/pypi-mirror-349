from datetime import datetime

from solax_py_library.smart_scene.core.condition.base import BaseCondition
from solax_py_library.smart_scene.types.condition import (
    DateConditionItemData,
    DateConditionType,
)


class DateCondition(BaseCondition):
    def __init__(self, update_value_function, **kwargs):
        super().__init__(update_value_function, **kwargs)

    def _update_value(self):
        """获取time 类型需要的数据"""
        now = datetime.now()
        self.hour = now.hour
        self.minute = now.minute

    def meet_func(self, data: DateConditionItemData, ctx):
        if data.childType == DateConditionType.time:
            date = data.childData.data[0]
            hour, minute = date.split(":")
            if int(hour) == self.hour and int(minute) == self.minute:
                return True
        return False
