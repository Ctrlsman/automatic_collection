from repository import models


class Disk:
    def __init__(self, server_info, server_obj):
        self.server_info = server_info
        self.server_obj = server_obj

    def dispose(self):
        hostname = self.server_info['basic']['data']['hostname']
        if not self.server_info['disk']['status']:
            models.ErrorLog.objects.create(content=self.server_info['disk']['data'], asset_obj=self.server_obj.asset,
                                           title='【%s】硬盘采集错误信息' % hostname)
        new_disk_dict = self.server_info['disk']['data']

        old_disk_list = models.Disk.objects.filter(server_obj=self.server_obj)

        # 交集：5, 创建：3,删除4;
        new_slot_list = list(new_disk_dict.keys())

        old_slot_list = []
        for item in old_disk_list:
            old_slot_list.append(item.slot)

        # 交集：更新[5,]
        update_list = set(new_slot_list).intersection(old_slot_list)
        # 差集: 创建[3]
        create_list = set(new_slot_list).difference(old_slot_list)
        # 差集: 创建[4]
        del_list = set(old_slot_list).difference(new_slot_list)

        if del_list:
            # 删除
            models.Disk.objects.filter(server_obj=self.server_obj, slot__in=del_list).delete()
            # 记录日志
            models.AssetRecord.objects.create(asset_obj=self.server_obj.asset,
                                              content="移除硬盘：%s" % ("、".join(del_list),))

        # 增加、
        record_list = []
        for slot in create_list:
            disk_dict = new_disk_dict[slot]  # {'capacity': '476.939', 'slot': '4', 'model': 'S1AXNSAF303909M     Samsung SSD 840 PRO Series
            disk_dict['server_obj'] = self.server_obj
            models.Disk.objects.create(**disk_dict)
            temp = "新增硬盘:位置{slot},容量{capacity},型号:{model},类型:{pd_type}".format(**disk_dict)
            record_list.append(temp)
        if record_list:
            content = ";".join(record_list)
            models.AssetRecord.objects.create(asset_obj=self.server_obj.asset, content=content)

        # ############ 更新 ############
        record_list = []
        row_map = {'capacity': '容量', 'pd_type': '类型', 'model': '型号'}
        for slot in update_list:
            new_dist_row = new_disk_dict[slot]
            ol_disk_row = models.Disk.objects.filter(slot=slot, server_obj=self.server_obj).first()
            for k, v in new_dist_row.items():
                # k: capacity;slot;pd_type;model
                # v: '476.939''xxies              DXM05B0Q''SATA'
                value = getattr(ol_disk_row, k)
                if v != str(value):
                    record_list.append("槽位%s,%s由%s变更为%s" % (slot, row_map[k], value, v,))
                    setattr(ol_disk_row, k, v)
            ol_disk_row.save()
        if record_list:
            content = ";".join(record_list)
            models.AssetRecord.objects.create(asset_obj=self.server_obj.asset, content=content)
