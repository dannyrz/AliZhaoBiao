# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-18 01:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Chong', '0010_auto_20170718_0130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='PagePropertyRegularExpression',
            field=models.TextField(max_length=100, verbose_name='属性内容匹配'),
        ),
    ]