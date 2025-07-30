from collections import defaultdict

from solax_py_library.smart_scene.core.condition.base import BaseCondition
from solax_py_library.smart_scene.types.condition import CabinetConditionItemData
from solax_py_library.device.types.alarm import AlarmLevel


class CabinetCondition(BaseCondition):
    def __init__(self, **kwargs):
        super().__init__()
        self.value = defaultdict(
            lambda: {
                "soc": None,
                "alarm_level": {
                    AlarmLevel.EMERGENCY: False,
                    AlarmLevel.NORMAL: False,
                    AlarmLevel.TIPS: False,
                },
            }
        )
        self.redis_service = kwargs.get("redis_service")
        self.db_service = kwargs.get("db_service")

    def update_value(self):
        ...

    def meet_func(self, data: CabinetConditionItemData, ctx):
        ...
