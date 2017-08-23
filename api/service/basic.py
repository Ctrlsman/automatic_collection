from repository import models


class Basic:
    def __init__(self, server_info, server_obj):
        self.server_info = server_info
        self.server_obj = server_obj

    def dispose(self):
        """
        {'basic': {
        'status': True,
            'data': {
                 'os_platform': 'linux',
                 'os_version': 'CentOS release 6.6 (Final)\nKernel \r on an \\m',
                 'hostname': 'c1.com'
         }
         }
        :return:
        """
        content = []
        hostname = self.server_info['basic']['data']['hostname']
        if not self.server_info['basic']['status']:
            models.ErrorLog.objects.create(content=self.server_info['basic']['data'], asset_obj=self.server_obj.asset,
                                           title='【%s】主机采集错误信息' % hostname)
        new_basic_dict = self.server_info['basic']['data']
        old_basic_dict = models.Server.objects.filter(hostname=hostname).values('hostname','os_platform','os_version').first()
        for k,v in new_basic_dict.items():
            if v != old_basic_dict[k]:
                content.append("[%s]的:[%s]由[%s]变为[%s]" % (hostname, k, old_basic_dict[k], v))
                old_basic_dict[k] = v
        models.Server.objects.filter(hostname=hostname).update(**old_basic_dict)
        models.AssetRecord.objects.create(asset_obj=self.server_obj.asset, content=';'.join(content))