from solax_py_library.smart_scene.core.condition.base import BaseCondition
from solax_py_library.smart_scene.types.condition import (
    WeatherConditionItemData,
    WeatherConditionType,
)
from solax_py_library.utils.cloud_client import CloudClient
from solax_py_library.utils.time_util import get_rounded_times


class WeatherCondition(BaseCondition):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cloud_url = kwargs.pop("cloud_url")
        self.sn = kwargs.pop("ems_sn")
        self.secret = kwargs.pop("secret")
        self.client = CloudClient(base_url=self.cloud_url)

    def update_value(self):
        self.value = self.client.get_weather_data_from_redis()

    def meet_weather_condition(self, data: WeatherConditionItemData, ctx):
        if not self.value:
            return False
        child_data = data.childData
        child_type = data.childType
        function_value = child_data.function
        data_value = child_data.data
        nearest_time, right_time = get_rounded_times()
        if nearest_time not in self.value["timeList"]:
            time_now = right_time
        else:
            time_now = nearest_time
        index = self.value["timeList"].index(time_now)
        if child_type == WeatherConditionType.irradiance:
            return function_value.function()(function_value, data_value, index)
        elif child_type == WeatherConditionType.temperature:
            return function_value.function()(
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
        return function_value.function()(
            self.value["irradiance"]["valueList"][index], irradiance
        )
