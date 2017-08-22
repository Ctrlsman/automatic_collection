#!/usr/local/python3
from lib.conf.config import settings
import importlib
import traceback


class PluginManager(object):
    def __init__(self, hostname=None):
        self.hostname = hostname
        self.plugin_dict = settings.PLUGINS_DICT
        self.mode = settings.MODE
        self.debug = settings.DEBUG
        if self.mode == "SSH":
            self.ssh_user = settings.SSH_USER
            self.ssh_port = settings.SSH_PORT
            self.ssh_pwd = settings.SSH_PWD
            self.ssh_key = settings.SSH_KEY

    def exec_plugin(self):
        response = {}
        for k,v in self.plugin_dict.items():
            ret = {'status':True,'data':None}
            try:
                module_path, class_name = v.rsplit('.',1)
                m = importlib.import_module(module_path)
                cls = getattr(m,class_name)
                if hasattr(cls,'initial'):
                    obj = cls.initial()
                else:
                    obj = cls()
                result = obj.process(self.command,self.debug)
                ret['data'] = result
            except Exception as e:
                ret['status'] = False
                ret['data'] = "[%s][%s] 采集数据出现错误 : %s" %(self.hostname if self.hostname else "AGENT",k,traceback.format_exc())
                # 获取错误栈全部信息
            response[k] = ret
        return response

    def command(self, cmd):
        if self.mode == 'AGENT':
            return self.__agent(cmd)
        elif self.mode == 'SALT':
            return self.__salt(cmd)
        elif self.mode == 'SSH':
            return self.__ssh(cmd)
        else:
            raise Exception('Just Support mode ：["AGENT","SALT","SSH"]')


    def __agent(self, cmd):
        import subprocess
        output = subprocess.getoutput(cmd)
        return output

    def __salt(self, cmd):
        import subprocess
        output = subprocess.getoutput('salt "%s" cmd.run "%s"' % (self.hostname, cmd))
        return output

    def __ssh(self, cmd):
        import paramiko
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.hostname, port=self.ssh_port, username=self.ssh_user, password=self.ssh_pwd)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        output = stdout.read()
        ssh.close()
        return output
