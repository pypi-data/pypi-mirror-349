from datetime import datetime

from solax_py_library.smart_scene.core.condition.base import BaseCondition
from solax_py_library.smart_scene.types.condition import PriceConditionItemData, PriceConditionType, SmartSceneUnit


class ElePriceCondition(BaseCondition):
    def __init__(self):
        super().__init__()
        self.buy = True
        self.value = {}
        self.unit = None

    def update_value(self):
        """获取电价 类型需要的数据"""
        ele_info = self.smart_scene_service.get_electrovalence_data()
        if self.buy:
            self.value = ele_info.get("buy", [])
        else:
            self.value = ele_info.get("sell", [])
        self.unit = ele_info.get("ele_unit", " ")

    def meet_func_price(self, function_value, data_value, index) -> bool:
        """电价条件的判定"""
        if index < 0 or index > len(self.value):
            return False
        if self.value[index] is None:
            return False
        return self.smart_scene_service.compare_the_magnitudes(
            function_value, self.value[index], data_value[0]
        )

    def meet_func_highest_price(self, data_value, index) -> bool:
        value, unit = data_value
        if None in self.value[0:96]:
            return False
        if unit == SmartSceneUnit.NUM:  # 比最高电价低X元
            base = max(self.value[0:96]) - value
        else:  # 比最高电价低X%
            base = round(max(self.value[0:96]) * (1 - value / 100), 4)
        if self.value[index] <= base:
            return True
        else:
            return False

    def meet_func_lowest_price(self, data_value, index) -> bool:
        value, unit = data_value
        if None in self.value[0:96]:
            return False
        if unit == SmartSceneUnit.NUM:  # 比最低电价高X元
            base = value - min(self.value[0:96])
        else:  # 比最低电价高X%
            base = round(min(self.value[0:96]) * (1 + value / 100), 4)
        if self.value[index] >= base:
            return True
        else:
            return False

    def meet_func_highest_or_lowest_hours(self, data_value, index, func) -> bool:
        sort_index, start_index = self.smart_scene_service.get_highest_or_lowest_price(
            data_value[0], data_value[1], data_value[2], self.value, func=func
        )
        if not sort_index:
            return False
        if index - start_index in sort_index:
            return True
        else:
            return False

    def meet_func(self, data: PriceConditionItemData, ctx):
        if not self.value:
            # 未获取到价格数据，直接返回
            return False
        child_data = data.childData
        child_type = data.childType
        data_value = child_data.data
        now_time = datetime.strftime(datetime.now(), "%H:%M")
        index = self.smart_scene_service.trans_str_time_to_index(now_time)
        if child_type == PriceConditionType.price:
            return self.meet_func_price(child_data.function, data_value, index)
        elif child_type == PriceConditionType.lowerPrice:
            return self.meet_func_highest_price(data_value, index)
        elif child_type == PriceConditionType.higherPrice:
            return self.meet_func_lowest_price(data_value, index)
        elif child_type == PriceConditionType.expensiveHours:
            return self.meet_func_highest_or_lowest_hours(
                data_value, index, "expensive_hours"
            )
        elif child_type == PriceConditionType.cheapestHours:
            return self.meet_func_highest_or_lowest_hours(
                data_value, index, "cheapest_hours"
            )
        return False


class EleSellPriceCondition(ElePriceCondition):
    def __init__(self):
        super().__init__()
        self.buy = False


class ElsBuyPriceCondition(ElePriceCondition):
    def __init__(self):
        super().__init__()
        self.buy = True
