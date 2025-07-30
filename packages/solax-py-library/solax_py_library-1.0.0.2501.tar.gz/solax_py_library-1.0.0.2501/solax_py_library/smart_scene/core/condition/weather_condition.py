
class WeatherCondition(BaseCondition):
    def __init__(self, smart_scene_service):
        super().__init__(smart_scene_service)
        self.type = IF_ELE_TYPE
        self.buy = True
        self.child_type_list = ["irradiance", "temperature"]
        self.value = {}
        self.unit = ""
        self.meet_func = self.meet_weather_condition

    def update_value(
        self,
    ):
        self.value = self.smart_scene_service.get_weather_data_from_redis()

    def meet_weather_condition(self, data: WeatherConditionItemData, ctx):
        if not self.value:
            return False
        child_data = data.childData
        child_type = data.childType
        function_value = child_data.function
        data_value = child_data.data
        nearest_time, right_time = self.smart_scene_service.get_rounded_times()
        if nearest_time not in self.value["timeList"]:
            time_now = right_time
        else:
            time_now = nearest_time
        index = self.value["timeList"].index(time_now)
        app_log.info(
            f"最近时间点为: {nearest_time}, 右侧时间点为: {right_time}, 数组索引为: {index}"
        )
        if child_type == WeatherConditionType.irradiance:
            return self.meet_func_irradiance(function_value, data_value, index)
        elif child_type == WeatherConditionType.temperature:
            app_log.info(f"当前实际值为: {self.value[child_type]['valueList'][index]}")
            return self.smart_scene_service.compare_the_magnitudes(
                function_value,
                self.value[child_type]["valueList"][index],
                data_value[0],
            )
        return False

    def meet_func_irradiance(self, function_value, data_value, index):
        """太阳辐照度判断"""
        irradiance = data_value[0]
        duration = data_value[1]
        meet_num = 0
        meet_flag = False
        if duration == 0:
            meet_flag = True
        elif duration > 24:
            pass
        else:
            # 1. 保证累计duration个小时大于200,
            for value in self.value["irradiance"]["valueList"]:
                if value > 200:
                    meet_num += 1
                    if meet_num >= duration * 4:
                        meet_flag = True
                        break
        if not meet_flag:
            return False
        # 2. 再判断当前太阳辐照度
        return self.smart_scene_service.compare_the_magnitudes(
            function_value, self.value["irradiance"]["valueList"][index], irradiance
        )
