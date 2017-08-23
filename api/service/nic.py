from repository import models


class Nic:
    def __init__(self, server_info, server_obj):
        self.server_info = server_info
        self.server_obj = server_obj

    def dispose(self):
        """
        'nic': {
        'status': True,
        'data': {
            'eth0': {
                'up': True,
                'hwaddr': '00:1c:42:a5:57:7a',
                'ipaddrs': '10.211.55.4',
                'netmask': '255.255.255.0'
            }
            name = models.CharField('网卡名称', max_length=128)
            hwaddr = models.CharField('网卡mac地址', max_length=64)
            netmask = models.CharField(max_length=64)
            ipaddrs = models.CharField('ip地址', max_length=256)
            up = models.BooleanField(default=False)
            server_obj = models.ForeignKey('Server',related_name='nic')
        :return:
        """

        content = []
        hostname = self.server_info['basic']['data']['hostname']
        if not self.server_info['nic']['status']:
            models.ErrorLog.objects.create(content=self.server_info['nic']['data'], asset_obj=self.server_obj.asset,
                                           title='【%s】网卡采集错误信息' % hostname)
        new_nic_dict = self.server_info['nic']['data']
        old_nic_obj = models.NIC.objects.filter(server_obj=self.server_obj)
        if not old_nic_obj:
            for k,v in new_nic_dict.items():
                new_nic_dict[k]['name'] = k
                new_nic_dict[k]['server_obj'] = self.server_obj
                models.NIC.objects.create(**new_nic_dict[k])
                new_nic_dict[k].pop('server_obj')
                content.append("[%s]主机" % hostname + "新增网卡:{name},MAC地址：{hwaddr},IP地址:{ipaddrs},网关：{netmask},状态:{up}".format(**(new_nic_dict[k])))
            models.AssetRecord.objects.create(asset_obj=self.server_obj.asset, content=';'.join(content))
        # 修改网卡
