import json
import os.path
import struct
import traceback
import threading
import subprocess as sp

import requests
from datetime import datetime, timedelta

from tornado.log import app_log

from domain.ems_enum.smart_scene.condition import ConditionFunc
from settings.const import (
    RedisKey,
    Role,
    DeviceInfo,
    PCSOperateFunctionName,
    Enumeration,
    FilePath,
)
from web.web_ext import config_json
from models.tables import Device
from utils.common import options, get_logger_sn, md5_encrypt, read_write_json_file
from services.redis_service import RedisService
from models.sqlite_db import session_maker
from utils.redis_utils import RedisProducer
from services.strategy_control_service import StrategyControlService
from solax_py_library.utils.cloud_client import CloudClient

redis_host = options.REDIS_HOST
redis_port = options.REDIS_PORT
db = options.REDIS_DB
LOCAL_URL = "http://127.0.0.1:8000/ems/cloud/"


class SmartSceneService(object):
    def __init__(self):
        self.ems_sn = get_logger_sn()
        self.redis_service = RedisService()
        self.redis_producer = RedisProducer().producer
        self.strategy_control_service = StrategyControlService()

    def request_local_redis(self, redis_topic, payload):
        """本地redis分发任务"""
        try:
            self.redis_producer.publish(redis_topic, payload)
        except Exception:
            app_log.info(traceback.format_exc())

    def request_local_server(self, apiName, apiPostData, scene_id=None):
        """
        访问本地接口, 调用server8000
        需要使用admin权限
        :param apiName: 接口名称
        :param apiPostData: 请求参数
        :param scene_id: 请求标识
        :return:
        """
        username = Role.SUPER_ADMIN
        user_info = {"username": username, "password": md5_encrypt(self.ems_sn)}
        token = self.redis_service.make_token(username, user_info)
        url = LOCAL_URL + apiName
        headers = {"token": token}
        try:
            response = requests.post(url, json=apiPostData, headers=headers, timeout=5)
            app_log.info(
                f"scene_id: {scene_id}, request apiName: {apiName}, response: {response.text}"
            )
            return json.loads(response.text)
        except Exception:
            app_log.info(traceback.format_exc())
            return False

    def get_token(self):
        token = self.redis_service.get_token()
        if not token:
            client = CloudClient(base_url=config_json.get("CLOUD_URL", ""))
            token = client.get_token(
                ems_sn=self.ems_sn, sn_secret=config_json.get("MQTT_PASSWORD")
            )
            if not token:
                app_log.info("访问token接口失败")
                return False
            self.redis_service.set_token(token)
            return token
        else:
            return token

    def get_weather_data_from_redis(self):
        try:
            weather_info = self.redis_service.get_ele_price_info() or {}
            return weather_info
        except Exception:
            app_log.error(traceback.format_exc())
            return {}

    def get_weather_data_from_cloud(self):
        """获取未来24小时天气数据"""
        try:
            token = self.get_token()
            client = CloudClient(base_url=config_json.get("CLOUD_URL", ""))
            weather_info = client.get_weather_data_from_cloud(
                ems_sn=self.ems_sn,
                token=token,
            )
            if not weather_info:
                app_log.error(f"获取天气数据失败 异常 {traceback.format_exc()}")
                return False
            app_log.info(f"获取天气数据成功: {weather_info}")
            self.redis_service.set_weather_info(weather_info)
        except Exception:
            app_log.error(f"获取天气数据失败 异常 {traceback.format_exc()}")
            return False

    def trans_str_time_to_index(self, now_time, minute=15):
        """将时间按照minute切换为索引，时间格式为 %H-%M"""
        time_list = [int(i) for i in now_time.split(":")]
        time_int = time_list[0] * 4 + time_list[1] // minute
        return time_int

    def get_electrovalence_data_from_cloud(self):
        try:
            token = self.get_token()
            client = CloudClient(base_url=config_json.get("CLOUD_URL", ""))
            ele_price_info = client.get_electrovalence_data_from_cloud(
                ems_sn=self.ems_sn, token=token
            )
            app_log.info(f"获取电价数据成功: {ele_price_info}")
            self.redis_service.set_ele_price_info(ele_price_info)
        except Exception:
            app_log.error(f"获取电价数据失败 异常 {traceback.format_exc()}")
            return False

    def get_electrovalence_data_from_redis(self):
        """从自定义电价的缓存中获取"""
        month_temp = self.redis_service.hget(
            RedisKey.MONTH_TEMPLATE, RedisKey.MONTH_TEMPLATE
        )
        month_temp = json.loads(month_temp) if month_temp else {}
        if month_temp == {}:
            return {}
        month = datetime.strftime(datetime.now(), "%m")
        month_map = {
            "01": "Jan",
            "02": "Feb",
            "03": "Mar",
            "04": "Apr",
            "05": "May",
            "06": "Jun",
            "07": "Jul",
            "08": "Aug",
            "09": "Sep",
            "10": "Oct",
            "11": "Nov",
            "12": "Dec",
        }
        month = month_map.get(month, None)
        if month is None:
            return {}
        template_id = str(month_temp.get(month, 0))
        price_info = self.redis_service.hget(
            RedisKey.ELECTRICITY_PRICE_TEMPLATE, template_id
        )
        price_info = json.loads(price_info) if price_info else {}
        if price_info == {}:
            return {}

        stationInfo = self.redis_service.get(RedisKey.STATION_INFO)
        stationInfo = json.loads(stationInfo) if stationInfo else {}
        currencyCode = stationInfo.get("currencyCode")
        currency_file = read_write_json_file(FilePath.CURRENCY_PATH)
        ele_unit = False
        try:
            for j in currency_file["list"]:
                if currencyCode == j["code"]:
                    ele_unit = j["unit"].split(":")[-1] + "/kWh"
                    break
        except:
            app_log.error(f"获取本地电价单位出错 {traceback.format_exc()}")
        ele_price_info = {
            "buy": [None] * 192,
            "sell": [None] * 192,
            "date": datetime.strftime(datetime.now(), "%Y-%m-%d"),
            "ele_unit": ele_unit if ele_unit else "/kWh",
        }
        for period in price_info["periodConfiguration"]:
            start_index = self.trans_str_time_to_index(period["startTime"])
            end_index = self.trans_str_time_to_index(period["endTime"])
            slotName = period["slotName"]
            for price in price_info["priceAllocation"]:
                if price["slotName"] == slotName:
                    ele_price_info["buy"][start_index:end_index] = [
                        price["buyPrice"]
                    ] * (end_index - start_index)
                    ele_price_info["sell"][start_index:end_index] = [
                        price["salePrice"]
                    ] * (end_index - start_index)
                    break
        return ele_price_info

    def get_electrovalence_data(self):
        try:
            online_status = self.redis_service.hget(RedisKey.LED_STATUS_KEY, "blue")
            online_status = (
                json.loads(online_status).get("status") if online_status else 0
            )
            if online_status:
                ele_price_info = self.redis_service.get_ele_price_info() or {}
                today = datetime.strftime(datetime.now(), "%Y-%m-%d")
                date_now = ele_price_info.get("date", "")
                if today not in date_now:
                    ele_price_info = {}
            else:
                app_log.info("设备离线，获取本地电价")
                ele_price_info = self.get_electrovalence_data_from_redis()
            return ele_price_info
        except Exception:
            app_log.error(traceback.format_exc())
            return {}

    def get_highest_or_lowest_price(
        self, start_time, end_time, hours, price_list, func="expensive_hours"
    ):
        """获取一段时间内，电价最高或最低的几个小时"""
        start_index = self.trans_str_time_to_index(start_time)
        end_index = self.trans_str_time_to_index(end_time)
        arr = price_list[start_index:end_index]
        if None in arr:
            return False
        indices = list(range(end_index - start_index))
        if func == "expensive_hours":
            reverse = True
        else:
            reverse = False
        sorted_indices = sorted(indices, key=lambda i: arr[i], reverse=reverse)
        return sorted_indices[: int(hours * 4)], start_index

    def get_rounded_times(self):
        """
        返回距离当前时间最近的15min的整点时间以及后一整点5min时间（天气是预测未来15min的，也就是在00:00时，只能拿到00:15的数据）
        """
        now = datetime.now()
        # 确定当前时间所属的15分钟区间
        index_1 = now.minute // 15
        index_2 = now.minute % 15
        left_time = now.replace(minute=15 * index_1, second=0, microsecond=0)
        right_time = left_time + timedelta(minutes=15)
        if index_2 < 8:
            nearest_time = left_time
        else:
            nearest_time = right_time
        return datetime.strftime(nearest_time, "%Y-%m-%d %H:%M:%S"), datetime.strftime(
            right_time, "%Y-%m-%d %H:%M:%S"
        )

    def compare_the_magnitudes(self, function, compare_value, base_value):
        """比较两个值"""
        if function == ConditionFunc.GT:
            return compare_value > base_value
        elif function == ConditionFunc.EQ:
            return compare_value == base_value
        elif function == ConditionFunc.LT:
            return compare_value < base_value
        return False

    def get_cabinet_type(self):
        # 获取机柜类型
        cabinet_type = 1
        with session_maker(change=False) as session:
            result = (
                session.query(Device.deviceModel)
                .filter(Device.deviceType == DeviceInfo.ESS_TYPE, Device.isDelete == 0)
                .first()
            )

            if result:
                cabinet_type = result[0]
        if cabinet_type in [3, 4, 7, 8]:
            key_name = "AELIO"
        else:
            key_name = "TRENE"
        return key_name

    def set_manual_mode(self, work_mode, power, soc, cabinet_type):
        """设置手动模式"""
        # 充电
        if work_mode == 3:
            strategy_info = {
                "chargePower": power,
                "chargeTargetSoc": soc,
                "runState": 1,
            }
            self.redis_service.hset(
                RedisKey.MANUAL_STRATEGY_INFO,
                RedisKey.CHARGE_MODE,
                json.dumps(strategy_info),
            )
            self.strategy_control_service.apply_or_stop_strategy(
                0, RedisKey.MANUAL_STRATEGY_INFO, RedisKey.DISCHARGE_MODE
            )
            # 将运行模式修改为手动
            self.redis_service.set(RedisKey.RUN_STRATEGY_TYPE, 1)
        elif work_mode == 4:
            strategy_info = {
                "dischargePower": power,
                "dischargeTargetSoc": soc,
                "runState": 1,
            }
            self.redis_service.hset(
                RedisKey.MANUAL_STRATEGY_INFO,
                RedisKey.DISCHARGE_MODE,
                json.dumps(strategy_info),
            )
            # 将充电状态修改
            self.strategy_control_service.apply_or_stop_strategy(
                0, RedisKey.MANUAL_STRATEGY_INFO, RedisKey.CHARGE_MODE
            )
            # 将运行模式修改为手动
            self.redis_service.set(RedisKey.RUN_STRATEGY_TYPE, 1)
        # 停止
        else:
            self.strategy_control_service.apply_or_stop_strategy(
                0, RedisKey.MANUAL_STRATEGY_INFO, RedisKey.DISCHARGE_MODE
            )
            self.strategy_control_service.apply_or_stop_strategy(
                0, RedisKey.MANUAL_STRATEGY_INFO, RedisKey.CHARGE_MODE
            )
            self.redis_service.set(RedisKey.RUN_STRATEGY_TYPE, 1)
        if work_mode == 3:
            manualType = 1
        elif work_mode == 4:
            manualType = 2
        else:
            manualType = 3
        data = {
            "power": power,
            "soc": soc,
            "workMode": work_mode,
            "manualType": manualType,
            "useMode": 3,
        }
        if cabinet_type in ["TRENE"]:
            t = threading.Thread(
                target=self.request_local_redis, args=(options.REDIS_POWER_CONTROL, "")
            )
        else:
            func_name = PCSOperateFunctionName.SET_AELIO_USE_MODE
            channel = options.REDIS_WRITE_SERIAL_DEVICE
            future_data = {}
            future_data["func_name"] = func_name
            future_data["operationMode"] = Enumeration.SINGLE_DEVICE_MODE
            future_data["data"] = data
            t = threading.Thread(
                target=self.request_local_redis,
                args=(channel, json.dumps(future_data)),
                daemon=True,
            )
        t.start()
        return True

    def struct_transform(self, value, fmt, order="big"):
        """将10进制的原始值转换为modbus协议需要的精度与类型的值"""
        value = int(value)
        if order == "little":
            opt = "<"
        else:
            opt = ">"
        try:
            if fmt == "int16":
                ret = struct.pack(f"{opt}h", value)
                ret_list = struct.unpack(f"{opt}H", ret)
            elif fmt == "uint16":
                ret = struct.pack(f"{opt}H", value)
                ret_list = struct.unpack(f"{opt}H", ret)
            elif fmt == "int32":
                ret = struct.pack(f"{opt}i", value)
                ret_list = struct.unpack(f"{opt}HH", ret)
            elif fmt == "uint32":
                ret = struct.pack(f"{opt}I", value)
                ret_list = struct.unpack(f"{opt}HH", ret)
            elif fmt == "int64":
                ret = struct.pack(f"{opt}q", value)
                ret_list = struct.unpack(f"{opt}HHHH", ret)
            elif fmt == "uint64":
                ret = struct.pack(f"{opt}Q", value)
                ret_list = struct.unpack(f"{opt}HHHH", ret)
            else:
                ret_list = [0]
        except Exception:
            if "16" in fmt:
                ret_list = [0]
            elif "32" in fmt:
                ret_list = [0, 0]
            else:
                ret_list = [0, 0, 0, 0]
        return list(ret_list)

    def ems_do_control(self, data):
        for do_info in data:
            do_number = do_info.DoNumber
            do_value = do_info.DoValue
            if 1 <= do_number <= 8 and do_value in [0, 1]:
                path = DeviceInfo.DI_DO_GPIO_MAPPING[f"DO{do_number}"] + "/value"
                if not os.path.exists(path):
                    app_log.info(f"DO path not exists {do_info}")
                else:
                    cmd = f"echo {do_value} > {path}"
                    ret = sp.getstatusoutput(cmd)
                    ret = True if ret[0] == 0 else False
                    app_log.info(f"DO {do_info} 控制结果: {ret}")
