from django.db import models
from django.contrib.auth.models import User

class IDC(models.Model):
    """
    机房表
    """
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Host(models.Model):
    """
    存储所有主机信息
    """
    hostname = models.CharField(max_length=64, unique=True)
    ip_addr = models.GenericIPAddressField(unique=True)
    port = models.IntegerField(default=22)
    idc = models.ForeignKey("IDC", models.CASCADE)
    # host_group = models.ManyToManyField("HostGroup")
    # host_users = models.ManyToManyField("HostUser")
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return "%s-%s" % (self.hostname, self.ip_addr)


class HostGroup(models.Model):
    """
    主机组
    """
    name = models.CharField(max_length=64, unique=True)
    # hosts = models.ManyToManyField("Host")
    host_user_binds = models.ManyToManyField("HostUserBind")

    def __str__(self):
        return self.name


class HostUser(models.Model):
    """
    存储远程主机的用户信息
    """
    auth_type_choices = ((0, "ssh-password"), (1, "ssh-key"))
    auth_type = models.SmallIntegerField(choices=auth_type_choices)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return "%s-%s-%s" % (self.get_auth_type_display(), self.username, self.password)

    class Meta:
        unique_together = ("username", "password")


class Task(models.Model):
    """存储任务信息"""
    task_type_choice = (
        (0,"cmd"),(1,"file_transfer"),
    )
    task_type = models.SmallIntegerField(choices=task_type_choice)
    host_user_binds = models.ManyToManyField("HostUserBind")
    content = models.TextField("任务内容")
    taskout = models.IntegerField("任务超时",default=300)
    account = models.ForeignKey("Account",on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    # success_num = models.SmallIntegerField()
    # failed_num = models.SmallIntegerField()
    # total_num = models.SmallIntegerField()

class TaskLog(models.Model):
    task = models.ForeignKey("Task",on_delete=models.CASCADE)
    host_user_bind = models.ForeignKey("HostUserBind",on_delete=models.CASCADE)
    result = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    status_choices = (
        (0,"成功"),(1,"失败"),(2,"超时"),
    )
    status = models.IntegerField(choices=status_choices)

    class Meta:
        unique_together = (
            ("task","host_user_bind"),
        )




class Token(models.Model):
    host_user_bind = models.ForeignKey("HostUserBind",on_delete=models.CASCADE)
    val = models.CharField(max_length=128,unique=True)
    account = models.ForeignKey("Account",on_delete=models.CASCADE)
    expire = models.IntegerField("超时时间(s)",default=300)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s-%s" % (self.host_user_bind,self.val)

    # class Meta:
    #     unique_together = (
    #         ("host_user_bind","val"),
    #     )

class HostUserBind(models.Model):
    """
    绑定主机和用户
    """
    host = models.ForeignKey("Host", models.CASCADE)
    host_user = models.ForeignKey("HostUser", models.CASCADE)

    def __str__(self):
        return "%s-%s" % (self.host, self.host_user)

    class Meta:
        unique_together = ("host", "host_user")


class AuditLog(models.Model):
    """
    审计日志
    """
    session = models.ForeignKey("SessionLog", models.CASCADE)
    cmd = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s-%s" % (self.session, self.cmd)


class SessionLog(models.Model):
    account = models.ForeignKey("Account", models.CASCADE)
    host_user_bind = models.ForeignKey("HostUserBind", models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "%s-%s" % (self.account, self.host_user_bind)


class Account(models.Model):
    """
    堡垒机账户
    1.扩展
    2.继承
    """
    user = models.OneToOneField(User, models.CASCADE)
    name = models.CharField(max_length=64)
    host_user_bind = models.ManyToManyField("HostUserBind", blank=True)
    host_groups = models.ManyToManyField("HostGroup", blank=True)




