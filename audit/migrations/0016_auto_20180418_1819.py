# Generated by Django 2.0.1 on 2018-04-18 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audit', '0015_auto_20180418_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='timeout',
            field=models.IntegerField(default=10, verbose_name='任务超时'),
        ),
    ]
