# -*- coding:utf-8 -*-


import time
import multiprocessing
import paramiko
import json
import os


def cmd_run(tasklog_id,task_id,cmd_str):
    import django
    django.setup()
    from audit import models

    tasklog_obj = models.TaskLog.objects.get(id=tasklog_id)
    try:
        print("run cmd:",tasklog_obj,cmd_str)

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(
            hostname=tasklog_obj.host_user_bind.host.ip_addr,
            port=tasklog_obj.host_user_bind.host.port,
            username=tasklog_obj.host_user_bind.host_user.username,
            password=tasklog_obj.host_user_bind.host_user.password,
            timeout=15,
        )
        stdin, stdout, stderr = ssh.exec_command(cmd_str)
        result = stdout.read() + stderr.read()
        # print(result.decode("utf-8"), )
        ssh.close()

        tasklog_obj.result = result.decode("utf-8") or "cmd has no result output."
        tasklog_obj.status = 0
        tasklog_obj.save()


    except Exception as e:
        print("error:", e)
        tasklog_obj.result = str(e)
        tasklog_obj.save()


def file_transfer(tasklog_id,task_id,task_content):
    import django
    django.setup()
    from audit import models
    from django.conf import settings

    tasklog_obj = models.TaskLog.objects.get(id=tasklog_id)
    try:
        # print("task content:",tasklog_obj,task_content)
        # task_data = json.loads(tasklog_obj.task.content)
        task_data = json.loads(task_content)

        t = paramiko.Transport((tasklog_obj.host_user_bind.host.ip_addr, tasklog_obj.host_user_bind.host.port))
        t.connect(username=tasklog_obj.host_user_bind.host_user.username, password=tasklog_obj.host_user_bind.host_user.password,)
        sftp = paramiko.SFTPClient.from_transport(t)

        if task_data.get("file_transfer_type") == "send":
            '''文件上传'''
            local_path = "%s/%s/%s" % (settings.FILE_UPLOADS,
                                       tasklog_obj.task.account.id,
                                       task_data.get("random_str"))
            print(local_path)
            for file_name in os.listdir(local_path):
                sftp.put("%s/%s" % (local_path,file_name),'%s/%s' % (task_data.get("remote_path"),file_name))
            tasklog_obj.result = "send all files done..."

        else:
            # 循环到所有的机器上的指定目录下载文件
            local_dir = os.path.join(settings.FILE_DOWNLOADS,task_id)
            # local_path = "{download_base_dir}/{task_id}".format(download_base_dir=settings.FILE_DOWNLOADS,task_id=task_id)
            os.makedirs(local_dir,exist_ok=True)
            file_name = "%s_%s" % (os.path.basename(task_data.get("remote_path")),tasklog_obj.host_user_bind.host.ip_addr)
            local_path = os.path.join(local_dir,file_name)
            sftp.stat(task_data.get("remote_path"))  # 如果直接get，无论是否存在该文件，都会创建一个local_path，所以先做这一步
            sftp.get(task_data.get("remote_path"),local_path)
            tasklog_obj.result = "get remote files [%s] to local done" % task_data.get("remote_path")

        tasklog_obj.status = 0
        tasklog_obj.save()

        t.close()



    except Exception as e:
        print("error:",e)
        tasklog_obj.result = str(e)
        tasklog_obj.save()


if __name__ == '__main__':
    import os
    import sys
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.append(BASE_DIR)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LuffyAudit.settings")
    import django
    django.setup()
    from audit import models
    from django.conf import settings


    task_id = sys.argv[1]

    # 1.根据Taskid拿到任务对象
    # 2.拿到任务关联的所有主机
    # 3.根据任务类型调用多线程，执行不同的方法
    # 4.每个子任务执行完毕后，自己把结果写入数据库

    task_obj = models.Task.objects.get(id=task_id)

    pool = multiprocessing.Pool(processes=settings.MAXTASKPROCESSES)

    if task_obj.task_type == 0:  # cmd
        task_func = cmd_run
    else:
        task_func = file_transfer

    for tasklog_obj in task_obj.tasklog_set.all():
        pool.apply_async(task_func,args=(tasklog_obj.id,task_id,task_obj.content))


    print("-----------------",task_obj)
    pool.close()
    pool.join()




