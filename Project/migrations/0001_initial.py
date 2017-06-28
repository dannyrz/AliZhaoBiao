# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-28 03:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Organization', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IID', models.CharField(max_length=32, verbose_name='IID')),
                ('Name', models.CharField(max_length=100, verbose_name='项目名称')),
                ('SerialNumber', models.CharField(blank=True, max_length=100, verbose_name='项目编号')),
                ('OrganizationName', models.CharField(max_length=100)),
                ('Address', models.CharField(blank=True, max_length=200, verbose_name='项目地点')),
                ('BuildDimensions', models.FloatField(default=0, verbose_name='建筑面积')),
                ('Country', models.CharField(blank=True, max_length=200, verbose_name='国家')),
                ('Province', models.CharField(blank=True, max_length=50, verbose_name='省份')),
                ('City', models.CharField(blank=True, max_length=50, verbose_name='城市')),
                ('District', models.CharField(blank=True, max_length=50, verbose_name='区域')),
                ('Abstract', models.TextField(blank=True, max_length=2000, verbose_name='项目概述')),
                ('DocumentURL', models.FileField(blank=True, upload_to='upload', verbose_name='相关文件')),
                ('Status', models.IntegerField(choices=[(0, '发布公告'), (1, '招标中'), (-1, '取消')], default=1, verbose_name='状态')),
                ('OrganizationID', models.ForeignKey(blank=True, on_delete='id', to='Organization.Info', to_field='IID')),
            ],
        ),
    ]