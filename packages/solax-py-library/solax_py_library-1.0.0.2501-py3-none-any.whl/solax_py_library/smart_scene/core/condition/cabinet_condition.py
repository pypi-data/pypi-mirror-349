
class CabinetCondition(BaseCondition):
    def __init__(self, smart_scene_service):
        super().__init__(smart_scene_service)
        self.type = IF_ELE_TYPE
        self.value = defaultdict(
            lambda: {
                "soc": None,
                "alarm_level": {
                    AlarmLevel.EMERGENCY: False,
                    AlarmLevel.NORMAL: False,
                    AlarmLevel.TIPS: False,
                },
            }
        )
        self.meet_func = self.meet_cabinet_condition

    def update_value(self):
        # 查询实时数据
        cabinet_sns = [c.SN for c in self.db_service.get_all_cabinet()]
        self._update_cabinet_soc(cabinet_sns)
        self._update_cabinet_alarm(cabinet_sns)

    def _update_cabinet_alarm(self, cabinet_sns):
        all_alarm_code = self.redis_service.get_all_device_alarm_code()
        if not all_alarm_code:
            return

        cabinet_sn_pcs_sn_map = defaultdict(list)
        for pcs in self.db_service.get_pcs_by_cabinet(cabinet_sns):
            cabinet_sn_pcs_sn_map[pcs.cabinetSN].append(pcs.SN)

        cabinet_sn_bms_sn_map = defaultdict(list)
        for bms in self.db_service.get_bms_by_cabinet(cabinet_sns):
            cabinet_sn_bms_sn_map[bms.cabinetSN].append(bms.SN)

        cabinet_sn_io_sn_map = defaultdict(list)
        for io in self.db_service.get_io_by_cabinet(cabinet_sns):
            cabinet_sn_io_sn_map[io.cabinetSN].append(io.SN)

        for sn in cabinet_sns:
            cabinet_alarm = set(all_alarm_code.get(sn, []))
            pcs_alarm = set()
            for pcs_sn in cabinet_sn_pcs_sn_map.get(sn, []):
                pcs_alarm.update(all_alarm_code.get(pcs_sn, []))

            bms_alarm = set()
            for bms_sn in cabinet_sn_bms_sn_map.get(sn, []):
                bms_alarm.update(all_alarm_code.get(bms_sn, []))

            io_alarm = set()
            for io_sn in cabinet_sn_io_sn_map.get(sn, []):
                io_alarm.update(all_alarm_code.get(io_sn, []))

            self.value[sn]["alarm_level"][AlarmLevel.TIPS] = any(
                [
                    bool(cabinet_alarm & set(AlarmPointInfo.CABINET_TIPS_ALARM_DATA)),
                    bool(pcs_alarm & set(AlarmPointInfo.PCS_TIPS_ALARM_DATA)),
                    bool(bms_alarm & set(AlarmPointInfo.BMS_TIPS_ALARM_DATA)),
                    bool(io_alarm & set(AlarmPointInfo.IO_TIPS_ALARM_DATA)),
                ]
            )
            self.value[sn]["alarm_level"][AlarmLevel.NORMAL] = any(
                [
                    bool(cabinet_alarm & set(AlarmPointInfo.CABINET_NORMAL_ALARM_DATA)),
                    bool(pcs_alarm & set(AlarmPointInfo.PCS_NORMAL_ALARM_DATA)),
                    bool(bms_alarm & set(AlarmPointInfo.BMS_NORMAL_ALARM_DATA)),
                    bool(io_alarm & set(AlarmPointInfo.IO_NORMAL_ALARM_DATA)),
                ]
            )
            self.value[sn]["alarm_level"][AlarmLevel.EMERGENCY] = any(
                [
                    bool(
                        cabinet_alarm & set(AlarmPointInfo.CABINET_EMERGENCY_ALARM_DATA)
                    ),
                    bool(pcs_alarm & set(AlarmPointInfo.PCS_EMERGENCY_ALARM_DATA)),
                    bool(bms_alarm & set(AlarmPointInfo.BMS_EMERGENCY_ALARM_DATA)),
                    bool(io_alarm & set(AlarmPointInfo.IO_EMERGENCY_ALARM_DATA)),
                ]
            )

    def _update_cabinet_soc(self, cabinet_sns):
        for sn in cabinet_sns or []:
            result = self.smart_scene_service.redis_service.get_bms_current_data(sn)
            self.value[sn]["soc"] = result[14] if result else 0

    def meet_cabinet_condition(self, data: CabinetConditionItemData, ctx):
        if not self.value:
            return False
        cabinet = ctx["cabinet"] or []
        for cabinet_sn in cabinet:
            if data.childType == CabinetConditionType.cabinetSoc:
                if self.value[cabinet_sn]["soc"] is None:
                    return False
                if self.smart_scene_service.compare_the_magnitudes(
                    data.childData.function,
                    compare_value=self.value[cabinet_sn]["soc"],
                    base_value=data.childData.data[0],
                ):
                    return True
            elif data.childType == CabinetConditionType.cabinetAlarm:
                if self.value[cabinet_sn]["alarm_level"][data.childData.data[0]]:
                    return True
        return False
