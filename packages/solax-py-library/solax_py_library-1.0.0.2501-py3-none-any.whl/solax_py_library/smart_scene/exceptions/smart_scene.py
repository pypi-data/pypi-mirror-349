from solax_py_library.exception import SolaxBaseError


class OnlyPositive(SolaxBaseError):
    message = "smart_scene__time_range"


class TimeRange(SolaxBaseError):
    message = "smart_scene__irradiance_only_positive"


class IrradianceOnlyPositive(SolaxBaseError):
    message = "smart_scene__export_limit_num"


class ExportLimitNum(SolaxBaseError):
    message = "smart_scene__export_limit_percent"


class ExportLimitPercent(SolaxBaseError):
    message = "smart_scene__import_limit_num"


class ImportLimitNum(SolaxBaseError):
    message = "smart_scene__import_only_positive"


class ImportOnlyPositive(SolaxBaseError):
    message = "smart_scene__soc_limit"


class SocLimit(SolaxBaseError):
    message = "smart_scene__active_power_limit_num"


class ActivePowerLimitNum(SolaxBaseError):
    message = "smart_scene__reactive_power_limit_num"


class ReactivePowerLimitNum(SolaxBaseError):
    message = "smart_scene__energy_limit"


class EnergyLimit(SolaxBaseError):
    message = "smart_scene__power_limit_num"


class PowerLimitNum(SolaxBaseError):
    message = "smart_scene__battery_power_limit_num"


class BatteryPowerLimitNum(SolaxBaseError):
    message = "smart_scene__pv_only_ge_0"


class PvOnlyGe0(SolaxBaseError):
    message = "smart_scene__miss_param"


class MissParam(SolaxBaseError):
    message = "smart_scene__count_limit"


class CountLimit(SolaxBaseError):
    message = "smart_scene__name_length_limit"


class NameLengthLimit(SolaxBaseError):
    message = "smart_scene__unique_limit"


class UniqueLimit(SolaxBaseError):
    message = "cloud__electricity_price_failure"


class ElectricityPriceFailure(SolaxBaseError):
    message = "cloud__weather_failure"


class WeatherFailure(SolaxBaseError):
    message = "cloud__weather_failure"
