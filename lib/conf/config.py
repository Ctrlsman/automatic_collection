#!/usr/local/python3
import os
from . import global_settings
import importlib


class Settings:
    """
    先加载系统配置，再加载用户自定义配置，利用反射，默认配置形式 USER=‘xxx’
    """

    def __init__(self):
        for name in dir(global_settings):
            if name.isupper():
                value = getattr(global_settings, name)
                setattr(self, name, value)
        settings_module = os.environ.get('USER_SETTINGS')   # start.py中 os.environ['USER_SETTINGS'] = "config.settings"
        if not settings_module:
            return
        m = importlib.import_module(settings_module)  # 拿到模块对象 <module 'time' (built-in)>  m. 调用
        for name in dir(m):  # 循环该模块的属性列表
            if name.isupper():
                value = getattr(m, name)
                setattr(self, name, value)


settings = Settings()