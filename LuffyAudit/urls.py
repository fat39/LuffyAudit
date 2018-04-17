"""LuffyAudit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from audit import views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path("^$",views.index),
    re_path("^login/$",views.acc_login),
    re_path("^logout/$",views.acc_logout),
    re_path("^hostlist/$",views.hostlist,name='hostlist'),
    re_path("^multitask/$",views.multitask,name='multitask'),
    re_path("^multitask/result/$",views.multitask_result,name='get_task_result'),
    re_path("^multitask/cmd/$",views.multi_cmd,name='multi_cmd'),
    re_path("^api/hostlist/$",views.get_host_list,name='get_host_list'),
    re_path("^api/token/$",views.get_token,name='get_token'),
]
