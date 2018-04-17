import string
import datetime
import random
import json
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from audit import models

# @login_required(login_url='/login/')  # 单独添加login页面的url
# 或在settings.py设置全局LOGIN_URL = '/login/'
@login_required
def index(request):
    return render(request,"index.html")


def acc_login(request):
    error = ''
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username,password=password)  # 认证
        if user:
            login(request,user)  # 登录
            return redirect(request.GET.get('next') or "/")  # 若有next字段，则跳转到该url，否则index页面
        else:
            error = "Wrong username or password"

    return render(request,"login.html",{"error":error})


@login_required
def acc_logout(request):
    logout(request)  # 登出
    return redirect("/login/")

# @login_required(login_url='/login/')  # 单独添加login页面的url
# 或在settings.py设置全局LOGIN_URL = '/login/'
@login_required
def hostlist(request):
    return render(request,"hostlist.html")

@login_required()
def get_host_list(request):
    gid = request.GET.get("gid")
    if gid:
        if gid == "-1":  # 未分组
            host_list = request.user.account.host_user_bind.all()
        else:
            group_obj = request.user.account.host_groups.get(id=gid)
            host_list = group_obj.host_user_binds.all()

        data = json.dumps(list(host_list.values('id','host__hostname','host__ip_addr','host__idc__name','host__port',
                         'host_user__username')))

        return HttpResponse(data)


@login_required
def get_token(request):
    """ 生成token并返回 """
    bind_host_id = request.POST.get("bind_host_id")
    time_obj = datetime.datetime.now() - datetime.timedelta(seconds=300) 
    exist_token_objs = models.Token.objects.filter(account_id=request.user.account.id,host_user_bind_id=bind_host_id,date__gt=time_obj)
    token_data = {}
    if exist_token_objs:  # has token already
        token_data = {"token":exist_token_objs[0].val}
    else:
        token_val = "".join(random.sample(string.ascii_lowercase+string.digits,8))
        token_obj = models.Token.objects.create(host_user_bind_id = bind_host_id,
            account = request.user.account,
            val = token_val,
            )
        token_data = {"token":token_val}
    return HttpResponse(json.dumps(token_data))








