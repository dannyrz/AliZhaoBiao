# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-01 00:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Chong', '0003_auto_20170630_0847'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='Account',
            field=models.CharField(default='UTF-8', max_length=100, verbose_name='账号,密码'),
        ),
        migrations.AddField(
            model_name='task',
            name='NeedLogin',
            field=models.BooleanField(default=0, verbose_name='需要登陆'),
        ),
    ]
