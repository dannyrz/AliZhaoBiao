# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-14 06:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Chong', '0007_auto_20170713_0619'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='StartURL',
            field=models.CharField(default='', max_length=5000, verbose_name='起始页'),
        ),
    ]