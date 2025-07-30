#
# class EMS1000Action(BaseAction):
#     def __init__(self, smart_scene_service):
#         super().__init__(smart_scene_service)
#         self.do_func = self.do_ems1000_action
#         self.cabinet_type = None
#
#     def do_ems1000_action(self, scene_id, data: EmsActionItemData):
#         if data.childType == "DoControl":
#             ret = self.do_control(data.childData.data)
#         else:
#             ret = False
#         return ret
#
#     def do_control(self, data):
#         app_log.info("执行: DO控制")
#         self.smart_scene_service.ems_do_control(data)
#         return True
#
