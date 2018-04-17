# -*- coding:utf-8 -*-
from audit import models
import json

class Task(object):
    """处理批量任务，包括命令和文件传输"""
    def __init__(self,request):
        self.request = request
        self.errors = []


    def is_valid(self):
        """
        1.验证命令、主机列表合法
        :return:
        """
        task_data = self.request.POST.get("task_data")
        if task_data:
            self.task_data = json.loads(task_data)
            if self.task_data.get("task_type") == "cmd":
                if self.task_data.get("cmd") and self.task_data.get("selected_host_ids"):
                    return True
                self.errors.append({"invalid_argument": "cmd or host_list is empty."})
            elif self.task_data.get("task_type") == "file_transfer":
                '''待补充'''
                return
                self.errors.append({"invalid_argument": "cmd or host_list is empty."})
            else:
                self.errors.append({"invalid_argument": "task_type is invalid."})
        self.errors.append({"invalid_data":"task_data is not exist."})


    def run(self):
        """start task and return task id"""
        task_func = getattr(self,self.task_data.get("task_type"))
        res = task_func()
        return 1

    def cmd(self):
        """批量任务"""
        print("run multitask cmd")
        task_obj = models.Task.objects.create(
            task_type = 0,
            account = self.request.user.account,
            content = self.task_data.get("cmd"),
        )
        task_obj.host_user_binds.add(*self.task_data.get("selected_host_ids"))
        task_obj.save()


    def file_transfer(self):
        """批量文件"""
        pass





