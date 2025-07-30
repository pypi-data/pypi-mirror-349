# from solax_py_library.smart_scene.core.action.base import BaseAction
# from solax_py_library.smart_scene.types.action import SystemActionType
# from solax_py_library.smart_scene.types.condition import SystemConditionItemData
#
#
# class SystemAction(BaseAction):
#     def __init__(self, smart_scene_service, app_log):
#         super().__init__(smart_scene_service)
#         self.log = app_log
#         self.do_func = self.do_system_action
#         self.cabinet_type = None
#
#     def do_system_action(self, scene_id, data: SystemConditionItemData):
#         child_data = data.childData
#         child_type = data.childType
#         data = child_data.data
#         if self.cabinet_type is None:
#             self.cabinet_type = self.smart_scene_service.get_cabinet_type()
#         if child_type == SystemActionType.systemSwitch:
#             return self.system_switch(data[0], scene_id)
#         elif child_type == SystemActionType.exportControl:
#             return self.export_control(data, scene_id)
#         elif child_type == SystemActionType.importControl:
#             return self.import_control(data, scene_id)
#         elif child_type == SystemActionType.workMode:
#             return self.work_mode(data, scene_id)
#         return False
#
#
# class SystemSwitchAction(SystemAction):
#     def system_switch(self, value, scene_id) -> bool:
#         """系统开关机"""
#         if value not in [0, 1]:
#             value = 1
#         if self.cabinet_type in ["TRENE"]:
#             self.ems_tcp_service.set_trene_switch(value)
#             return True
#         else:
#             master_sn = self.device_service.get_master_inv_by_device()
#             # 如果为AELIO，则只需要操控主机
#             if master_sn:
#                 data = {"sn": master_sn, "switch": value}
#                 self.log.info(f"执行: 系统开关机, data: {data}")
#                 t = threading.Thread(
#                     target=self.smart_scene_service.request_local_server,
#                     args=("setSystemSwitch", data, scene_id),
#                     daemon=True,
#                 )
#                 t.start()
#         return True
#
#
# class ExportControlAction(SystemAction):
#     def export_control(self, value, scene_id) -> bool:
#         """零输出控制"""
#         if len(value) != 4:
#             value.extend([1, 0, 1])
#         data = {
#             "isEnable": value[0],
#             "controlMode": value[1],
#             "exportValue": value[2],
#             "unitType": value[3],
#         }
#         self.log.info(f"执行: 馈网控制, data: {data}")
#         ret = self.smart_scene_service.request_local_server(
#             "editOutputControl", data, scene_id
#         )
#         if not ret or ret["success"] is False:
#             return False
#         return True
#
#
# class ImportControlAction(SystemAction):
#     def import_control(self, value, scene_id) -> bool:
#         """需量控制"""
#         if self.cabinet_type in ["TRENE"]:
#             if len(value) != 3:
#                 value.extend([1, 0])
#             data = {
#                 "isAllowDischarge": value[1],
#                 "demandLimitValue": value[2],
#                 "isEnable": value[0],
#             }
#         else:
#             if len(value) != 2:
#                 value.append(0)
#             data = {
#                 "isAllowDischarge": 1,
#                 "demandLimitValue": value[1],
#                 "isEnable": value[0],
#             }
#         self.log.info(f"执行: 需量控制, data: {data}")
#         ret = self.smart_scene_service.request_local_server(
#             "editDemandControl", data, scene_id
#         )
#         if not ret or ret["success"] is False:
#             return False
#         return True
#
#
# class WorkModeAction(SystemAction):
#     def work_mode(self, value, scene_id) -> bool:
#         # 0: self use; 1: 并网优先; 2: 备用模式; 3: 手动； 4： 削峰填谷 5： TOU（暂不用）; 16: VPP
#         if value[0] not in [0, 1, 2, 3, 4, 16]:
#             return False
#         data = None
#         if self.cabinet_type in ["AELIO"]:
#             if value[0] in [0, 1, 2, 3, 4]:
#                 data = {"useMode": value[0]}
#         elif self.cabinet_type in ["TRENE"]:
#             if value[0] in [0, 1, 3, 4]:
#                 data = {"useMode": value[0]}
#         else:
#             return False
#         if data is not None:  # 普通模式
#             self.log.info(f"普通模式控制 data: {data}")
#             # 手动模式
#             if data["useMode"] == 3:
#                 if value[1] == 5:
#                     value.extend([0, 10])
#                 self.smart_scene_service.set_manual_mode(
#                     value[1], value[2], value[3], self.cabinet_type
#                 )
#             else:
#                 self.smart_scene_service.request_local_server(
#                     "setAelioUseMode", data, scene_id
#                 )
#         else:  # VPP模式
#             if self.cabinet_type in ["AELIO"]:
#                 if value[1] == 1:
#                     reg_value_list = [1]
#                     # 有功功率
#                     reg_value_list.extend(
#                         self.smart_scene_service.struct_transform(
#                             value[2] * 1000, "int32", "little"
#                         )
#                     )
#                     # 无功功率
#                     reg_value_list.extend(
#                         self.smart_scene_service.struct_transform(
#                             value[3] * 1000, "int32", "little"
#                         )
#                     )
#                     # 持续时间35秒, 控制超时 35s,控制类型为set
#                     reg_value_list.extend([35, 35, 1])
#                 elif value[1] == 2:
#                     reg_value_list = [2, 1]
#                     # 能量目标
#                     reg_value_list.extend(
#                         self.smart_scene_service.struct_transform(
#                             value[2] * 1000, "uint32", "little"
#                         )
#                     )
#                     # 功率目标
#                     reg_value_list.extend(
#                         self.smart_scene_service.struct_transform(
#                             value[3] * 1000, "int32", "little"
#                         )
#                     )
#                     # 控制超时 35s
#                     reg_value_list.extend([35])
#                 elif value[1] == 3:
#                     # 控制类型为set，SOC：value[2]
#                     reg_value_list = [3, 1, value[2]]
#                     # 充放电功率目标
#                     reg_value_list.extend(
#                         self.smart_scene_service.struct_transform(
#                             value[3] * 1000, "int32", "little"
#                         )
#                     )
#                     # 控制超时 35s
#                     reg_value_list.extend([35])
#                 elif value[1] == 4:
#                     reg_value_list = [4]
#                     # 电池功率目标
#                     reg_value_list.extend(
#                         self.smart_scene_service.struct_transform(
#                             value[2] * 1000, "int32", "little"
#                         )
#                     )
#                     # 控制超时 35s, # 远程控制超时后需设备执行的模式 0xA0 关闭VPP，0xA1 默认的VPP模式
#                     reg_value_list.extend([35, 0xA0])
#                 elif value[1] == 5:
#                     reg_value_list = [5]
#                     # 控制超时 35s, # 远程控制超时后需设备执行的模式 0xA0 关闭VPP，0xA1 默认的VPP模式
#                     reg_value_list.extend([35, 0xA0])
#                 elif value[1] == 6:
#                     reg_value_list = [6]
#                     # 控制超时 35s, # 远程控制超时后需设备执行的模式 0xA0 关闭VPP，0xA1 默认的VPP模式
#                     reg_value_list.extend([35, 0xA0])
#                 elif value[1] == 7:
#                     reg_value_list = [7]
#                     # 控制超时 35s, # 远程控制超时后需设备执行的模式 0xA0 关闭VPP，0xA1 默认的VPP模式
#                     reg_value_list.extend([35, 0xA0])
#                 elif value[1] == 8:
#                     # 控制类型为set，
#                     reg_value_list = [8, 1]
#                     # PV功率限制
#                     reg_value_list.extend(
#                         self.smart_scene_service.struct_transform(
#                             value[2] * 1000, "uint32", "little"
#                         )
#                     )
#                     # 电池功率限制
#                     reg_value_list.extend(
#                         self.smart_scene_service.struct_transform(
#                             value[3] * 1000, "int32", "little"
#                         )
#                     )
#                     # 控制超时 35s, # 远程控制超时后需设备执行的模式 0xA0 关闭VPP，0xA1 默认的VPP模式
#                     reg_value_list.extend([35, 0xA0])
#                 elif value[1] == 9:
#                     # 控制类型为set，
#                     reg_value_list = [9, 1]
#                     # PV功率限制
#                     reg_value_list.extend(
#                         self.smart_scene_service.struct_transform(
#                             value[2] * 1000, "uint32", "little"
#                         )
#                     )
#                     # 电池功率限制
#                     reg_value_list.extend(
#                         self.smart_scene_service.struct_transform(
#                             value[3] * 1000, "int32", "little"
#                         )
#                     )
#                     # 控制超时 35s, # 远程控制超时后需设备执行的模式 0xA0 关闭VPP，0xA1 默认的VPP模式
#                     reg_value_list.extend([value[4], 35, 0xA0])
#                 else:
#                     reg_value_list = []
#                 func_name = PCSOperateFunctionName.SET_AELIO_VPP_MODE
#                 channel = options.REDIS_WRITE_SERIAL_DEVICE
#                 future_data = {}
#                 future_data["func_name"] = func_name
#                 future_data["operationMode"] = Enumeration.SINGLE_DEVICE_MODE
#                 future_data["data"] = {"value_list": reg_value_list}
#                 app_log.info(f"VPP模式控制 data: {future_data}")
#                 self.smart_scene_service.request_local_redis(
#                     channel, json.dumps(future_data)
#                 )
#         return True
