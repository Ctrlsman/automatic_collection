from repository import models


class Board:
    def __init__(self, server_info, server_obj):
        self.server_info = server_info
        self.server_obj = server_obj

    def dispose(self):
        """
        "board": {
        "status": true,
        "data": {
        "manufacturer": "Parallels Software International Inc.",
        "model": "Parallels Virtual Platform",
        "sn": "Parallels-1A 1B CB 3B 64 66 4B 13 86 B0 86 FF 7E 2B 20 30"}}
        :return:
        """
        hostname = self.server_info['basic']['data']['hostname']
        if not self.server_info['board']['status']:
            models.ErrorLog.objects.create(content=self.server_info['board']['data'], asset_obj=self.server_obj.asset,
                                           title='【%s】主板采集错误信息' % hostname)
        new_board_dict = self.server_info['board']['data']
        old_board_obj = models.Server.objects.filter(hostname=hostname).values('manufacturer', 'model',
                                                                               'sn').first()
        content = []
        for k, v in new_board_dict.items():
            if k not in old_board_obj:
                print(k,old_board_obj)
                models.Server.objects.filter(hostname=hostname).update(**new_board_dict)
                content.append(
                    "新增主板: 型号{model};制造商：{manufacturer};SN号：{sn}".format(**new_board_dict))
                break
            if v != old_board_obj[k]:
                content.append("[%s]的主板:[%s]由[%s]变为[%s]" % (hostname, k, old_board_obj[k], v))
                old_board_obj[k] = v
        models.Server.objects.filter(hostname=hostname).update(**old_board_obj)
        models.AssetRecord.objects.create(asset_obj=self.server_obj.asset, content=';'.join(content))
