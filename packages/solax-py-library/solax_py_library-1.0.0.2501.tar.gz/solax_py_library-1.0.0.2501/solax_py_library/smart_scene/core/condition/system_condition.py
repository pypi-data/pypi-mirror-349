

class SystemCondition(BaseCondition):
    def __init__(self, smart_scene_service):
        super().__init__(smart_scene_service)
        self.type = IF_ELE_TYPE
        self.value = {}
        self.meet_func = self.meet_system_condition

    def update_value(self):
        overview_statistic_data = (
            self.smart_scene_service.redis_service.get_overview_statistic_data()
        )
        self.value["grid_active_power"] = overview_statistic_data[8]
        self.value["system_soc"] = overview_statistic_data[16]

    def meet_system_condition(self, data: SystemConditionItemData, ctx):
        if not self.value:
            return False
        child_data = data.childData
        function_value = child_data.function
        compare_value = None
        app_log.info(self.value)
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
        return self.smart_scene_service.compare_the_magnitudes(
            function_value,
            compare_value=abs(compare_value),
            base_value=child_data.data[0],
        )

