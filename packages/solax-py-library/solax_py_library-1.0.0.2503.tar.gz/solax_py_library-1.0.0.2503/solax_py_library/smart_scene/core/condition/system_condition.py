from solax_py_library.smart_scene.core.condition.base import BaseCondition
from solax_py_library.smart_scene.types.condition import (
    SystemConditionItemData,
    SystemConditionType,
)


class SystemCondition(BaseCondition):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.redis_service = kwargs.pop("redis_service")

    def update_value(self):
        overview_statistic_data = self.redis_service.get_overview_statistic_data()
        self.value["grid_active_power"] = overview_statistic_data[8]
        self.value["system_soc"] = overview_statistic_data[16]

    def meet_system_condition(self, data: SystemConditionItemData, ctx):
        if not self.value:
            return False
        child_data = data.childData
        function_value = child_data.function
        compare_value = None
        if data.childType == SystemConditionType.systemExportPower:
            compare_value = self.value["grid_active_power"]
            if compare_value < 0:
                return False
        elif data.childType == SystemConditionType.systemImportPower:
            compare_value = self.value["grid_active_power"]
            if compare_value > 0:
                return False
        elif data.childType == SystemConditionType.systemSoc:
            compare_value = self.value["system_soc"]
        if compare_value is None:
            return False
        return function_value.function()(
            compare_value=abs(compare_value), base_value=child_data.data[0]
        )
