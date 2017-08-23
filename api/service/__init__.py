from . import basic
from django.conf import settings
import importlib


class ManageInfo:
    def __init__(self, server_info, server_obj):
        self.server_info = server_info
        self.server_obj = server_obj

    def manage(self):
        """
        SERVICE_DICT = {
            'basic': "api.service.basic.Basic",
            'board': "api.service.board.Board",
            'cpu': "api.service.cpu.Cpu",
            'disk': "api.service.disk.Disk",
            'memory': "api.service.memory.Memory",
            'nic': "api.service.nic.Nic",
        }
        :return:
        """
        for k, v in settings.SERVICE_DICT.items():
            module_path, class_name = v.rsplit('.', 1)
            m = importlib.import_module(module_path)
            cls = getattr(m, class_name)
            obj = cls(self.server_info,self.server_obj)
            obj.dispose()



