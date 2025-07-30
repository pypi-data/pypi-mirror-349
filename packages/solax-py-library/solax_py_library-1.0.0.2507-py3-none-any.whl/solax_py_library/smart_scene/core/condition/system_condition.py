from solax_py_library.smart_scene.core.condition.base import BaseCondition
from solax_py_library.smart_scene.types.condition import (
    SystemConditionItemData,
    SystemConditionType,
)


class SystemCondition(BaseCondition):
    def __init__(self, update_value_function, **kwargs):
        super().__init__(update_value_function, **kwargs)
        self.grid_active_power = None
        self.system_soc = None

    def meet_system_condition(self, data: SystemConditionItemData, ctx):
        if not self.value:
            return False
        child_data = data.childData
        function_value = child_data.function
        compare_value = None
        if data.childType == SystemConditionType.systemExportPower:
            compare_value = self.grid_active_power
            if compare_value < 0:
                return False
        elif data.childType == SystemConditionType.systemImportPower:
            compare_value = self.grid_active_power
            if compare_value > 0:
                return False
        elif data.childType == SystemConditionType.systemSoc:
            compare_value = self.system_soc
        if compare_value is None:
            return False
        return function_value.function()(
            compare_value=abs(compare_value), base_value=child_data.data[0]
        )
