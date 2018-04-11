from django.contrib import admin
from audit import models
# Register your models here.

class HostUserAdmin(admin.ModelAdmin):
    list_display = ('id','auth_type','username')




admin.site.register(models.Host)
admin.site.register(models.HostUser,HostUserAdmin)
admin.site.register(models.HostGroup)
admin.site.register(models.HostUserBind)
admin.site.register(models.Account)
admin.site.register(models.IDC)
admin.site.register(models.AuditLog)
admin.site.register(models.SessionLog)
