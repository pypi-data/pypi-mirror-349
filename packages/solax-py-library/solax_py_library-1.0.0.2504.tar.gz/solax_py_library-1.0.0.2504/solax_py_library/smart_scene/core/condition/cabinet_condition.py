from collections import defaultdict

from solax_py_library.smart_scene.core.condition.base import BaseCondition
from solax_py_library.smart_scene.types.condition import CabinetConditionItemData, CabinetConditionType
from solax_py_library.device.types.alarm import AlarmLevel


class CabinetCondition(BaseCondition):
    def __init__(self, update_value_function, **kwargs):
        super().__init__(update_value_function, **kwargs)
        self.value = defaultdict(
            lambda: {
                "soc": 0,
                "alarm_level": {
                    AlarmLevel.EMERGENCY: False,
                    AlarmLevel.NORMAL: False,
                    AlarmLevel.TIPS: False,
                },
            }
        )

    def meet_func(self, data: CabinetConditionItemData, ctx):
        if not self.value:
            return False
        cabinet = ctx["cabinet"] or []
        for cabinet_sn in cabinet:
            if data.childType == CabinetConditionType.cabinetSoc:
                if self.value[cabinet_sn]["soc"] is None:
                    return False
                if data.childData.function.function()(
                    compare_value=self.value[cabinet_sn]["soc"],
                    base_value=data.childData.data[0],
                ):
                    return True
            elif data.childType == CabinetConditionType.cabinetAlarm:
                if self.value[cabinet_sn]["alarm_level"][data.childData.data[0]]:
                    return True
        return False
