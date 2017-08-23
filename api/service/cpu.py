from repository import models


class Cpu:
    def __init__(self, server_info, server_obj):
        self.server_info = server_info
        self.server_obj = server_obj

    def dispose(self):
        """
        cpu {'status': True,
        'data': {
            'cpu_count': 24,
            'cpu_physical_count': 2,
            'cpu_model': ' Intel(R) Xeon(R) CPU E5-2620 v2 @ 2.10GHz'
        }}

        :return:
        """
        hostname = self.server_info['basic']['data']['hostname']
        if not self.server_info['cpu']['status']:
            models.ErrorLog.objects.create(content=self.server_info['cpu']['data'], asset_obj=self.server_obj.asset,
                                           title='【%s】cpu采集错误信息' % hostname)
        new_cpu_dict = self.server_info['cpu']['data']
        old_cpu_obj = models.Server.objects.filter(hostname=hostname).values('cpu_count','cpu_physical_count','cpu_model').first()
        content = []
        for k,v in new_cpu_dict.items():
            if k not in old_cpu_obj:
                models.Server.objects.filter(hostname=hostname).update(**new_cpu_dict)
                content.append("新增CPU: 型号{cpu_model};cpu物理个数：{cpu_physical_count};cpu个数{cpu_count}".format(**new_cpu_dict))
                break
            if v != old_cpu_obj[k]:
                content.append("[%s]的CPU:[%s]由[%s]变为[%s]" % (hostname, k, old_cpu_obj[k], v))
                old_cpu_obj[k] = v
        models.Server.objects.filter(hostname=hostname).update(**old_cpu_obj)
        models.AssetRecord.objects.create(asset_obj=self.server_obj.asset, content=';'.join(content))