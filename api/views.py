from django.shortcuts import render, HttpResponse, redirect
import json
from repository import models
from . import service
from utils import auth
from django.conf import settings
from utils import my_aes


@auth.auth
def asset(request):
    if request.method == 'GET':
        ys = '这真的是重要数据'
        return HttpResponse(ys)
    elif request.method == 'POST':
        # 新资产信息
        server_info = request.body
        server_info = my_aes.decrypt(server_info,settings.AES_KEY)
        server_info = json.loads(server_info)
        hostname = server_info['basic']['data']['hostname']
        # 老资产信息
        server_obj = models.Server.objects.filter(hostname=hostname).first()
        if not server_obj:
            return HttpResponse('当前主机名在资产中未录入')

        service.ManageInfo(server_info,server_obj).manage()
        return HttpResponse('ok')


