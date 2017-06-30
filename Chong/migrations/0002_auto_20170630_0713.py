# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-30 07:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Chong', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='EnableBroswer',
            field=models.IntegerField(choices=[(0, '关闭'), (1, '启用')], default=0, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='task',
            name='ThreadNumber',
            field=models.IntegerField(default=1, verbose_name='线程数'),
        ),
        migrations.AlterField(
            model_name='task',
            name='WorkInterval',
            field=models.IntegerField(default=1, verbose_name='间隔时(min)'),
        ),
    ]
